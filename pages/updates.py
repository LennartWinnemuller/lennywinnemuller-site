body = f'''
  <section class="pagehead">
    <div class="wrap narrow">
      <p class="eyebrow">Market updates</p>
      <h1>A weekly note for long-term investors</h1>
      <p class="lead">Every week a short update: what moved the markets and what it means for long-term investors. No tips, no predictions, no advice.</p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap narrow">
      {post_list(POSTS)}
    </div>
  </section>
  {CTA_BAND}
'''
ns['PAGE'] = dict(path='/updates/', title='Weekly Market Updates for Long-Term Investors | Lenny Winnemuller',
  desc='A weekly note for long-term investors by Lenny Winnemuller: what moved the markets and what it means for long-term investors. No tips, no advice.',
  body=body, active='/updates/', graph=[{"@type": "Blog", "@id": SITE + "/updates/#blog", "name": "Weekly Market Updates", "url": SITE + "/updates/", "author": {"@id": PERSON_ID}, "inLanguage": "en"}, PERSON])
