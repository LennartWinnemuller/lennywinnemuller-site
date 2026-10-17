# lennywinnemuller.com

Static site for Lenny Winnemuller, hosted on Netlify. Netlify runs `python3 build.py` on every push and publishes `public/`.

Everything is editable in the editor at https://lennywinnemuller.com/admin:

- **Market updates:** saved as Markdown in `content/updates/`.
- **Pages** (homepage, workshop, about, market updates page, program, site settings): saved as JSON in `content/pages/`. Field names must match `admin/config.yml`.
- **Photos:** uploaded to `static/images/`, served at `/images/`.

Layout, shared header and footer, workshop form and structured data live in `build.py`; the privacy policy in `pages/privacy.py`; styling in `styles.css`.

Local build: `python3 build.py` (no dependencies), then open `public/`.
