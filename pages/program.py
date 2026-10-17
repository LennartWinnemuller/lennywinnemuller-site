faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>\n      ' for q, a in FAQ)
faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
body = f'''
  <section class="pagehead">
    <div class="wrap">
      <p class="eyebrow">The 12-month program</p>
      <h1>Build your own long-term investing system in one year</h1>
      <p class="lead">Long-term investing is a skill, not a tip. In twelve months of personal coaching you build your own system, step by step, and learn to run it on your own.</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2>What you'll walk away with</h2>
      <div class="grid four">
        <div class="card"><h3>Investment Policy Statement</h3><p>Your personal rules and principles, written down and rewritten every quarter as your skill grows.</p></div>
        <div class="card"><h3>Investment plan</h3><p>How you apply those rules: your allocation, your process and how you review it.</p></div>
        <div class="card"><h3>Crash plan and selling rules</h3><p>What you do when markets fall, and when you sell, decided in advance and not in the moment.</p></div>
        <div class="card"><h3>Decision journal</h3><p>A record of every decision you made and why, so you learn from your own choices.</p></div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2>How we work</h2>
      <div class="grid">
        <div class="card"><h3>A paper portfolio from week 1</h3><p>You practice real decisions from the start, without risking money. It's about the quality of your decisions, not returns.</p></div>
        <div class="card"><h3>Weekly and monthly assignments</h3><p>Every week you do something concrete, so the skill builds steadily.</p></div>
        <div class="card"><h3>Valuation and thesis defense</h3><p>You learn how to value businesses and how to defend your investment theses.</p></div>
        <div class="card"><h3>1:1 coaching</h3><p>Regular personal sessions and quarterly reviews, with support in between.</p></div>
        <div class="card"><h3>Education, not advice</h3><p>I teach you how to make your own decisions. I never tell you what to buy or sell.</p></div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2>The year at a glance</h2>
      <div class="quarters">
        <div class="quarter"><span class="q">Months 1–3</span><h3>Foundation</h3><ul><li>Your investor identity</li><li>Why long-term investing works</li><li>The playing field</li></ul></div>
        <div class="quarter"><span class="q">Months 4–6</span><h3>Understanding businesses</h3><ul><li>Recognising a quality business</li><li>Reading an annual report</li><li>Competitive advantage and management</li></ul></div>
        <div class="quarter"><span class="q">Months 7–9</span><h3>Valuation and portfolio</h3><ul><li>Valuation</li><li>Your research process</li><li>Building a portfolio</li></ul></div>
        <div class="quarter"><span class="q">Months 10–12</span><h3>Behaviour and independence</h3><ul><li>Investor psychology</li><li>Crashes, patience and selling</li><li>Your investment plan</li></ul></div>
      </div>
      <p class="muted" style="margin-top:20px">Every quarter ends with a review, and you rewrite your Investment Policy Statement.</p>
    </div>
  </section>

  <section class="faq">
    <div class="wrap narrow">
      <h2>Frequently asked questions</h2>
      {faq_html}
    </div>
  </section>

  <section class="dark cta-band">
    <div class="wrap">
      <div>
        <p class="eyebrow">Places are limited</p>
        <h2>Pricing and the founding offer</h2>
        <p>Both are presented at the free workshop on Thursday 29 October.</p>
      </div>
      <a class="btn light" href="/workshop/">Join the free workshop</a>
    </div>
  </section>
'''
ns['PAGE'] = dict(path='/program/', title='12-Month Coaching Program in Long-Term Investing | Lenny Winnemuller',
  desc='A 12-month coaching program in which you build your own long-term investing system: an Investment Policy Statement, investment plan, crash plan and decision journal. Education, no investment advice.',
  body=body, active='/program/', graph=[SERVICE, faq_ld, PERSON])
