from scrapegraphai.graphs import SmartScraperGraph,SmartScraperMultiGraph
import json
import csv

# Define the configuration for the scraping pipeline
graph_config = {
   "llm": {
       "api_key": "",
       "model": "openai/gpt-4o-mini",
   },
   "verbose": True,
   "headless": False,
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract the Timings, Entry Fees, Estimated Turnout, website.",
    source="https://10times.com/e143-dkrr-shr0-9",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()
print(json.dumps(result, indent=4))
