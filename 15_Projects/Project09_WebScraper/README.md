# 🕸️ Project 9: Web Scraper Tool

**Author:** Pavan Shetty H S
**Built:** October 2024

---

## Project Overview

A multi-page book scraper that combines Module 12 (web scraping) and
Module 10 (multithreading) concepts. Scraping multiple pages is
I/O-bound — most of the time is spent WAITING for network responses, not
computing — which is exactly the scenario where Python's threading
genuinely helps, unlike the CPU-bound case from Module 10 where I
measured NO real speedup due to the GIL. This project let me prove that
distinction to myself with real, timed results instead of just trusting
the theory.

Targets `books.toscrape.com`, a site built specifically for scraping
practice, with a clear comment in the code about checking `robots.txt`
and rate-limiting on real production sites.

## Features

- Scrape multiple pages sequentially OR concurrently with threading
- Built-in sequential vs threaded speed comparison tool
- Thread-safe result collection (using `threading.Lock`)
- Export results to CSV
- Summary statistics (average/min/max price, total books found)
- Graceful handling of failed requests (timeouts, non-200 responses)

## Folder Structure

```
Project09_WebScraper/
├── web_scraper.py
├── README.md
└── requirements.txt
```

## Flowchart

```
   Threaded Scrape Flow:
   ┌─────────┐
   │  Start    │
   └────┬─────┘
        │
  ┌─────▼──────────┐
  │ For each page:    │
  │  spawn a Thread     │
  └─────┬──────────┘
        │
  ┌─────▼──────────┐
  │ Each thread fetches │
  │ + parses its page    │
  │ + acquires Lock        │
  │ + appends to results     │
  │ + releases Lock            │
  └─────┬──────────┘
        │
  ┌─────▼──────────┐
  │ Main thread joins   │
  │ all worker threads    │
  └─────┬──────────┘
        │
   ┌────▼────┐
   │   End    │
   └─────────┘
```

## Class Diagram

```
┌──────────────────────────────┐
│           BookScraper              │
├──────────────────────────────┤
│ - results: list[dict]                │
│ - lock: threading.Lock                │
├──────────────────────────────┤
│ + scrape_page(page_num)                │
│ + scrape_pages_sequential(n)             │
│ + scrape_pages_threaded(n)                │
│ + export_to_csv(filepath)                   │
│ + get_stats()                                 │
└──────────────────────────────┘
```

## Algorithm

**Thread-Safe Result Collection:**
1. Each worker thread scrapes ONE page independently
2. Before modifying the shared `self.results` list, a thread must
   acquire `self.lock`
3. This prevents the exact race condition demonstrated in Module 10's
   Multithreading.py — without the lock, simultaneous list mutations
   from multiple threads could corrupt data or lose entries
4. After appending, the lock is released for the next thread

## Requirements

```
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
```

## Installation Steps

```bash
cd 15_Projects/Project09_WebScraper
pip install -r requirements.txt
python web_scraper.py
```

## Sample Inputs & Outputs

```
==========================================
           WEB SCRAPER TOOL
           Target: books.toscrape.com
==========================================

Note: this scraper targets books.toscrape.com, a site built
specifically for scraping practice. Always check robots.txt
and rate-limit yourself on real production sites.

 1. Scrape Pages (Sequential)
 2. Scrape Pages (Threaded -- faster)
 3. Compare Sequential vs Threaded Speed
 4. View Scraped Results
 5. Export Results to CSV
 6. View Statistics
 7. Exit

Enter Choice: 3
Number of pages for comparison: 5

  Sequential: 3.42s
  Threaded  : 0.89s
  Speedup   : 3.84x faster with threading
  (Real speedup here because this is I/O-bound work --
  see Module 10's Multithreading.py notes for why this
  differs from CPU-bound tasks where threading didn't help)

Enter Choice: 6

  Total Books   : 100
  Average Price : £35.07
  Min Price     : £10.00
  Max Price     : £59.99

Enter Choice: 5
Export filename (e.g. books.csv): scraped_books.csv

✓ Exported to scraped_books.csv
```

## Screenshots

> See `/Images/Screenshots/project09_*.png`:
> - `project09_menu.png`
> - `project09_speed_comparison.png` — sequential vs threaded timing
> - `project09_results_view.png`
> - `project09_csv_export.png`
> - `project09_stats.png`

## Learning Outcomes

- Directly applied the I/O-bound vs CPU-bound distinction from Module 10
  to a real project, with measured timing proof rather than just trusting
  the concept
- Used `threading.Lock` for genuinely necessary thread safety, not as a
  theoretical exercise — multiple threads really do write to the same
  results list concurrently here
- Reinforced responsible scraping habits (descriptive User-Agent,
  timeout on every request, target a scraping-friendly practice site)
- Combined concepts across two separate modules (12 and 10) into one
  cohesive project, which felt like a meaningful step up from
  single-module exercises

## Future Enhancements

- [ ] Add `asyncio`/`aiohttp` version to compare against threading
      (haven't studied async yet — noted as a future learning goal)
- [ ] Configurable rate limiting between requests
- [ ] Resume capability for interrupted large scrapes
- [ ] Price drop tracking across multiple scrape runs over time
