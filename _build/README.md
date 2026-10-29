# FZ Consultation — site generator

The site's HTML pages are generated. Don't edit the files in `fr/` or `en/` by hand; edit the content here and rebuild.

## Content files
- `content.py` — expertise, services, methodology, FAQ
- `industries.py` — industry pages and example engagements
- `cases.py` — case studies (public sources only)
- `downtime.py` — cost-of-downtime benchmarks, incidents and sources
- `tools.py` — templates (including the AI agent audit scorecard), calculator labels, glossary
- `insights.py` — Insights articles (add one entry, rebuild: the RSS feeds update by themselves)
- `partners.py`, `ai.py`, `auditor.py`, `newcontent.py` — partners, AI services and Auditor, self-assessment questions
- `extras.py` — resources hub, calculator, templates, glossary, insights, search, security, accessibility, governance pages
- `build.py` — layout, contact, legal pages, CONFIG block (booking link, Formspree ID, analytics token, `UPDATED`, `REVIEWED`, `SECURITY_EXPIRES`)
- `make_docs.py` — generates the eight Word templates in `assets/downloads/`

## Rebuild (Python 3.10+, `pip install -r _build/requirements.txt`)

    python3 _build/build.py                                   # pages, feeds, sitemap, security.txt, Word templates
    npx pagefind --site . --glob "{fr,en}/**/*.html"          # search index (re-run after every build)
    python3 _build/check.py                                   # links, anchors, metadata, CSP, JSON-LD, security.txt
    python3 _build/audit.py                                   # axe accessibility (light+dark), console + CSP errors, phone overflow
                                                              # needs: npm install axe-core ; playwright install chromium

Commit the regenerated files (including `pagefind/`). GitHub Pages does not publish folders starting with `_`, so this folder stays out of the public site.

## Things to remember
- `SECURITY_EXPIRES` in `build.py`: renew `security.txt` at least once a year (check.py warns 45 days before).
- `REVIEWED` in `build.py`: add a page's path and date only after re-checking its sources; the date is then shown under the title.
- Every new page must go through `page()` so it gets the CSP, structured data and search attributes.
- No inline `<script>` blocks: the Content-Security-Policy forbids them. Data for scripts goes in `<script type="application/json">`.
- See `GOVERNANCE.md` for review, privacy-register and account-security routines.
