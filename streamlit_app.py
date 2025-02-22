import streamlit as st
import json
from scrapegraphai.graphs import SmartScraperGraph,SmartScraperMultiGraph
import json
import pandas as pd
from helper import (
    playwright_install,
    add_download_options
)

playwright_install()


st.title("AI Scrapper")

api_key = st.text_input("Enter API Key", type="password")
source = st.text_input("Enter API URL")
prompt = st.text_area("Enter Prompt")


if st.button("Submit"):
    graph_config = {
        "llm": {
            "api_key": api_key,
            "model": "openai/gpt-4o-mini",
        },
        "verbose": True,
        "headless": False,
        }
    if api_key and source and prompt:
        smart_scraper_graph = SmartScraperGraph(
                prompt=prompt,
                source=source,
                config=graph_config
            )
        # Run the pipeline
        result = smart_scraper_graph.run()
        print(json.dumps(result, indent=4))
        st.text(json.dumps(result, indent=4))        
else:
    st.warning("Please fill in all fields before submitting.")