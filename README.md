# Web Scraping Data Acquisition Protocol – Books E-commerce

This repository implements an **end-to-end data acquisition protocol** using web scraping on a demo e-commerce website for books: `https://books.toscrape.com/`.

The goal is to demonstrate how to:
- Identify a data source.
- Design a web scraping strategy.
- Collect, validate, and store the data in a structured format.
- Document the full acquisition process in a reproducible way.

> Note: The target website is a public demo site created specifically for web scraping practice.

---

## Project Overview

- **Problem**: Build a clean and analyzable catalog of books from an online store.
- **Data type**: Structured tabular data (title, price, rating, availability, URL).
- **Source**: Demo e-commerce website (`books.toscrape.com`) with multiple pages of book listings.

---

## Repository Structure

```text
web-scraping-books-protocol/
├─ data/
│   ├─ raw/          # Raw HTML pages or intermediate files
│   └─ processed/    # Final CSV/JSON datasets
├─ notebooks/        # Jupyter notebooks for exploration and demonstration
├─ src/              # Reusable scraping and data processing code
└─ docs/             # Documentation of the data acquisition protocol

