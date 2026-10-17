body = f'''
  <section class="pagehead">
    <div class="wrap split">
      <div class="photo"><img class="portrait" src="{PHOTO}" alt="Portrait of Lenny Winnemuller" width="400" height="500"></div>
      <div>
        <p class="eyebrow">About me</p>
        <h1>Lenny Winnemuller</h1>
        <p>I'm Lenny Winnemuller, based in Amsterdam. I graduated with honors in psychology from the University of Amsterdam, specializing in group behavior, and also hold a degree in entrepreneurship. I've worked as a professional in the financial markets in the Netherlands and Canada, and today I invest independently.</p>
        <p>I also teach long-term investing in a Canadian trader education program, where I help students build the discipline and frameworks that long-term investing requires.</p>
        <p>My mission is simple: to improve financial education and help people master the skill of long-term investing.</p>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap narrow">
      <h2>Why I teach investing as a skill</h2>
      <p>Long-term investing isn't about finding the next big idea. It's a skill: making good decisions, consistently, for years. Like any skill, it can be learned. It takes the right method, deliberate practice and someone who gives you honest feedback along the way.</p>
      <p>That's why I never give tips or tell anyone what to buy. I teach you how to make your own well-founded decisions, so you never depend on anyone else's opinion again.</p>
    </div>
  </section>

  {CTA_BAND}
'''
ns['PAGE'] = dict(path='/about/', title='About Lenny Winnemuller | Long-Term Investing Coach',
  desc='Lenny Winnemuller is an Amsterdam-based coach who teaches long-term investing as a skill. Psychology graduate (honors, University of Amsterdam), worked in the financial markets in the Netherlands and Canada.',
  body=body, active='/about/', graph=[PERSON])
