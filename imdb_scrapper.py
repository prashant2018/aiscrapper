from scrapegraphai.graphs import SmartScraperGraph,SmartScraperMultiGraph
import json
import os
import nest_asyncio
nest_asyncio.apply()
# Define the configuration for the scraping pipeline
graph_config = {
   "llm": {
       "api_key": os.getenv("API_KEY"),
       "model": "openai/gpt-4o-mini",
   },
   "verbose": True,
   "headless": True,
#    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
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



# async def scrapegraph_products(domain_url: str, prompt: str):
#     scrape_graph = SmartScraperGraph(
#         prompt=prompt,
#         source=domain_url,
#         config=graph_config,
#     )
#     loop = asyncio.get_running_loop()
#     result = await loop.run_in_executor(None, scrape_graph.run)
#     print(result)
#     return result

# if __name__=='__main__':
#     asyncio.run(scrapegraph_products("https://www.imdb.com/find/?q=horror&s=tt&exact=true&ref_=fn_ttl_ex","Extract the list of movie name,year, description, image icon url, detail page url"))