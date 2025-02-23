from scrapegraphai.graphs import SmartScraperGraph
import json
import os
from playwright.sync_api import sync_playwright

# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": os.getenv("OPENAI_API_KEY"),  # Secure API key handling
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": True,     # Enable headless mode
    "use_browser": True,  # Use Playwright for JavaScript rendering
}

# Fetch page content using Playwright
def fetch_page_content(url):
    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch(headless=True)

            # Set custom user agent and headers
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://www.google.com/",
                }
            )

            page = context.new_page()

            print(f"Navigating to {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=120000)

            # Explicitly wait for the movie list to load
            page.wait_for_selector("body", timeout=60000)

            # Ensure dynamic content is fully loaded
            page.wait_for_timeout(5000)  # Give additional time for rendering

            # Log page status and headers
            print(f"Headers: {page.evaluate('() => navigator.userAgent')}")

            print("Movie list loaded")

            content = page.content()

            # Save the HTML for debugging
            with open("debug.html", "w") as f:
                f.write(content)

            # Capture a screenshot for further debugging
            page.screenshot(path="screenshot.png")
            print("Screenshot saved as screenshot.png")

            browser.close()
            return content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

url = "https://10times.com/india/technology"
page_content = fetch_page_content(url)

if not page_content:
    print("Failed to retrieve page content. Exiting...")
    exit(1)

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract the list of event name <event_name>, event date<event_date>, location<location> and link to event<event_link>.",
    source=page_content,  # Pass HTML content directly
    config=graph_config
)

# Run the scraper
result = smart_scraper_graph.run()

print(json.dumps(result, indent=4))