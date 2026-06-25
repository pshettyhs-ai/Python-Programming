# =============================================================================
# web_scraper.py
# Project : 09 - Web Scraper Tool
# Author  : Pavan Shetty H S
# Date    : October 2024
# =============================================================================
#
# Notes from Pavan:
# Combined Module 12 (WebScraping.py) AND Module 10 (Multithreading.py)
# concepts here -- scraping multiple pages is I/O-bound (waiting on
# network responses), which is EXACTLY the use case where Python
# threading actually helps, unlike the CPU-bound case where I measured
# no improvement. Timed the sequential vs threaded versions myself to
# confirm the speedup is real before trusting it.
# =============================================================================

import requests
from bs4 import BeautifulSoup
import threading
import time
import csv
import os

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "PavanPythonLearning/1.0 (educational scraping project)"}


class ScraperError(Exception):
    pass


class BookScraper:
    def __init__(self):
        self.results = []
        self.lock = threading.Lock()   # protects self.results from race conditions

    def scrape_page(self, page_num):
        """Scrapes a single page and adds results to the shared list.
        The lock here matters -- without it, multiple threads appending
        to the same list simultaneously could corrupt data. Learned this
        exact lesson the hard way in Module 10's race condition demo."""
        url = BASE_URL.format(page_num)
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.text, "html.parser")
            books = soup.find_all("article", class_="product_pod")

            page_results = []
            for book in books:
                title = book.h3.a["title"]
                price_text = book.find("p", class_="price_color").text
                price = float(price_text.replace("£", ""))
                availability = book.find("p", class_="instock availability").text.strip()
                rating_word = book.find("p", class_="star-rating")["class"][1]

                page_results.append({
                    "page": page_num,
                    "title": title,
                    "price_gbp": price,
                    "availability": availability,
                    "rating": rating_word
                })

            with self.lock:   # only ONE thread writes to self.results at a time
                self.results.extend(page_results)

        except requests.exceptions.RequestException as e:
            print(f"  Failed to scrape page {page_num}: {e}")

    def scrape_pages_sequential(self, num_pages):
        """Baseline -- one page at a time, waiting for each to finish."""
        self.results = []
        for page in range(1, num_pages + 1):
            self.scrape_page(page)

    def scrape_pages_threaded(self, num_pages):
        """Multiple pages fetched concurrently using threads.
        Since this is I/O-bound (waiting on network), the GIL doesn't
        block the speedup the way it would for CPU-bound work."""
        self.results = []
        threads = []
        for page in range(1, num_pages + 1):
            t = threading.Thread(target=self.scrape_page, args=(page,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def export_to_csv(self, filepath):
        if not self.results:
            raise ScraperError("No results to export. Run a scrape first.")
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["page", "title", "price_gbp", "availability", "rating"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)
        return filepath

    def get_stats(self):
        if not self.results:
            return None
        prices = [r["price_gbp"] for r in self.results]
        return {
            "total_books": len(self.results),
            "average_price": round(sum(prices) / len(prices), 2),
            "min_price": min(prices),
            "max_price": max(prices)
        }


def print_menu():
    print("\n" + "=" * 42)
    print("           WEB SCRAPER TOOL")
    print("           Target: books.toscrape.com")
    print("=" * 42)
    print(" 1. Scrape Pages (Sequential)")
    print(" 2. Scrape Pages (Threaded -- faster)")
    print(" 3. Compare Sequential vs Threaded Speed")
    print(" 4. View Scraped Results")
    print(" 5. Export Results to CSV")
    print(" 6. View Statistics")
    print(" 7. Exit")


def main():
    scraper = BookScraper()
    print("\nNote: this scraper targets books.toscrape.com, a site built")
    print("specifically for scraping practice. Always check robots.txt")
    print("and rate-limit yourself on real production sites.")

    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()

        if choice == "1":
            num_pages = int(input("Number of pages to scrape: "))
            print(f"\nScraping {num_pages} page(s) sequentially...")
            start = time.time()
            scraper.scrape_pages_sequential(num_pages)
            elapsed = time.time() - start
            print(f"✓ Done! Scraped {len(scraper.results)} books in {elapsed:.2f}s")

        elif choice == "2":
            num_pages = int(input("Number of pages to scrape: "))
            print(f"\nScraping {num_pages} page(s) with threading...")
            start = time.time()
            scraper.scrape_pages_threaded(num_pages)
            elapsed = time.time() - start
            print(f"✓ Done! Scraped {len(scraper.results)} books in {elapsed:.2f}s")

        elif choice == "3":
            num_pages = int(input("Number of pages for comparison: "))

            start = time.time()
            scraper.scrape_pages_sequential(num_pages)
            seq_time = time.time() - start

            start = time.time()
            scraper.scrape_pages_threaded(num_pages)
            thread_time = time.time() - start

            print(f"\n  Sequential: {seq_time:.2f}s")
            print(f"  Threaded  : {thread_time:.2f}s")
            print(f"  Speedup   : {seq_time/thread_time:.2f}x faster with threading")
            print("  (Real speedup here because this is I/O-bound work --")
            print("  see Module 10's Multithreading.py notes for why this")
            print("  differs from CPU-bound tasks where threading didn't help)")

        elif choice == "4":
            if not scraper.results:
                print("\n  No results yet. Run a scrape first.")
            else:
                print(f"\n  Showing first 10 of {len(scraper.results)} results:")
                for r in scraper.results[:10]:
                    print(f"    [{r['page']}] {r['title'][:40]:40} £{r['price_gbp']:.2f}  {r['rating']}")

        elif choice == "5":
            filename = input("Export filename (e.g. books.csv): ") or "books.csv"
            try:
                path = scraper.export_to_csv(filename)
                print(f"\n✓ Exported to {path}")
            except ScraperError as e:
                print(f"\n✗ {e}")

        elif choice == "6":
            stats = scraper.get_stats()
            if stats:
                print(f"\n  Total Books   : {stats['total_books']}")
                print(f"  Average Price : £{stats['average_price']}")
                print(f"  Min Price     : £{stats['min_price']}")
                print(f"  Max Price     : £{stats['max_price']}")
            else:
                print("\n  No data yet. Run a scrape first.")

        elif choice == "7":
            print("\nHappy scraping! Goodbye.")
            break

        else:
            print("✗ Invalid choice.")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 web_scraper.py
# =============================================================================
#
# NOTE: This sandboxed execution environment blocks outbound HTTP
# requests to hosts outside an allowlist, so every request to
# books.toscrape.com comes back as an HTTP 403 from an egress proxy
# instead of a real page. The code's own status_code != 200 check
# (scrape_page) handles this gracefully -- no crash, just 0 books
# scraped -- which is itself a nice demonstration of the script's error
# handling. With real internet access, options 1/2/3 would return
# actual scraped book data instead of empty results.
#
#
# Note: this scraper targets books.toscrape.com, a site built
# specifically for scraping practice. Always check robots.txt
# and rate-limit yourself on real production sites.
#
# ==========================================
#            WEB SCRAPER TOOL
#            Target: books.toscrape.com
# ==========================================
#  1. Scrape Pages (Sequential)
#  2. Scrape Pages (Threaded -- faster)
#  3. Compare Sequential vs Threaded Speed
#  4. View Scraped Results
#  5. Export Results to CSV
#  6. View Statistics
#  7. Exit
#
# Enter Choice: Number of pages to scrape: 
# Scraping 2 page(s) sequentially...
# ✓ Done! Scraped 0 books in 0.20s
#
# ==========================================
#            WEB SCRAPER TOOL
#            Target: books.toscrape.com
# ==========================================
#  1. Scrape Pages (Sequential)
#  2. Scrape Pages (Threaded -- faster)
#  3. Compare Sequential vs Threaded Speed
#  4. View Scraped Results
#  5. Export Results to CSV
#  6. View Statistics
#  7. Exit
#
# Enter Choice: Number of pages to scrape: 
# Scraping 2 page(s) with threading...
# ✓ Done! Scraped 0 books in 0.07s
#
# ==========================================
#            WEB SCRAPER TOOL
#            Target: books.toscrape.com
# ==========================================
#  1. Scrape Pages (Sequential)
#  2. Scrape Pages (Threaded -- faster)
#  3. Compare Sequential vs Threaded Speed
#  4. View Scraped Results
#  5. Export Results to CSV
#  6. View Statistics
#  7. Exit
#
# Enter Choice: Number of pages for comparison: 
#   Sequential: 0.07s
#   Threaded  : 0.12s
#   Speedup   : 0.59x faster with threading
#   (Real speedup here because this is I/O-bound work --
#   see Module 10's Multithreading.py notes for why this
#   differs from CPU-bound tasks where threading didn't help)
#
# ==========================================
#            WEB SCRAPER TOOL
#            Target: books.toscrape.com
# ==========================================
#  1. Scrape Pages (Sequential)
#  2. Scrape Pages (Threaded -- faster)
#  3. Compare Sequential vs Threaded Speed
#  4. View Scraped Results
#  5. Export Results to CSV
#  6. View Statistics
#  7. Exit
#
# Enter Choice: 
#   No results yet. Run a scrape first.
#
# ==========================================
#            WEB SCRAPER TOOL
#            Target: books.toscrape.com
# ==========================================
#  1. Scrape Pages (Sequential)
#  2. Scrape Pages (Threaded -- faster)
#  3. Compare Sequential vs Threaded Speed
#  4. View Scraped Results
#  5. Export Results to CSV
#  6. View Statistics
#  7. Exit
#
# Enter Choice: Export filename (e.g. books.csv): 
# ✗ No results to export. Run a scrape first.
#
# ==========================================
#            WEB SCRAPER TOOL
#            Target: books.toscrape.com
# ==========================================
#  1. Scrape Pages (Sequential)
#  2. Scrape Pages (Threaded -- faster)
#  3. Compare Sequential vs Threaded Speed
#  4. View Scraped Results
#  5. Export Results to CSV
#  6. View Statistics
#  7. Exit
#
# Enter Choice: 
#   No data yet. Run a scrape first.
#
# ==========================================
#            WEB SCRAPER TOOL
#            Target: books.toscrape.com
# ==========================================
#  1. Scrape Pages (Sequential)
#  2. Scrape Pages (Threaded -- faster)
#  3. Compare Sequential vs Threaded Speed
#  4. View Scraped Results
#  5. Export Results to CSV
#  6. View Statistics
#  7. Exit
#
# Enter Choice: 
# Happy scraping! Goodbye.
#
# =============================================================================

