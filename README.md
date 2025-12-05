# IA626_FinalProject_venkatb_pammics

Project Overview: This project focuses on building an automated pipeline for collecting, storing, and serving news or blog articles. It begins with a web scraping system that extracts article data (titles, authors, publication dates, content, etc.) from target websites. The scraped data is then structured and stored in a database, ensuring it can be queried efficiently and reliably.

On top of this data pipeline, the project exposes a REST API endpoint that allows external applications to access the collected articles. This enables developers to integrate the article dataset into other tools, dashboards, or research workflows.

The goal of this project is to provide a simple, end-to-end solution for:

1) Scraping article content from the web

2) Cleaning and storing data in a persistent database

3) Serving the data through an accessible API

This repository includes all components needed for the workflow, including scrapers, database schema, API routes, and documentation for setting everything up.