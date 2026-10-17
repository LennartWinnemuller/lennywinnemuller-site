body = f'''
  <section class="dark workshop">
    <div class="wrap">
      <div>
        <p class="eyebrow">Free online workshop · Thursday 29 October</p>
        <h1 style="color:#fff">Why Great Investors Study More and Trade Less</h1>
        <p class="subtitle">The 20-Decision Rule</p>
        <p class="when">Thursday 29 October 2026 · 19:30 Amsterdam time
          <small>2:30 pm Toronto · 11:30 am Vancouver · Online · Free · About 60 minutes</small></p>
        <p>In this workshop you'll learn:</p>
        <ul>
          <li>What the 20-decision rule is, and why fewer, better decisions beat constant activity</li>
          <li>How great long-term investors spend their time: studying, not trading</li>
          <li>How to start making your own investing decisions count</li>
        </ul>
      </div>
      {KIT_FORM}
    </div>
  </section>

  <section>
    <div class="wrap narrow">
      <h2>Who this workshop is for</h2>
      <ul class="checklist">
        <li>You follow the markets every day, but you don't have a clear plan for your long-term wealth.</li>
        <li>You set rules for yourself, and then you break them when the market gets loud.</li>
        <li>You've collected strategies, opinions and tips, but none of it adds up to a system that's yours.</li>
      </ul>
      <p>After you sign up, you get an email to confirm your spot. The link to join arrives in that email.</p>
      <p class="muted">Hosted by <a href="/about/">Lenny Winnemuller</a>. Education only, no investment advice.</p>
    </div>
  </section>
'''
ns['PAGE'] = dict(path='/workshop/', title='Free Workshop: Why Great Investors Study More and Trade Less | Lenny Winnemuller',
  desc='Free online workshop on Thursday 29 October 2026, 19:30 Amsterdam time: Why Great Investors Study More and Trade Less, the 20-Decision Rule.',
  body=body, active='/workshop/', graph=[EVENT, PERSON], announce=False, kit=True)
