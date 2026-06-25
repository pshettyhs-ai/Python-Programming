# =============================================================================
# WebScraping.py
# Author  : Pavan Shetty H S
# Date    : August 2024
# Topic   : Web Scraping with requests + BeautifulSoup
# =============================================================================
#
# Notes from Pavan:
# Web scraping is genuinely fun but also where I started learning about
# WHY some websites actively block scrapers (rate limiting, robots.txt,
# changing HTML structure to break scrapers). Built this with a basic
# practice site (books.toscrape.com, designed specifically FOR scraping
# practice) rather than scraping a real production site without
# permission.
# =============================================================================

import requests
from bs4 import BeautifulSoup
import time

print("=" * 50)
print("    WEB SCRAPING DEMO")
print("=" * 50)

# ---------------------
# Always check robots.txt and terms of service first
# ---------------------
print("\n[1] Checking robots.txt before scraping ANYTHING")
print("  This is a habit I built early -- robots.txt tells you what a")
print("  site owner is okay with bots crawling. Respecting it matters")
print("  even when not legally binding.")
robots_response = requests.get("https://books.toscrape.com/robots.txt")
print(f"  robots.txt content preview: {robots_response.text[:100]}")

# ---------------------
# Fetching and parsing HTML
# ---------------------
print("\n[2] Fetching a page and parsing with BeautifulSoup")
url = "https://books.toscrape.com/"
headers = {"User-Agent": "PavanPythonLearning/1.0 (learning purposes)"}
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, "html.parser")

print(f"  Status: {response.status_code}")
print(f"  Page title: {soup.title.string}")

# ---------------------
# Finding elements -- find() vs find_all()
# ---------------------
print("\n[3] find() vs find_all()")
first_book = soup.find("article", class_="product_pod")
print(f"  First book element found: {first_book is not None}")

all_books = soup.find_all("article", class_="product_pod")
print(f"  Total books found on page: {len(all_books)}")

# ---------------------
# Extracting specific data -- title, price, availability
# ---------------------
print("\n[4] Extracting structured data from each book")
book_list = []
for book in all_books[:5]:   # just first 5 for demo
    title = book.h3.a["title"]   # title is in the 'title' attribute, not text!
    price = book.find("p", class_="price_color").text
    availability = book.find("p", class_="instock availability").text.strip()
    rating_class = book.find("p", class_="star-rating")["class"]
    rating = rating_class[1]   # second class is the rating word, e.g. "Three"

    book_list.append({
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating
    })

for b in book_list:
    print(f"  {b['title'][:40]:40} | {b['price']:8} | {b['availability']:15} | Rating: {b['rating']}")

# ---------------------
# Using CSS selectors -- select() method (alternative to find_all)
# ---------------------
print("\n[5] Using select() with CSS selectors")
prices = soup.select("p.price_color")
print(f"  Found {len(prices)} prices using CSS selector")
print(f"  First 3 prices: {[p.text for p in prices[:3]]}")

# ---------------------
# Following pagination -- the part that took longest to get right
# ---------------------
print("\n[6] Handling pagination (scraping multiple pages)")
print("  My first attempt hardcoded page URLs and broke on page 2 because")
print("  the URL pattern actually CHANGES between page 1 and later pages")
print("  (page 1 is just '/' but page 2+ is '/catalogue/page-2.html').")
print("  Fixed by reading the 'next' link from the page itself instead of")
print("  guessing the URL pattern.")

next_link = soup.find("li", class_="next")
if next_link:
    next_url = url + next_link.a["href"]
    print(f"  Next page URL found dynamically: {next_url}")

# ---------------------
# Being a respectful scraper -- rate limiting myself
# ---------------------
print("\n[7] Rate limiting -- being respectful to the server")
print("  Adding time.sleep() between requests to avoid hammering the server.")
print("  Example pattern I use for multi-page scraping:")
print("""
  for page_num in range(1, 4):
      response = requests.get(page_url, headers=headers)
      # ... process page ...
      time.sleep(1)   # be polite, don't spam requests
""")

# ---------------------
# Handling missing elements gracefully
# ---------------------
print("[8] Handling missing elements without crashing")
fake_soup = BeautifulSoup("<div>No book data here</div>", "html.parser")
missing_title = fake_soup.find("h3")
print(f"  fake_soup.find('h3') = {missing_title}")
if missing_title is None:
    print("  Correctly handled missing element -- returned None, didn't crash")
    print("  Lesson: ALWAYS check for None before calling .text on a find()")
    print("  result, or you'll get AttributeError: 'NoneType' object has")
    print("  no attribute 'text' -- hit this constantly early on.")

print("\n" + "=" * 50)

# =============================================================================
# Debugging note: Got AttributeError: 'NoneType' object has no attribute
# 'text' repeatedly when a page's structure didn't match what I expected
# (missing element). Now I always check `if element:` before accessing
# .text or attributes on anything returned by find().
# =============================================================================

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 WebScraping.py
# =============================================================================
#
# NOTE: This sandboxed execution environment blocks outbound HTTP
# requests to hosts outside an allowlist -- an egress proxy returns an
# HTTP 403 with a plain-text 'Host not in allowlist' body instead of the
# real books.toscrape.com page. BeautifulSoup parses that plain text and
# finds no <title> tag, so soup.title is None, and soup.title.string
# raises an uncaught AttributeError, ending the script there. This is an
# environment restriction, not a bug in the script -- with real internet
# access this would proceed to parse and print real book listings.
#
# ==================================================
#     WEB SCRAPING DEMO
# ==================================================
#
# [1] Checking robots.txt before scraping ANYTHING
#   This is a habit I built early -- robots.txt tells you what a
#   site owner is okay with bots crawling. Respecting it matters
#   even when not legally binding.
#   robots.txt content preview: Host not in allowlist: books.toscrape.com. Add this host to your network egress settings to allow ac
#
# [2] Fetching a page and parsing with BeautifulSoup
#   Status: 403
# Traceback (most recent call last):
#   File "/tmp/tmp.C3nQ8TIeIB/WebScraping.py", line 45, in <module>
#     print(f"  Page title: {soup.title.string}")
#                            ^^^^^^^^^^^^^^^^^
# AttributeError: 'NoneType' object has no attribute 'string'
#
# [Process exited with status 1]
#
# =============================================================================

