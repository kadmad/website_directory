# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All Django commands are run from `sitelike/` directory:

```bash
cd sitelike
python manage.py runserver          # Start dev server
python manage.py migrate            # Apply migrations
python manage.py makemigrations     # Create new migrations
python manage.py createsuperuser    # Create admin user
python manage.py test directory     # Run tests for the directory app
python manage.py test directory.tests.SpecificTestCase  # Run a single test
```

Utility scripts (run from `sitelike/`):
```bash
python script.py                    # Scrape and import 100 top websites
python sitemap_generator.py         # Regenerate sitemap.xml
```

## Architecture

Django 4.2 project with a single app (`directory`) and PostgreSQL backend.

**URL structure**: All website routes are under `/websites/`. Views follow standard Django CBV patterns (ListView, DetailView, CreateView, UpdateView, DeleteView).

**Data flow for new entries**: `DirectoryForm` (domain + category only) → `DirectoryCreateView` → `capture_website_screenshot()` in `utils.py` (Selenium + Chrome) → saves WebP thumbnail to `media/snaps/` → stored in `Directory` model.

**Bulk import**: `script.py` scrapes sitelike.org for top 100 websites, extracts SEO metrics (DA, Moz Rank, SEMrush Rank, website worth, Facebook likes), captures screenshots, and inserts into the database.

**Key model**: `Directory` in `directory/models.py` — tracks `domain`, `title`, `description`, SEO metrics, `category` (20 choices), and `image_url`. Extends `TimestampedModel` from `base_models.py`.

**Templates**: Located at `directory/templates/directory/`. Bootstrap 4 layout with Crispy Forms for form rendering. Grid layout uses ad column slots (col-md-2 sidebars + col-md-8/9 content).

## Database

PostgreSQL — credentials are hardcoded in `sitelike/settings.py` (host=localhost, db=sitelike, user=postgres). No `.env` setup exists yet.
