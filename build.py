#!/usr/bin/env python3
"""Builds the site into public/. Netlify runs this on every change.

Page texts live in content/pages/*.json and updates in content/updates/*.md; both are edited at /admin.
The layout and structured data for search engines are defined here.
"""
import datetime, glob, html, json, os, re, shutil
from mdlite import parse_front_matter, markdown

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'public')
SITE = 'https://lennywinnemuller.com'
PERSON_ID = SITE + '/#lenny'
NAV = [('/about/', 'About me'), ('/updates/', 'Market updates'), ('/program/', 'Six-month program')]


def load(name):
    return json.load(open(os.path.join(HERE, 'content', 'pages', name + '.json'), encoding='utf-8'))


C = {n: load(n) for n in ['site', 'home', 'about', 'updates', 'program']}
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
SOCIAL = [(name, S.get(key)) for key, name in [('instagram', 'Instagram'), ('x', 'X'), ('linkedin', 'LinkedIn')] if S.get(key)]

PERSON = {
    "@type": "Person", "@id": PERSON_ID, "name": "Lenny Winnemuller", "url": SITE + "/",
    "image": PHOTO, "jobTitle": "Long-term investing coach",
    "description": "Coach who teaches long-term investing as a skill through a personal six-month coaching program. Education and coaching only, no investment advice.",
    "email": "mailto:" + S['email'],
    "address": {"@type": "PostalAddress", "addressLocality": "Amsterdam", "addressCountry": "NL"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of Amsterdam"},
    "knowsAbout": ["Long-term investing", "Investor psychology", "Group behavior", "Behavioral finance", "Portfolio management"],
    "sameAs": [url for _, url in SOCIAL],
}
SERVICE = {
    "@type": "Service", "@id": SITE + "/program/#service", "name": "Six-Month Coaching Program in Long-Term Investing",
    "serviceType": "Investing education and coaching", "provider": {"@id": PERSON_ID}, "url": SITE + "/program/",
    "description": C['program']['seo_description'],
    "areaServed": "Worldwide",
}


# ---------- shared building blocks ----------

def link_button(text, href, primary=True):
    cls = 'btn' if primary else 'textlink'
    arrow = '' if primary else ' →'
    return f'<a class="{cls}" href="{e(href)}">{e(text)}{arrow}</a>'


def sec_head(title, link=None, link_text=None, tag='h2'):
    more = f'<a href="{e(link)}">{e(link_text)} →</a>' if link and link_text else ''
    return f'<div class="sec-h"><{tag}>{e(title)}</{tag}>{more}</div>'


def cta_band(eyebrow=None, title=None, text=None, button=None, link=None):
    return f'''<section class="cta-band">
    <div class="wrap">
      <div class="cta-inner">
        <div>
          <p class="kicker">{e(eyebrow or S['cta_eyebrow'])}</p>
          <h2>{e(title or S['cta_title'])}</h2>
          <p>{e(text or S['cta_text'])}</p>
        </div>
        {link_button(button or S['cta_button'], link or S['cta_link'])}
      </div>
    </div>
  </section>'''


def numbered(items, cls='numbered'):
    """Ruled, numbered list of title + text items (cards in the editor)."""
    li = ''.join(f'<li><span><b>{e(c["title"])}</b>{e(c["text"])}</span></li>' for c in items)
    return f'<ol class="{cls}">{li}</ol>'


def columns(items, label_key=None):
    """Items side by side, separated by thin vertical rules, like newspaper columns."""
    out = ''
    for c in items:
        label = f'<p class="col-label">{e(c[label_key])}</p>' if label_key else ''
        out += f'<div class="col">{label}<h3>{e(c["title"])}</h3><p>{e(c["text"])}</p></div>'
    return f'<div class="cols-ruled n{min(len(items), 4)}">{out}</div>'


def social_links(sep=' · '):
    links = sep.join(f'<a href="{e(url)}" rel="me noopener" target="_blank">{name}</a>' for name, url in SOCIAL)
    return f'<p class="social">{links}</p>' if links else ''


def figure(src, caption, cls='figure', alt=None, eager=False):
    if not str(src or '').strip():
        return ''
    cap = f'<figcaption>{e(caption)}</figcaption>' if str(caption or '').strip() else ''
    load = '' if eager else ' loading="lazy"'
    return f'<figure class="{cls}"><img src="{e(src)}" alt="{e(alt or caption or "Lenny Winnemuller")}"{load}>{cap}</figure>'


def page(path, title, desc, body, active=None, graph=None, announce=True, og_type='website', image=None):
    head_ld = ''
    if graph:
        head_ld = '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False) + '\n</script>\n'
    current = ' aria-current="page"'
    nav = ''.join(f'<a href="{h}"{current if h == active else ""}>{t}</a>' for h, t in NAV)
    nav += f'<a class="book" href="{e(S["cta_link"])}">Book an intro call</a>'
    # The banner only shows when a banner text is filled in at /admin.
    ann = ''
    if announce and str(S.get('announce_text') or '').strip():
        link = f' · <a href="{e(S.get("announce_url") or S["cta_link"])}">{e(S.get("announce_link"))}</a>' if str(S.get('announce_link') or '').strip() else ''
        ann = f'<div class="announce">{e(S["announce_text"])}{link}</div>\n'
    latest = f'<a href="{POSTS[0]["path"]}">Latest update: {POSTS[0]["date_label"]}</a>' if POSTS else 'Education and coaching, no investment advice'
    fnav = ''.join(f'<a href="{h}">{t}</a>' for h, t in [('/', 'Home')] + NAV + [('/privacy/', 'Privacy policy')])
    title, desc = e(title), e(desc)
    og_image = e(absolute(image) if image else PHOTO)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/newsreader-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
<link rel="alternate" type="application/rss+xml" title="Market updates by Lenny Winnemuller" href="/updates/feed.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{og_image}">
{head_ld}</head>
<body>
{ann}<header class="mast">
  <div class="wrap">
    <div class="mast-top"><span>Amsterdam · Education and coaching, no investment advice</span><span>{latest}</span></div>
    <a class="brand" href="/">Lenny Winnemuller</a>
    <nav class="menu" aria-label="Main">{nav}</nav>
  </div>
</header>

<main>
{body}
</main>

<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <p class="foot-name">Lenny Winnemuller</p>
        <p>{e(S['footer_tagline'])}<br><a href="mailto:{e(S['email'])}">{e(S['email'])}</a></p>
        {social_links()}
      </div>
      <nav class="fnav" aria-label="Footer">{fnav}</nav>
    </div>
    <div class="disclaimer">{md(S['disclaimer'])}</div>
    <p>© {datetime.date.today().year} Lenny Winnemuller</p>
  </div>
</footer>
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
        slug = os.path.basename(f)[:-3]
        # Optional short URL set in the editor; the file name stays the same.
        url = re.sub(r'[^a-z0-9]+', '-', str(m.get('url') or '').lower()).strip('-')
        posts.append({
            'date': d.isoformat(),
            'date_label': d.strftime('%A ') + str(d.day) + d.strftime(' %B %Y'),
            'week': f'Week {week}, {year}',
            'title': str(m['title']).strip(),
            'description': str(m.get('description', '')).strip(),
            'body': markdown(body),
            'cover': str(m.get('image') or '').strip(),
            # Picture for lists and social media: the image field, or else the first image in the text.
            'image': str(m.get('image') or '').strip() or (re.search(r'!\[[^\]]*\]\(([^)\s]+)\)', body) or [None, ''])[1],
            'slug': slug,
            'path': f"/updates/{url or slug}/",
            'old_path': f"/updates/{slug}/" if url and url != slug else None,
        })
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    return posts


POSTS = load_posts()



def post_meta(p, short=False):
    if short:
        return f'<p class="date"><time datetime="{p["date"]}">{p["date_label"].split(" ", 1)[1]}</time></p>'
    return f'<p class="date"><time datetime="{p["date"]}">{p["week"]} · {p["date_label"]}</time></p>'


def front_page(posts):
    """The latest updates laid out like the front page of a newspaper."""
    if not posts:
        return '<p class="muted">The first update is published soon.</p>'
    lead, rest = posts[0], posts[1:4]
    img = f'<a href="{lead["path"]}" tabindex="-1"><img src="{e(lead["image"])}" alt="" loading="lazy"></a>' if lead['image'] else ''
    out = f'<article class="lead-story">{img}{post_meta(lead, True)}<h3><a href="{lead["path"]}">{e(lead["title"])}</a></h3><p>{e(lead["description"])}</p></article>'
    groups = [rest[:1], rest[1:]] if len(rest) > 1 else [rest]
    for g in groups:
        if not g:
            continue
        items = ''.join(f'<div class="story">{post_meta(p, True)}<h3><a href="{p["path"]}">{e(p["title"])}</a></h3>' + (f'<p>{e(p["description"])}</p>' if i == 0 else '') + '</div>' for i, p in enumerate(g))
        out += f'<article>{items}</article>'
    return f'<div class="front">{out}</div>'


def post_list(posts):
    if not posts:
        return '<p class="muted">The first update is published soon.</p>'
    items = ''
    for p in posts:
        thumb = f'<a class="thumb" href="{p["path"]}" tabindex="-1"><img src="{e(p["image"])}" alt="" loading="lazy"></a>' if p['image'] else ''
        items += f'<li class="{"has-thumb" if thumb else ""}"><div>{post_meta(p)}<h2><a href="{p["path"]}">{e(p["title"])}</a></h2><p>{e(p["description"])}</p></div>{thumb}</li>'
    return f'<ul class="post-list">{items}</ul>'


def build_home():
    h = C['home']
    facts = ''.join(f'<div><b>{e(f["title"])}</b>{e(f["text"])}</div>' for f in h.get('about_facts', []))
    quote = ''
    if str(h.get('quote') or '').strip():
        quote = f'''
  <section class="quote-sec">
    <div class="wrap"><blockquote class="pull">“{e(h['quote'])}”<cite>{e(h.get('quote_author') or 'Lenny Winnemuller')}</cite></blockquote></div>
  </section>'''
    body = f'''
  <section class="opening">
    <div class="wrap"><div class="opening-grid">
      <div>
        <p class="kicker">{e(h['hero_eyebrow'])}</p>
        <h1>{md_inline(h['hero_title'])}</h1>
        <p class="deck">{e(h['hero_text'])}</p>
        <div class="actions">{link_button(h['hero_button'], '/program/')}{link_button(h['hero_button_call'], S['cta_link'], False)}</div>
      </div>
      {figure(h.get('hero_photo'), h.get('hero_caption'), 'figure tall', eager=True)}
    </div></div>
  </section>

  <section id="updates">
    <div class="wrap">
      {sec_head(h['updates_title'], '/updates/', h['updates_button'])}
      {front_page(POSTS)}
    </div>
  </section>

  <section id="about">
    <div class="wrap">
      {sec_head(h['about_eyebrow'], '/about/', h['about_button'])}
      <div class="about-grid">
        {figure(h['photo'], None, 'figure portrait', alt='Portrait of Lenny Winnemuller')}
        <div class="body">
          <h3>{e(h['about_title'])}</h3>
          {md(h['about_text'])}
        </div>
        <div class="facts">{facts}</div>
      </div>
    </div>
  </section>
{quote}
  <section id="program">
    <div class="wrap">
      {sec_head(h['program_eyebrow'], '/program/', h['program_button'])}
      <div class="program-grid">
        {figure(h.get('program_photo'), h.get('program_caption'))}
        <div>
          <h3 class="subhead">{e(h['program_title'])}</h3>
          <p class="deck small">{e(h['program_intro'])}</p>
          {numbered(h['program_cards'])}
        </div>
      </div>
    </div>
  </section>

  {cta_band()}
'''
    page('/', h['seo_title'], h['seo_description'], body, graph=[PERSON, SERVICE])


def build_about():
    a = C['about']
    photos = a.get('photos', [])
    gallery = ''.join(figure(f['image'], f.get('caption')) for f in photos)
    body = f'''
  <section class="pagehead">
    <div class="wrap about-head">
      {figure(a['photo'], None, 'figure portrait', alt='Portrait of Lenny Winnemuller', eager=True)}
      <div>
        <p class="kicker">{e(a['eyebrow'])}</p>
        <h1>{e(a['title'])}</h1>
        <div class="body dropcap">{md(a['text'])}</div>
        {social_links()}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      {sec_head(a['photos_title'])}
      <div class="gallery n{min(len(photos), 3)}">{gallery}</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      {sec_head(a.get('approach_title', ''))}
      <div class="approach">
        <div class="essay">{md(a.get('approach_text', ''))}</div>
        {columns(a.get('expertise', []))}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      {sec_head(a['section_title'])}
      <div class="essay">{md(a['section_text'])}</div>
    </div>
  </section>

  {cta_band()}
'''
    page('/about/', a['seo_title'], a['seo_description'], body, active='/about/', graph=[PERSON])


def build_updates():
    u = C['updates']
    body = f'''
  <section class="pagehead">
    <div class="wrap">
      <p class="kicker">{e(u['eyebrow'])}</p>
      <h1>{e(u['title'])}</h1>
      <p class="deck">{e(u['intro'])}</p>
    </div>
  </section>
  <section class="tight">
    <div class="wrap">
      {post_list(POSTS)}
      <p class="muted small"><a href="/updates/feed.xml">RSS feed</a></p>
    </div>
  </section>
  {cta_band()}
'''
    blog = {"@type": "Blog", "@id": SITE + "/updates/#blog", "name": "Weekly Market Updates by Lenny Winnemuller", "url": SITE + "/updates/", "author": {"@id": PERSON_ID}, "inLanguage": "en"}
    page('/updates/', u['seo_title'], u['seo_description'], body, active='/updates/', graph=[blog, PERSON])


def build_program():
    p = C['program']
    highlights = ''.join(f'<li>{e(t)}</li>' for t in p['highlights'])
    for_points = ''.join(f'<li>{e(t)}</li>' for t in p['for_points'])
    notfor_points = ''.join(f'<li>{e(t)}</li>' for t in p['notfor_points'])
    modules = ''.join(f'<tr{" class=review" if not m["title"][:1].isdigit() else ""}><td>{e(m["weeks"])}</td><th scope="row">{e(m["title"])}</th><td>{e(m["defense"])}</td><td>{e(m["portfolio"])}</td></tr>' for m in p['modules'])
    faq_html = ''.join(f'<details><summary>{e(f["question"])}</summary>{md(f["answer"])}</details>\n      ' for f in p['faq'])
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f['question'], "acceptedAnswer": {"@type": "Answer", "text": f['answer']}} for f in p['faq']]}
    body = f'''
  <section class="opening">
    <div class="wrap"><div class="opening-grid">
      <div>
        <p class="kicker">{e(p['eyebrow'])}</p>
        <h1>{e(p['title'])}</h1>
        <p class="deck">{e(p['intro'])}</p>
        <ul class="ruled">{highlights}</ul>
        <div class="actions">{link_button(p['cta_button'], p['cta_link'])}</div>
      </div>
      {figure(p.get('hero_photo'), p.get('hero_caption'), 'figure tall', eager=True)}
    </div></div>
  </section>

  <section>
    <div class="wrap two-text">
      <div>
        {sec_head(p['why_title'])}
        <div class="body">{md(p['why_text'])}</div>
      </div>
      <div>
        {sec_head(p['learn_title'])}
        <div class="body">{md(p['learn_text'])}</div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap two-text">
      <div>
        {sec_head(p['for_title'], tag='h2')}
        <ul class="ruled yes">{for_points}</ul>
      </div>
      <div>
        {sec_head(p['notfor_title'], tag='h2')}
        <ul class="ruled no">{notfor_points}</ul>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      {sec_head(p['req_title'])}
      {columns(p['requirements'])}
    </div>
  </section>

  <section>
    <div class="wrap">
      {sec_head(p['year_title'])}
      <p class="deck small">{e(p['year_intro'])}</p>
      {columns(p['quarters'], 'label')}
      <details class="modules">
        <summary>{e(p['modules_button'])}</summary>
        <div class="table-scroll">
          <table>
            <thead><tr><th scope="col">Weeks</th><th scope="col">Module</th><th scope="col">Thesis defense or review</th><th scope="col">Paper portfolio</th></tr></thead>
            <tbody>{modules}</tbody>
          </table>
        </div>
      </details>
    </div>
  </section>

  <section>
    <div class="wrap">
      {sec_head(p['how_title'])}
      {numbered(p['how'], 'numbered two-up')}
    </div>
  </section>

  <section>
    <div class="wrap program-grid">
      {figure(p.get('deliverables_photo'), p.get('deliverables_caption'))}
      <div>
        {sec_head(p['deliverables_title'])}
        <p class="deck small">{e(p['deliverables_intro'])}</p>
        {numbered(p['deliverables'])}
      </div>
    </div>
  </section>

  <section class="quote-sec">
    <div class="wrap">
      <h2 class="center-title">{e(p['assessed_title'])}</h2>
      <div class="pull small">{md(p['assessed_text'])}</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      {sec_head(p['coach_eyebrow'], '/about/', p['coach_button'])}
      <div class="about-grid two">
        {figure(p['coach_photo'], None, 'figure portrait', alt='Lenny Winnemuller teaching')}
        <div class="body dropcap">
          <h3>{e(p['coach_title'])}</h3>
          {md(p['coach_text'])}
        </div>
      </div>
    </div>
  </section>

  <section class="faq">
    <div class="wrap narrow">
      {sec_head(p['faq_title'])}
      {faq_html}
    </div>
  </section>

  {cta_band(p['cta_eyebrow'], p['cta_title'], p['cta_text'], p['cta_button'], p['cta_link'])}
'''
    page('/program/', p['seo_title'], p['seo_description'], body, active='/program/', graph=[SERVICE, faq_ld, PERSON])


def captioned_images(body_html):
    """Turns a Markdown image on its own line into a figure with its description as caption."""
    return re.sub(r'<p><img src="([^"]+)" alt="([^"]*)"></p>',
                  lambda m: f'<figure class="figure"><img src="{m.group(1)}" alt="{m.group(2)}" loading="lazy">' + (f'<figcaption>{m.group(2)}</figcaption>' if m.group(2) else '') + '</figure>',
                  body_html)


def build_post(p):
    article = {"@type": "BlogPosting", "@id": SITE + p['path'] + "#article", "headline": p['title'],
               "description": p['description'], "datePublished": p['date'], "author": {"@id": PERSON_ID},
               "publisher": {"@id": PERSON_ID}, "isPartOf": {"@id": SITE + "/updates/#blog"},
               "mainEntityOfPage": SITE + p['path'], "inLanguage": "en", "image": absolute(p['image']) if p['image'] else PHOTO}
    body = f'''
  <article class="post">
    <header class="post-head">
      <div class="wrap prose">
        <p class="kicker"><a href="/updates/">Market updates</a> · {p['week']}</p>
        <h1>{e(p['title'])}</h1>
        <p class="deck">{e(p['description'])}</p>
        <p class="byline">By <a href="/about/">Lenny Winnemuller</a> · <time datetime="{p['date']}">{p['date_label']}</time></p>
      </div>
    </header>
    <div class="wrap prose">
      {figure(p['cover'], None, 'figure cover', alt=p['title'], eager=True) if p['cover'] and p['cover'] not in p['body'] else ''}
      {captioned_images(p['body'])}
      <p class="post-disclaimer">{e(S['update_disclaimer'])}</p>
      <p><a class="textlink" href="/updates/">← All market updates</a></p>
    </div>
  </article>
  {cta_band()}
'''
    page(p['path'], f"{p['title']} | {p['week']} | Lenny Winnemuller", p['description'], body,
         active='/updates/', graph=[article, PERSON], og_type='article', image=p['image'])


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
         '<section class="pagehead"><div class="wrap narrow"><h1>Page not found</h1><p class="deck">This page doesn\'t exist. Go to the <a href="/">homepage</a> or the <a href="/program/">six-month program</a>.</p></div></section>')
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
    with open(os.path.join(OUT, '_redirects'), 'a', encoding='utf-8') as r:
        for p in POSTS:
            if p['old_path']:
                r.write(f"\n{p['old_path']}  {p['path']}  301")
    shutil.copytree(os.path.join(HERE, 'admin'), os.path.join(OUT, 'admin'))
    shutil.copytree(os.path.join(HERE, 'static'), OUT, dirs_exist_ok=True)
    build_home(); build_about(); build_updates(); build_program(); build_privacy(); build_404()
    for p in POSTS:
        build_post(p)
    build_feed()
    paths = ['/', '/about/', '/updates/', '/program/', '/privacy/'] + [p['path'] for p in POSTS]
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
