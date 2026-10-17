#!/usr/bin/env python3
"""Builds the site into public/. Netlify runs this on every change. Updates live in content/updates/."""
import html, json, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'public')
SITE = 'https://lennywinnemuller.com'
PHOTO = 'https://embed.filekitcdn.com/e/omtcB3AA6xNUtQV1kJDToV/cdtD5ksXrdiA5LwdMvjuKv'
PERSON_ID = SITE + '/#lenny'

PERSON = {
  "@type": "Person", "@id": PERSON_ID, "name": "Lenny Winnemuller", "url": SITE + "/",
  "image": PHOTO, "jobTitle": "Long-term investing coach",
  "description": "Coach who teaches long-term investing as a skill through a personal 12-month coaching program. Education and coaching only, no investment advice.",
  "email": "mailto:info@lennywinnemuller.com",
  "address": {"@type": "PostalAddress", "addressLocality": "Amsterdam", "addressCountry": "NL"},
  "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of Amsterdam"},
  "knowsAbout": ["Long-term investing", "Investor psychology", "Group behavior", "Behavioral finance", "Portfolio management"]
}
SERVICE = {
  "@type": "Service", "@id": SITE + "/program/#service", "name": "12-Month Coaching Program in Long-Term Investing",
  "serviceType": "Investing education and coaching", "provider": {"@id": PERSON_ID}, "url": SITE + "/program/",
  "description": "Personal online 12-month coaching program in which clients learn the skill of disciplined long-term investing. Clients build an Investment Policy Statement, an investment plan, a crash plan with selling rules and a decision journal, practice with a paper portfolio from week 1, and learn to value businesses and defend their investment theses. No investment advice.",
  "areaServed": "Worldwide"
}
EVENT = {
  "@type": "Event", "@id": SITE + "/workshop/#event",
  "name": "Why Great Investors Study More and Trade Less: The 20-Decision Rule",
  "description": "Free online workshop about why the best long-term investors make surprisingly few decisions, and how studying more and trading less makes each decision count.",
  "startDate": "2026-10-29T19:30:00+01:00", "endDate": "2026-10-29T20:30:00+01:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": {"@type": "VirtualLocation", "url": SITE + "/workshop/"},
  "image": PHOTO, "organizer": {"@id": PERSON_ID}, "performer": {"@id": PERSON_ID},
  "isAccessibleForFree": True,
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
             "url": SITE + "/workshop/", "validFrom": "2026-10-14"}
}

FAQ = [
  ("Is this investment advice?", "No. This is education and coaching. I teach you how to build and follow your own investing framework. I never give buy or sell recommendations for specific securities."),
  ("Who is this program for?", "For people who are already familiar with the financial markets and want to develop the skill of disciplined long-term investing."),
  ("How long does the program last?", "12 months. Real skills take time, so we work together long enough for your system to be tested in real markets."),
  ("How much does it cost?", "Pricing and the founding offer are presented at the free workshop on 29 October."),
  ("Is the coaching online?", "Yes. All sessions take place online, so you can join from anywhere."),
  ("How do I get started?", "Join the free workshop on 29 October. Afterwards you can book a personal intro call."),
]

NAV = [('/workshop/', 'Free workshop'), ('/about/', 'About me'), ('/updates/', 'Market updates'), ('/program/', '12-month program')]

KIT_FORM = '''<div class="signup" id="signup">
        <h3>Reserve your free spot</h3>
        <p class="sub">Thursday 29 October · 19:30 Amsterdam time · Online</p>
        <form action="https://app.kit.com/forms/10043918/subscriptions" class="seva-form formkit-form" method="post" data-sv-form="10043918" data-uid="3d027c31fc" data-format="inline" data-version="5" data-options='{"settings":{"after_subscribe":{"action":"message","success_message":"You’re in! Check your inbox to confirm your spot.","redirect_url":""},"recaptcha":{"enabled":false},"return_visitor":{"action":"show","custom_content":""}},"version":"5"}'>
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
              <span>Reserve my free spot</span>
            </button>
          </div>
        </form>
        <p class="fine">No spam. Unsubscribe anytime. See the <a href="/privacy/">privacy policy</a>.</p>
      </div>'''

CTA_BAND = '''<section class="dark cta-band">
    <div class="wrap">
      <div>
        <p class="eyebrow">Free online workshop · Thursday 29 October</p>
        <h2>Why Great Investors Study More and Trade Less</h2>
        <p>The 20-Decision Rule. 19:30 Amsterdam time, online, about 60 minutes.</p>
      </div>
      <a class="btn light" href="/workshop/">Reserve your free spot</a>
    </div>
  </section>'''

def page(path, title, desc, body, active=None, graph=None, announce=True, kit=False):
    head_ld = ''
    if graph:
        head_ld = '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False) + '\n</script>\n'
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    ann = ('<div class="announce">Free online workshop · Thursday 29 October, 19:30 Amsterdam time · '
           '<a href="/workshop/">Reserve your spot</a></div>\n') if announce else ''
    fnav = ''.join(f'<a href="{h}">{t}</a>' for h, t in [('/', 'Home')] + NAV + [('/privacy/', 'Privacy policy')])
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{PHOTO}">
{head_ld}</head>
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
      <div><strong style="color:var(--ink);font-family:var(--serif);font-size:1.1rem;font-weight:400">Lenny Winnemuller</strong><br>Coaching in long-term investing · Amsterdam<br><a href="mailto:info@lennywinnemuller.com">info@lennywinnemuller.com</a></div>
      <nav class="fnav" aria-label="Footer">{fnav}</nav>
    </div>
    <p class="disclaimer"><strong>Disclaimer:</strong> Lenny Winnemuller provides education and coaching only. Nothing on this website or in the program is investment advice or a recommendation to buy or sell any security. Investing involves risk, including the possible loss of capital. Past results do not guarantee future returns.</p>
    <p>© 2026 Lenny Winnemuller</p>
  </div>
</footer>
{'<script src="https://f.convertkit.com/ckjs/ck.5.js"></script>' if kit else ''}
</body>
</html>
'''
    rel = path.strip('/')
    dest = os.path.join(OUT, rel, 'index.html') if rel else os.path.join(OUT, 'index.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w').write(html)

def load_posts():
    import glob, datetime, markdown, yaml
    posts = []
    for f in glob.glob(os.path.join(HERE, 'content', 'updates', '*.md')):
        raw = open(f, encoding='utf-8').read()
        _, fm, body = raw.split('---', 2)
        m = yaml.safe_load(fm)
        d = m['date']
        if isinstance(d, str):
            d = datetime.date.fromisoformat(d[:10])
        elif isinstance(d, datetime.datetime):
            d = d.date()
        year, week, _ = d.isocalendar()
        m['date'] = d.isoformat()
        m['date_label'] = d.strftime('%A ') + str(d.day) + d.strftime(' %B %Y')
        m['week'] = f'Week {week}, {year}'
        m['title'] = html.escape(str(m['title']).strip())
        m['description'] = html.escape(str(m.get('description', '')).strip())
        m['body'] = markdown.markdown(body, extensions=['extra', 'sane_lists'])
        m['slug'] = os.path.basename(f)[:-3]
        m['path'] = f"/updates/{m['slug']}/"
        posts.append(m)
    posts.sort(key=lambda p: p['date'], reverse=True)
    return posts

POSTS = load_posts()

def post_list(posts):
    if not posts:
        return '<div class="empty"><strong style="color:var(--ink)">The first update is published soon.</strong></div>'
    items = ''.join(f'<li><time datetime="{p["date"]}">{p["week"]} · {p["date_label"]}</time><br><a href="{p["path"]}">{p["title"]}</a><p class="muted" style="margin:6px 0 0">{p["description"]}</p></li>' for p in posts)
    return f'<ul class="post-list">{items}</ul>'

def build_post(p):
    article = {"@type": "BlogPosting", "@id": SITE + p['path'] + "#article", "headline": p['title'],
               "description": p['description'], "datePublished": p['date'], "author": {"@id": PERSON_ID},
               "publisher": {"@id": PERSON_ID}, "isPartOf": {"@id": SITE + "/updates/#blog"},
               "mainEntityOfPage": SITE + p['path'], "inLanguage": "en"}
    body = f'''
  <section class="pagehead">
    <div class="wrap prose">
      <p class="eyebrow"><a href="/updates/" style="color:inherit;text-decoration:none">Market updates</a> · {p['week']}</p>
      <h1>{p['title']}</h1>
      <p class="muted">{p['date_label']} · By <a href="/about/">Lenny Winnemuller</a></p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap prose">
      {p['body']}
      <p class="muted" style="margin-top:2.4em;font-size:.9rem;border-top:1px solid var(--line);padding-top:1.2em">This update is for education only. It is not investment advice or a recommendation to buy, sell or hold any security. Companies are mentioned to illustrate how to think about news, not as opportunities.</p>
      <p><a href="/updates/">← All market updates</a></p>
    </div>
  </section>
  {CTA_BAND}
'''
    page(path=p['path'], title=f"{p['title']} | {p['week']} | Lenny Winnemuller", desc=p['description'],
         body=body, active='/updates/', graph=[article, PERSON])

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in ['styles.css', 'favicon.svg', 'robots.txt', 'llms.txt', '_redirects']:
        shutil.copy(os.path.join(HERE, f), OUT)
    shutil.copytree(os.path.join(HERE, 'admin'), os.path.join(OUT, 'admin'))
    shutil.copytree(os.path.join(HERE, 'static'), OUT, dirs_exist_ok=True)
    paths = []
    for name in ['home', 'program', 'workshop', 'about', 'updates', 'privacy']:
        ns = {}
        exec(open(os.path.join(HERE, 'pages', name + '.py')).read(), {**globals(), 'ns': ns})
        page(**ns['PAGE'])
        paths.append(ns['PAGE']['path'])
    for p in POSTS:
        build_post(p)
        paths.append(p['path'])
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in paths)
    sm += '</urlset>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
    print('built', paths)

if __name__ == '__main__':
    main()
