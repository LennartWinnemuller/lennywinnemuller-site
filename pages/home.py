WORKSHOP_POINTS = '''<ul>
          <li>What the 20-decision rule is, and why fewer, better decisions beat constant activity</li>
          <li>How great long-term investors spend their time: studying, not trading</li>
          <li>How to start making your own investing decisions count</li>
        </ul>'''
body = f'''
  <section class="dark workshop hero-workshop" id="workshop">
    <div class="wrap">
      <div>
        <p class="eyebrow">Free online workshop · Thursday 29 October</p>
        <h1 style="color:#fff">Why Great Investors Study More and Trade Less</h1>
        <p class="subtitle">The 20-Decision Rule</p>
        <p class="when">Thursday 29 October 2026 · 19:30 Amsterdam time
          <small>2:30 pm Toronto · 11:30 am Vancouver · Online · Free · About 60 minutes</small></p>
        <p>In this workshop you'll learn:</p>
        {WORKSHOP_POINTS}
      </div>
      {KIT_FORM}
    </div>
  </section>

  <section id="about">
    <div class="wrap split">
      <div class="photo"><img class="portrait" src="{PHOTO}" alt="Portrait of Lenny Winnemuller" width="400" height="500"></div>
      <div>
        <p class="eyebrow">About me</p>
        <h2>Long-term investing is a skill. I teach it.</h2>
        <p>I'm Lenny Winnemuller, based in Amsterdam. I graduated with honors in psychology from the University of Amsterdam, specializing in group behavior, and also hold a degree in entrepreneurship. I've worked as a professional in the financial markets in the Netherlands and Canada, and today I invest independently.</p>
        <p>I also teach long-term investing in a Canadian trader education program.</p>
        <a class="btn ghost" href="/about/">More about me</a>
      </div>
    </div>
  </section>

  <section class="band" id="updates">
    <div class="wrap">
      <p class="eyebrow">Market updates</p>
      <h2>A weekly note for long-term investors</h2>
      <p class="lead">Every week a short update on what moved the markets and what it means for long-term investors. No tips, no predictions, no advice.</p>
      <div style="margin-top:12px">{post_list(POSTS[:3])}</div>
      <div class="btns" style="margin-top:20px"><a class="btn ghost" href="/updates/">All market updates</a></div>
    </div>
  </section>

  <section id="program">
    <div class="wrap">
      <p class="eyebrow">The 12-month program</p>
      <h2>Build your own long-term investing system in one year</h2>
      <p class="lead">Twelve months of personal coaching in which you build your own system, step by step, and learn to run it on your own.</p>
      <div class="grid four">
        <div class="card"><span class="tag">You walk away with</span><h3>Investment Policy Statement</h3><p>Your rules and principles, rewritten every quarter.</p></div>
        <div class="card"><span class="tag">You walk away with</span><h3>Investment plan</h3><p>How you apply those rules, and how you review them.</p></div>
        <div class="card"><span class="tag">You walk away with</span><h3>Crash plan and selling rules</h3><p>Decided in advance, not in the moment.</p></div>
        <div class="card"><span class="tag">You walk away with</span><h3>Decision journal</h3><p>Every decision you made and why.</p></div>
      </div>
      <div class="btns" style="margin-top:28px"><a class="btn" href="/program/">See the full program</a></div>
    </div>
  </section>
'''
ns['PAGE'] = dict(path='/', title='Lenny Winnemuller | Coaching in Long-Term Investing',
  desc='Free online workshop on 29 October 2026: Why Great Investors Study More and Trade Less. Lenny Winnemuller teaches long-term investing as a skill. Education and coaching, no investment advice.',
  body=body, active=None, graph=[PERSON, EVENT, SERVICE], announce=False, kit=True)
