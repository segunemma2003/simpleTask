# Scrapy RSS Feed Spider

This Scrapy project is designed to scrape data from a specific RSS feed using Scrapy and Playwright.

## Installation

### 1. Create a Virtual Environment

```bash
# Create a virtual environment (replace 'venv' with your preferred name)
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install project requirements from the requirements.txt file
pip install -r requirements.txt

# Run the spider and save the output to a JSON file
scrapy crawl rssfeed_spider -o output.json
