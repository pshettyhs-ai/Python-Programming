# 📒 Module 12 — APIs and Automation: My Notes

**Started:** Jul 22, 2024
**Finished:** Aug 18, 2024
**Time spent:** ~26 hours

---

## What I learned this module

This module bridged the gap between "Python programs that run and output
text" and "Python programs that DO things in the world" — calling real
APIs, scraping live websites, sending actual emails, generating real PDF
documents. The first time `requests.get()` returned live JSON data from
a real server over the internet felt genuinely different from anything
I'd built before — the program was talking to something outside my own
machine.

### REST APIs

`requests` made HTTP calls far simpler than I expected — vague memories
of a networking course made we worry this would involve raw sockets and
manual header parsing. Building a personal HTTP status code reference
table helped me stop looking codes up constantly. The PUT vs PATCH
distinction (full replace vs partial update) tripped me up initially —
used PUT once with only a partial payload and accidentally wiped fields
I hadn't included.

**Important habit formed:** always set a `timeout` parameter on requests.
Had a script hang indefinitely once on what turned out to be a dead
connection — no timeout meant no way out except killing the process
manually. Now `timeout=5` (or similar) is automatic for me.

### Web Scraping

Fun, but also where I started understanding the ethics/etiquette side of
programming, not just syntax. Learned to check `robots.txt` before
scraping anything, to set a descriptive `User-Agent` header, and to rate
limit myself with `time.sleep()` between requests rather than hammering
a server as fast as possible. Used books.toscrape.com specifically
because it's designed FOR scraping practice rather than scraping a real
production site without permission.

Hit `AttributeError: 'NoneType' object has no attribute 'text'`
repeatedly when a page's structure didn't match my assumptions (missing
element, different page than expected). Now I always check `if element:`
before accessing `.text` or attributes on anything `find()` returns,
since `find()` returns `None` rather than raising an exception when
nothing matches.

Pagination took the longest to get right — my first attempt hardcoded
URL patterns assuming page 1 and page 2+ followed the same format. They
didn't (page 1 was the root URL, page 2+ had a different path pattern).
Fixed by reading the actual "next page" link FROM the page itself instead
of guessing the URL structure.

### Email Automation

Surprisingly the most frustrating sub-module, not because of Python but
because of Gmail's security model. Regular password authentication
doesn't work for SMTP anymore when 2-factor authentication is enabled —
needed to generate a dedicated "App Password" specifically for SMTP
access. Got `SMTPAuthenticationError` repeatedly before finding this out,
genuinely thought my code was broken when it was actually a Google
account settings issue.

**Real near-miss:** hardcoded my actual email and app password directly
in the script during initial testing. Caught myself before committing to
git, but it was close enough to scare me into permanently adopting
environment variables (`os.environ.get(...)`) plus a `.gitignore` entry
for any credentials file, as a non-negotiable habit for every project
going forward, not just this one.

### PDF Automation

Learned there are two distinct jobs needing two distinct libraries:
`reportlab` CREATES PDFs from scratch (drawing text/shapes onto a blank
canvas), `pypdf` MANIPULATES existing PDFs (merging, splitting, reading
text, adding metadata). Confused this for an afternoon trying to use
reportlab to merge existing files, which it's not designed for.

`reportlab`'s coordinate system genuinely confused me — (0,0) is the
BOTTOM-LEFT of the page, not top-left like screen/image coordinates I was
used to from other contexts. Spent a while wondering why my "header" text
kept rendering at the bottom of the page until I realized I needed
`height - some_value` for the y-position, not just `some_value` directly.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| Script hung indefinitely | requests.get() with no timeout, dead connection | Added timeout=5 (or similar) to all requests |
| PUT wiped unintended fields | Sent partial payload with PUT, expecting partial update | Learned PUT = full replace, PATCH = partial update |
| AttributeError on scraped data | find() returned None, called .text on it directly | Added `if element:` checks before accessing attributes |
| Hardcoded pagination URLs broke | Assumed consistent URL pattern across all pages | Read 'next page' link dynamically from the page itself |
| SMTPAuthenticationError | Used regular Gmail password with 2FA enabled | Generated and used a Google App Password instead |
| Nearly committed credentials | Hardcoded email/password during testing | Switched to environment variables + .gitignore |
| PDF text rendered at wrong position | Assumed (0,0) was top-left like screen coords | Learned reportlab uses bottom-left origin; used height - y |
| Confused reportlab and pypdf roles | Tried to merge PDFs using reportlab | Learned reportlab=create, pypdf=manipulate existing files |

---

## Lessons learned after this module

- Always set timeouts on network requests — no exceptions
- Check robots.txt and rate-limit scraping — be a respectful bot
- Never trust find()/select() results blindly — check for None first
- Credentials NEVER go in source code — environment variables, always
- reportlab creates, pypdf manipulates — different tools for different jobs
- reportlab's coordinate origin is bottom-left, not top-left

This module connected directly to why I started learning Python in the
first place — automating things and talking to APIs feels directly
relevant to IoT/embedded work I want to do eventually (sensor data
pipelines, remote device communication).

Next up: Data Structures & Algorithms — implementing the classics
(linked lists, stacks, queues, trees, graphs, sorting, searching) from
scratch instead of just using Python's built-in list/dict for everything.
