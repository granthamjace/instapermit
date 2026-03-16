# Amazon Laptop Scraper

A simple Python script that uses Selenium to scrape the first 5 laptop listings from Amazon search results, printing title, price, rating, and URL as JSON.

## Requirements

- Python 3
- Google Chrome

## Setup

1. Clone the repository:

```bash
git clone https://github.com/granthamjace/instapermit.git
cd instapermit
```

2. Create a virtual environment:

```bash
python3 -m venv venv
```

3. Activate the environment:

Mac/Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Script

```bash
python run.py
```

The script will launch a headless Chrome browser, navigate to Amazon's laptop search page, and print the first 5 results as JSON.

## Notes

- Amazon's page structure may change and break the scraper's CSS selectors.
- Avoid running the scraper against Amazon repeatedly during testing. Use a static local page instead to reduce the risk of being flagged as a bot.
- If the scraper times out, it may mean Amazon returned a CAPTCHA or robot check page rather than search results.
