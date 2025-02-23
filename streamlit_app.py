import streamlit as st
import json
from scrapegraphai.graphs import SmartScraperGraph,SmartScraperMultiGraph
import json
import pandas as pd
import nest_asyncio
from playwright.sync_api import sync_playwright
from helper import (
    playwright_install,
    add_download_options
)
playwright_install()
nest_asyncio.apply()


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

            content = page.content()

            # Save the HTML for debugging
            with open("debug.html", "w") as f:
                f.write(content)

            # Capture a screenshot for further debugging
            # page.screenshot(path="screenshot.png")
            # print("Screenshot saved as screenshot.png")

            browser.close()
            return content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None



st.title("AI Scrapper")

api_key = st.text_input("Enter API Key", type="password")
url = st.text_input("Enter the URL")
prompt = st.text_area("Enter Prompt")


if st.button("Submit"):
    graph_config = {
        "llm": {
            "api_key": api_key,
            "model": "openai/gpt-4o-mini",
        },
        "verbose": True,
        "headless": True,     # Enable headless mode
        "use_browser": True,  # Use Playwright for JavaScript rendering
        }
    page_content = fetch_page_content(url)
    if not page_content:
        st.warning("Failed to retrieve page content.")

    if api_key and url and prompt:
        smart_scraper_graph = SmartScraperGraph(
                prompt=prompt,
                source=page_content,
                config=graph_config
            )
        # Run the pipeline
        result = smart_scraper_graph.run()
        json_resp = json.dumps(result)
        print(json.dumps(result, indent=4))
        df = pd.DataFrame(json_resp)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="data.csv",
            mime="text/csv"
        )
        st.text(json.dumps(result, indent=4))    
   
else:
    st.warning("Please fill in all fields before submitting.")