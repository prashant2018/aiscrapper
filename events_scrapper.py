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
    prompt="Extract the list of event name <event_name>, event date<event_date>, location<location> and link to event<event_link>.",
    source="https://10times.com/india/technology",
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

# Get field names from keys of the first dictionary
fieldnames = result['events'][0].keys()

csv_filename = "output.csv"

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write data
    writer.writerows(result)

print(f"CSV file '{csv_filename}' saved successfully.")