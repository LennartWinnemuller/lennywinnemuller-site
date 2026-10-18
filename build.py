#!/usr/bin/env python3
"""Builds the site into public/. Netlify runs this on every change.

Page texts live in content/pages/*.json and updates in content/updates/*.md; both are edited at /admin.
The layout, structured data for search engines and the Kit form are defined here.
"""
import datetime, glob, html, json, os, shutil
from mdlite import parse_front_matter, markdown

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'public')
SITE = 'https://lennywinnemuller.com'
PERSON_ID = SITE + '/#lenny'
NAV = [('/workshop/', 'Free workshop'), ('/about/', 'About me'), ('/updates/', 'Market updates'), ('/program/', '12-month program')]


def load(name):
    return json.load(open(os.path.join(HERE, 'content', 'pages', name + '.json'), encoding='utf-8'))


C = {n: load(n) for n in ['site', 'home', 'workshop', 'about', 'updates', 'program']}
S = C['site']


def e(text):
    """Plain text field, safe for HTML text and attributes."""
    return html.escape(str(text or '').strip())


def md(text):
    return markdown(str(text or ''))


def md_inline(text):
    """Markdown for one line, without the surrounding paragraph."""
    out = markdown(str(text or '').strip())
    return out[3:-4] if out.startswith('<p>') and out.endswith('</p>') and out.count('<p>') == 1 else out


def absolute(url):
    url = str(url or '')
    return SITE + url if url.startswith('/') else url


PHOTO = absolute(C['about'].get('photo') or C['home'].get('photo'))

PERSON = {
    "@type": "Person", "@id": PERSON_ID, "name": "Lenny Winnemuller", "url": SITE + "/",
    "image": PHOTO, "jobTitle": "Long-term investing coach",
    "description": "Coach who teaches long-term investing as a skill through a personal 12-month coaching program. Education and coaching only, no investment advice.",
    "email": "mailto:" + S['email'],
    "address": {"@type": "PostalAddress", "addressLocality": "Amsterdam", "addressCountry": "NL"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of Amsterdam"},
    "knowsAbout": ["Long-term investing", "Investor psychology", "Group behavior", "Behavioral finance", "Portfolio management"],
}
SERVICE = {
    "@type": "Service", "@id": SITE + "/program/#service", "name": "12-Month Coaching Program in Long-Term Investing",
    "serviceType": "Investing education and coaching", "provider": {"@id": PERSON_ID}, "url": SITE + "/program/",
    "description": C['program']['seo_description'],
    "areaServed": "Worldwide",
}
W = C['workshop']
EVENT = {
    "@type": "Event", "@id": SITE + "/workshop/#event",
    "name": f"{W['title']}: {W['subtitle']}",
    "description": W['seo_description'],
    "startDate": W['event_start'], "endDate": W['event_end'],
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
    "location": {"@type": "VirtualLocation", "url": SITE + "/workshop/"},
    "image": PHOTO, "organizer": {"@id": PERSON_ID}, "performer": {"@id": PERSON_ID},
    "isAccessibleForFree": True,
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
               "url": SITE + "/workshop/", "validFrom": "2026-10-14"},
}


def kit_form():
    options = json.dumps({"settings": {"after_subscribe": {"action": "message", "success_message": "You’re in! Check your inbox to confirm your spot.", "redirect_url": ""},
                                       "recaptcha": {"enabled": False}, "return_visitor": {"action": "show", "custom_content": ""}}, "version": "5"}, ensure_ascii=False)
    return f'''<div class="signup" id="signup">
        <h3>{e(W['form_title'])}</h3>
        <p class="sub">{e(W['form_subtitle'])}</p>
        <form action="https://app.kit.com/forms/10043918/subscriptions" class="seva-form formkit-form" method="post" data-sv-form="10043918" data-uid="3d027c31fc" data-format="inline" data-version="5" data-options='{html.escape(options, quote=False)}'>
          <ul class="formkit-alert formkit-alert-error" data-element="errors" data-group="alert"></ul>
          <div data-element="fields" class="seva-fields formkit-fields">
            <div class="formkit-field">
              <label for="ck-first-name">First name</label>
              <input id="ck-first-name" class="formkit-input" name="fields[first_name]" type="text" autocomplete="given-name" required>
            </div>
            <div class="formkit-field">
              <label for="ck-email">Email address</label>
              <input id="ck-email" class="formkit-input" name="email_address" type="email" autocomplete="email" required>
            </div>
            <button data-element="submit" class="formkit-submit btn" type="submit">
              <div class="formkit-spinner"><div></div><div></div><div></div></div>
              <span>{e(W['form_button'])}</span>
            </button>
          </div>
        </form>
        <p class="fine">{md_inline(W['form_fineprint'])}</p>
      </div>'''


def workshop_section(h1_style=' style="color:#fff"', extra_class=''):
    points = ''.join(f'<li>{e(p)}</li>' for p in W['learn_points'])
    return f'''
  <section class="dark workshop{extra_class}" id="workshop">
    <div class="wrap">
      <div>
        <p class="eyebrow">{e(W['eyebrow'])}</p>
        <h1{h1_style}>{e(W['title'])}</h1>
        <p class="subtitle">{e(W['subtitle'])}</p>
        <p class="when">{e(W['date_line'])}
          <small>{e(W['details_line'])}</small></p>
        <p>{e(W['learn_intro'])}</p>
        <ul>{points}</ul>
      </div>
      {kit_form()}
    </div>
  </section>'''


def cta_band(eyebrow=None, title=None, text=None, button=None):
    return f'''<section class="dark cta-band">
    <div class="wrap">
      <div>
        <p class="eyebrow">{e(eyebrow or S['cta_eyebrow'])}</p>
        <h2>{e(title or S['cta_title'])}</h2>
        <p>{e(text or S['cta_text'])}</p>
      </div>
      <a class="btn light" href="/workshop/">{e(button or S['cta_button'])}</a>
    </div>
  </section>'''


def cards(items, cls='grid', tag=None):
    t = f'<span class="tag">{e(tag)}</span>' if tag else ''
    return f'<div class="{cls}">' + ''.join(f'<div class="card">{t}<h3>{e(c["title"])}</h3><p>{e(c["text"])}</p></div>' for c in items) + '</div>'


def portrait(src):
    return f'<div class="photo"><img class="portrait" src="{e(src)}" alt="Portrait of Lenny Winnemuller" width="400" height="500"></div>'


def analytics():
    """Cloudflare Web Analytics: cookieless visitor stats. Only added once a token is set in Site settings."""
    token = str(S.get('analytics_token') or '').strip()
    if not token:
        return ''
    beacon = html.escape(json.dumps({"token": token}))
    return f"<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" data-cf-beacon='{beacon}'></script>\n"


def page(path, title, desc, body, active=None, graph=None, announce=True, kit=False, og_type='website'):
    head_ld = ''
    if graph:
        head_ld = '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False) + '\n</script>\n'
    current = ' aria-current="page"'
    nav = ''.join(f'<a href="{h}"{current if h == active else ""}>{t}</a>' for h, t in NAV)
    ann = f'<div class="announce">{e(S["announce_text"])} · <a href="/workshop/">{e(S["announce_link"])}</a></div>\n' if announce else ''
    fnav = ''.join(f'<a href="{h}">{t}</a>' for h, t in [('/', 'Home')] + NAV + [('/privacy/', 'Privacy policy')])
    title, desc = e(title), e(desc)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css">
<link rel="alternate" type="application/rss+xml" title="Market updates by Lenny Winnemuller" href="/updates/feed.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{e(PHOTO)}">
{head_ld}{analytics()}</head>
<body>
{ann}<header class="top">
  <div class="wrap">
    <a class="brand" href="/">Lenny Winnemuller</a>
    <nav class="menu" aria-label="Main">{nav}</nav>
  </div>
</header>

<main>
{body}
</main>

<footer>
  <div class="wrap">
    <div class="cols">
      <div><strong style="color:var(--ink);font-family:var(--serif);font-size:1.1rem;font-weight:400">Lenny Winnemuller</strong><br>{e(S['footer_tagline'])}<br><a href="mailto:{e(S['email'])}">{e(S['email'])}</a></div>
      <nav class="fnav" aria-label="Footer">{fnav}</nav>
    </div>
    <div class="disclaimer">{md(S['disclaimer'])}</div>
    <p>© {datetime.date.today().year} Lenny Winnemuller</p>
  </div>
</footer>
{'<script src="https://f.convertkit.com/ckjs/ck.5.js"></script>' if kit else ''}
</body>
</html>
'''
    rel = path.strip('/')
    dest = os.path.join(OUT, rel, 'index.html') if rel else os.path.join(OUT, 'index.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8').write(doc)


def load_posts():
    posts = []
    for f in glob.glob(os.path.join(HERE, 'content', 'updates', '*.md')):
        m, body = parse_front_matter(open(f, encoding='utf-8').read())
        d = datetime.date.fromisoformat(str(m['date'])[:10])
        year, week, _ = d.isocalendar()
        posts.append({
            'date': d.isoformat(),
            'date_label': d.strftime('%A ') + str(d.day) + d.strftime(' %B %Y'),
            'week': f'Week {week}, {year}',
            'title': str(m['title']).strip(),
            'description': str(m.get('description', '')).strip(),
            'body': markdown(body),
            'slug': os.path.basename(f)[:-3],
            'path': f"/updates/{os.path.basename(f)[:-3]}/",
        })
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    return posts


POSTS = load_posts()


def post_list(posts):
    if not posts:
        return '<div class="empty"><strong style="color:var(--ink)">The first update is published soon.</strong></div>'
    items = ''.join(f'<li><time datetime="{p["date"]}">{p["week"]} · {p["date_label"]}</time><br><a href="{p["path"]}">{e(p["title"])}</a><p class="muted" style="margin:6px 0 0">{e(p["description"])}</p></li>' for p in posts)
    return f'<ul class="post-list">{items}</ul>'


def build_home():
    h = C['home']
    body = workshop_section(extra_class=' hero-workshop') + f'''

  <section id="about">
    <div class="wrap split">
      {portrait(h['photo'])}
      <div>
        <p class="eyebrow">{e(h['about_eyebrow'])}</p>
        <h2>{e(h['about_title'])}</h2>
        {md(h['about_text'])}
        <a class="btn ghost" href="/about/">{e(h['about_button'])}</a>
      </div>
    </div>
  </section>

  <section class="band" id="updates">
    <div class="wrap">
      <p class="eyebrow">{e(h['updates_eyebrow'])}</p>
      <h2>{e(h['updates_title'])}</h2>
      <p class="lead">{e(h['updates_intro'])}</p>
      <div style="margin-top:12px">{post_list(POSTS[:3])}</div>
      <div class="btns" style="margin-top:20px"><a class="btn ghost" href="/updates/">{e(h['updates_button'])}</a></div>
    </div>
  </section>

  <section id="program">
    <div class="wrap">
      <p class="eyebrow">{e(h['program_eyebrow'])}</p>
      <h2>{e(h['program_title'])}</h2>
      <p class="lead">{e(h['program_intro'])}</p>
      {cards(h['program_cards'], 'grid four', h['program_tag'])}
      <div class="btns" style="margin-top:28px"><a class="btn" href="/program/">{e(h['program_button'])}</a></div>
    </div>
  </section>
'''
    page('/', h['seo_title'], h['seo_description'], body, graph=[PERSON, EVENT, SERVICE], announce=False, kit=True)


def build_workshop():
    points = ''.join(f'<li>{e(p)}</li>' for p in W['for_points'])
    body = workshop_section() + f'''

  <section>
    <div class="wrap narrow">
      <h2>{e(W['for_title'])}</h2>
      <ul class="checklist">{points}</ul>
      {md(W['after_text'])}
    </div>
  </section>
'''
    page('/workshop/', W['seo_title'], W['seo_description'], body, active='/workshop/', graph=[EVENT, PERSON], announce=False, kit=True)


def build_about():
    a = C['about']
    body = f'''
  <section class="pagehead">
    <div class="wrap split">
      {portrait(a['photo'])}
      <div>
        <p class="eyebrow">{e(a['eyebrow'])}</p>
        <h1>{e(a['title'])}</h1>
        {md(a['text'])}
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap narrow">
      <h2>{e(a['section_title'])}</h2>
      {md(a['section_text'])}
    </div>
  </section>

  {cta_band()}
'''
    page('/about/', a['seo_title'], a['seo_description'], body, active='/about/', graph=[PERSON])


def build_updates():
    u = C['updates']
    body = f'''
  <section class="pagehead">
    <div class="wrap narrow">
      <p class="eyebrow">{e(u['eyebrow'])}</p>
      <h1>{e(u['title'])}</h1>
      <p class="lead">{e(u['intro'])}</p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap narrow">
      {post_list(POSTS)}
      <p class="muted" style="margin-top:20px;font-size:.9rem"><a href="/updates/feed.xml">RSS feed</a></p>
    </div>
  </section>
  {cta_band()}
'''
    blog = {"@type": "Blog", "@id": SITE + "/updates/#blog", "name": "Weekly Market Updates by Lenny Winnemuller", "url": SITE + "/updates/", "author": {"@id": PERSON_ID}, "inLanguage": "en"}
    page('/updates/', u['seo_title'], u['seo_description'], body, active='/updates/', graph=[blog, PERSON])


def build_program():
    p = C['program']
    quarters = ''.join(f'<div class="quarter"><span class="q">{e(q["label"])}</span><h3>{e(q["title"])}</h3><ul>' + ''.join(f'<li>{e(t)}</li>' for t in q['topics']) + '</ul></div>' for q in p['quarters'])
    faq_html = ''.join(f'<details><summary>{e(f["question"])}</summary>{md(f["answer"])}</details>\n      ' for f in p['faq'])
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f['question'], "acceptedAnswer": {"@type": "Answer", "text": f['answer']}} for f in p['faq']]}
    body = f'''
  <section class="pagehead">
    <div class="wrap">
      <p class="eyebrow">{e(p['eyebrow'])}</p>
      <h1>{e(p['title'])}</h1>
      <p class="lead">{e(p['intro'])}</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2>{e(p['deliverables_title'])}</h2>
      {cards(p['deliverables'], 'grid four')}
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2>{e(p['how_title'])}</h2>
      {cards(p['how'])}
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2>{e(p['year_title'])}</h2>
      <div class="quarters">{quarters}</div>
      <p class="muted" style="margin-top:20px">{e(p['year_note'])}</p>
    </div>
  </section>

  <section class="faq">
    <div class="wrap narrow">
      <h2>{e(p['faq_title'])}</h2>
      {faq_html}
    </div>
  </section>

  {cta_band(p['cta_eyebrow'], p['cta_title'], p['cta_text'], p['cta_button'])}
'''
    page('/program/', p['seo_title'], p['seo_description'], body, active='/program/', graph=[SERVICE, faq_ld, PERSON])


def build_post(p):
    article = {"@type": "BlogPosting", "@id": SITE + p['path'] + "#article", "headline": p['title'],
               "description": p['description'], "datePublished": p['date'], "author": {"@id": PERSON_ID},
               "publisher": {"@id": PERSON_ID}, "isPartOf": {"@id": SITE + "/updates/#blog"},
               "mainEntityOfPage": SITE + p['path'], "inLanguage": "en", "image": PHOTO}
    body = f'''
  <section class="pagehead">
    <div class="wrap prose">
      <p class="eyebrow"><a href="/updates/" style="color:inherit;text-decoration:none">Market updates</a> · {p['week']}</p>
      <h1>{e(p['title'])}</h1>
      <p class="muted">{p['date_label']} · By <a href="/about/">Lenny Winnemuller</a></p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap prose">
      {p['body']}
      <p class="muted" style="margin-top:2.4em;font-size:.9rem;border-top:1px solid var(--line);padding-top:1.2em">{e(S['update_disclaimer'])}</p>
      <p><a href="/updates/">← All market updates</a></p>
    </div>
  </section>
  {cta_band()}
'''
    page(p['path'], f"{p['title']} | {p['week']} | Lenny Winnemuller", p['description'], body,
         active='/updates/', graph=[article, PERSON], og_type='article')


def build_feed():
    items = ''.join(f'''
    <item>
      <title>{e(p['title'])}</title>
      <link>{SITE}{p['path']}</link>
      <guid>{SITE}{p['path']}</guid>
      <pubDate>{datetime.datetime.combine(datetime.date.fromisoformat(p['date']), datetime.time(9)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
      <description>{e(p['description'])}</description>
    </item>''' for p in POSTS[:20])
    feed = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Market updates by Lenny Winnemuller</title>
    <link>{SITE}/updates/</link>
    <description>{e(C['updates']['intro'])}</description>
    <language>en</language>{items}
  </channel>
</rss>
'''
    open(os.path.join(OUT, 'updates', 'feed.xml'), 'w', encoding='utf-8').write(feed)


def build_404():
    page('/404/', 'Page not found | Lenny Winnemuller', 'This page does not exist.',
         '<section class="pagehead"><div class="wrap narrow"><h1>Page not found</h1><p class="lead">This page doesn\'t exist. Go to the <a href="/">homepage</a> or the <a href="/workshop/">free workshop</a>.</p></div></section>')
    shutil.move(os.path.join(OUT, '404', 'index.html'), os.path.join(OUT, '404.html'))
    os.rmdir(os.path.join(OUT, '404'))


def build_privacy():
    ns = {}
    exec(open(os.path.join(HERE, 'pages', 'privacy.py'), encoding='utf-8').read(), {'ns': ns})
    page(**ns['PAGE'])


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in ['styles.css', 'favicon.svg', 'robots.txt', 'llms.txt', '_redirects']:
        shutil.copy(os.path.join(HERE, f), OUT)
    shutil.copytree(os.path.join(HERE, 'admin'), os.path.join(OUT, 'admin'))
    shutil.copytree(os.path.join(HERE, 'static'), OUT, dirs_exist_ok=True)
    build_home(); build_workshop(); build_about(); build_updates(); build_program(); build_privacy(); build_404()
    for p in POSTS:
        build_post(p)
    build_feed()
    paths = ['/', '/workshop/', '/about/', '/updates/', '/program/', '/privacy/'] + [p['path'] for p in POSTS]
    dates = {p['path']: p['date'] for p in POSTS}
    if POSTS:
        dates['/updates/'] = dates['/'] = POSTS[0]['date']
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join(f'  <url><loc>{SITE}{p}</loc>' + (f'<lastmod>{dates[p]}</lastmod>' if p in dates else '') + '</url>\n' for p in paths)
    sm += '</urlset>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
    print('built', len(paths), 'pages')


if __name__ == '__main__':
    main()
