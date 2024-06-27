import os
import streamlit as st
import pandas as pd
import requests
from transformers import pipeline, TFAutoModelForSeq2SeqLM, AutoTokenizer

# Loading the LLM 
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSeq2SeqLM.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

st.title("AI Powered Research Assistant")

# Sidebar
st.sidebar.header("Research Settings")
search_query = st.sidebar.text_input("Search Query", "Artificial Intelligence")
api_key = st.sidebar.text_input("API Key", type="password")

def search_papers(query, api_key):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields=title,abstract,url"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["data"]
    
def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
    return summary

if api_key:
    papers = search_papers(search_query, api_key)

    # Display search results
    st.header("Search Results")
    for paper in papers:
        st.subheader(paper["title"])
        st.write(paper["abstract"])
        st.write(f"[Read more]({paper['url']})")

        # Summarize the abstract
        if st.button(f"Summarize {paper['title']}"):
            summary = summarize_text(paper["abstract"])
            st.write("Summary:")
            st.write(summary)

else:
    st.warning("Please enter a valid API Key.")