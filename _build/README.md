# FZ Consultation — site generator

The site's HTML pages are generated. Don't edit the files in `fr/` or `en/` by hand; edit the content here and rebuild.

- `content.py` — expertise, services, methodology, FAQ
- `industries.py` — industry pages and example engagements
- `cases.py` — case studies (public sources only)
- `partners.py` — ecosystem and partnerships page
- `ai.py` — AI pages, Microsoft Foundry Citadel page, vision questionnaire
- `newcontent.py` — resilience self-assessment questions
- `build.py` — layout, contact, legal pages, and the CONFIG block (booking link, Formspree ID, analytics token)

Rebuild (Python 3.10+), from this folder:

    python3 build.py

This regenerates `fr/`, `en/`, `index.html`, `404.html`, `sitemap.xml`, `robots.txt` and `CNAME` one level up.
GitHub Pages does not publish folders starting with `_`, so this folder stays out of the public site.
