from scrapegraphai.graphs import SmartScraperGraph,SmartScraperMultiGraph
import json, os

# Define the configuration for the scraping pipeline
graph_config = {
   "llm": {
       "api_key": os.getenv("API_KEY"),
       "model": "openai/gpt-4o-mini",
   },
   "verbose": True,
   "headless": False,
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract the list with following event name <event_name>, event date<event_date>, location<location> and link to event<event_link>. The respnse should be a compatible with pandas dataframe.",
    source="https://10times.com/india/technology",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()
print("result keys",list(result.keys())[0])
print("result val", result[list(result.keys())[0]])

print(json.dumps(result, indent=4))