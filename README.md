# lennywinnemuller.com

Static site for Lenny Winnemuller, hosted on Netlify. Netlify runs `python3 build.py` on every push and publishes `public/`.

- **Market updates:** written in the editor at https://lennywinnemuller.com/admin, saved as Markdown in `content/updates/`.
- **Page texts:** `pages/*.py`. Shared header, footer, workshop form and structured data: `build.py`.
- **Styling:** `styles.css`.

Local build: `pip install -r requirements.txt && python3 build.py`, then open `public/`.
