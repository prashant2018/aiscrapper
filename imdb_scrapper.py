from scrapegraphai.graphs import SmartScraperGraph,SmartScraperMultiGraph
import json
import os
# Define the configuration for the scraping pipeline
graph_config = {
   "llm": {
       "api_key": os.getenv("API_KEY"),
       "model": "openai/gpt-4o-mini",
   },
   "verbose": True,
   "headless": True,
   "browser": "chrome",
   "driver_path":"/opt/homebrew/bin/chromedriver",
   "browser_path":"/opt/homebrew/bin/chromium"
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract the list of movie name,year, description, image icon url, detail page url",
    source="https://www.imdb.com/find/?q=horror&s=tt&exact=true&ref_=fn_ttl_ex",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()
print(json.dumps(result, indent=4))

# sources = []
# for res in result['events']:
#     sources.append(res['event_link'])

# result_list = []
# for source in sources[:2]:
#     smart_scraper_graph = SmartScraperGraph(
#         prompt="Extract the Timings, Entry Fees, Estimated Turnout, website.",
#         source=source,
#         config=graph_config
#     )
#     result = smart_scraper_graph.run()
#     result_list.append(result)

# print(json.dumps(result_list, indent=4))
