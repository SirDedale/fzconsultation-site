# Governance routines — FZ Consultation website

Owner: Fabien Mariou. Keep this file private (the `_build/` folder is not published by GitHub Pages).

## 1. Calendar
| When | What | How |
|---|---|---|
| Monthly (automatic) | Dead external links, expiring `security.txt` | GitHub Action "Site checks" runs `linkcheck_external.py` and `check.py`; read the run summary |
| Each change | Build is in sync, no broken links, accessibility, CSP | The same Action on every push and pull request |
| Quarterly | Account-security review (section 2); purge of old contacts (section 4) | Tick the checklists below, note the date |
| Every 6 months | Review the cost-of-downtime and regulation pages; re-check sources | Update `downtime.py` / `content.py`, then add the date to `REVIEWED` in `build.py` |
| Yearly | Review every page; renew `SECURITY_EXPIRES`; re-read privacy and accessibility pages; rotate/validate DKIM keys | Rebuild, run checks, commit |

## 2. Account-security checklist (tick each quarter)
- [ ] GitHub: two-factor authentication on with a passkey or hardware key; recovery codes stored offline
- [ ] GitHub: branch protection on `main` (require pull request or at least require the "Site checks" status); no unused collaborators, tokens or deploy keys
- [ ] GitHub: Actions permissions are read-only by default; Dependabot updates reviewed
- [ ] Namecheap: two-factor authentication on; domain lock on; auto-renew on; DNSSEC still enabled; WHOIS privacy on
- [ ] Namecheap Private Email: strong unique password; two-factor if offered; mailbox forwarding rules checked
- [ ] DNS: SPF, DKIM and DMARC records present (DMARC: start at `p=none` with a `rua` address, move to `quarantine` then `reject` once reports are clean)
- [ ] Formspree: two-factor on; notification email is correct; spam filter on; submission retention reviewed
- [ ] Calendly and Cloudflare: two-factor on; no unknown members
- [ ] Password manager in use; recovery methods up to date; backup copy of the repository outside GitHub (e.g. `git clone --mirror` to an encrypted drive)

## 3. Privacy register (processing of personal information)
| Activity | Data | Where | Basis | Retention |
|---|---|---|---|---|
| Contact form | name, email, organization, message | Formspree, then Namecheap mailbox | consent / legitimate interest | 3 years after last contact |
| Email | sender details, content | Namecheap Private Email | legitimate interest | 3 years after last contact |
| Booking | name, email, chosen slot | Calendly | consent | per Calendly settings; delete with contact |
| Analytics | aggregate page views, no cookies | Cloudflare Web Analytics | legitimate interest | per Cloudflare |
| Hosting | IP address in server logs | GitHub Pages | legitimate interest / security | per GitHub |
| Self-assessment, AI questionnaire, calculator, search, theme/language | answers and preferences | the visitor's browser only | n/a | not transmitted |

Review this table whenever a tool is added or removed, then update `privacy.html` text in `build.py` and the "Third-party services" table in `extras.py` (security page). Law 25 (Quebec) also expects an incident register: keep a simple log of any privacy incident, even minor, with date, what happened, and the decision on notification.

## 4. Deletion routine (quarterly)
1. Search the mailbox, Formspree submissions and Calendly for contacts with no activity for 3 years.
2. Delete them, unless a client relationship or legal obligation requires keeping them.
3. Answer access/deletion requests received by email within 30 days; log the request, date and action.
4. Note the date and the number of deletions here: ____________

## 5. Corrections
Reports go to the contact address. Verify against the cited source, fix in the content file, rebuild, and add a line to the corrections log in `extras.py` (`build_governance`) for any substantive change.

## 6. Known limitations to be aware of
- GitHub Pages cannot set HTTP response headers. The Content-Security-Policy is delivered through a `<meta>` tag, which does not support `frame-ancestors` (clickjacking protection) and cannot enforce `report-uri`. Putting the site behind Cloudflare's proxy would allow real headers (HSTS, frame-ancestors, referrer policy) if that matters later.
- Accessibility has only been verified with automated tooling (axe-core) and keyboard walkthroughs by script. Commission a manual review with screen-reader users before claiming conformance publicly.
- External source links may be blocked for automated checkers (403/429); the monthly job lists them as "review by hand".
- The Word templates are generated, not hand-checked with Office's accessibility checker.
