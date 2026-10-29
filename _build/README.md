# FZ Consultation — site generator

The site's HTML pages are generated. Don't edit the files in `fr/` or `en/` by hand; edit the content here and rebuild.

## Content files
- `content.py` — expertise, services, methodology, FAQ
- `industries.py` — industry pages and example engagements
- `cases.py` — case studies (public sources only)
- `downtime.py` — cost-of-downtime benchmarks, incidents and sources
- `tools.py` — templates (ransomware checklist, RTO/RPO worksheet, AI policy), calculator labels, glossary
- `insights.py` — Insights articles (add one entry, rebuild: the RSS feeds update by themselves)
- `partners.py`, `ai.py`, `newcontent.py` — partners, AI section, self-assessment questions
- `extras.py` — resources hub, calculator, templates, glossary, insights, search, security, accessibility, governance pages
- `build.py` — layout, contact, legal pages, CONFIG block (booking link, Formspree ID, analytics token, `UPDATED`, `REVIEWED`, `SECURITY_EXPIRES`)
- `make_docs.py` — generates the six Word templates in `assets/downloads/`

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

## Structure (October 2026 restructure)

- 40 pages per language (was 58). Old URLs are kept as `noindex` redirect stubs, generated from `REMAP` in `newsite_content.py` (old path → new path#anchor). `rewrite_links` updates internal links; add an entry to `REMAP` whenever you retire a page.
- `newsite.py` builds the home (entry points), case studies (the centrepiece), What we do, sector and AI hubs, and the contextual call to action. The CTA is chosen from the `CTX` table in `newsite_content.py` by page path (exact or prefix); the contact form is prefilled with `?topic=<key>`.
- `cases_extra.py` holds each case's one-line takeaway and "Monday" checks, plus the three newer cases. Use only sources you have read; attribute anything a company has not confirmed.
- EU AI Act dates live in `AI_EU` (`newsite_content.py`) and the `REG` entry in `build.py`; update both when the dates change, and log it in the governance corrections list in `extras.py`.

## Monthly note: "What this outage teaches"

Add one dict to `NOTES` in `notes.py` each month (copy issue 1): slug, `series: True`, `issue`, date, title, summary, then body blocks: `facts`, `h`, `p`, `ul`, `check`, `src`. Rules: quote the company's own words, attribute press claims, never state that a named company depended on a failed component unless it said so. Then rebuild, run `check.py` and pagefind.
