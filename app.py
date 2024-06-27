import streamlit as st
import pandas as pd
import requests
from transformers import pipeline, TFAutoModelForSeq2SeqLM, AutoTokenizer
from login import login_portal

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_portal()
    
    else:
        display_main_app()

def display_main_app():
    # Loading the LLM 
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    st.title("AI Powered Research Assistant")
    st.write(f"Welcome! {st.session_state.username}")
    st.write("This website is designed to help you discover and summarize research papers on your topic of interest.")
    st.write(f"Enter the topic you are interested in and your Semantic Scholar API Key in the input fields on the sidebar. In case you don't have an API key, you can get it from [this link](https://www.semanticscholar.org/product/api).")

    # Sidebar
    st.sidebar.header("Research Settings")
    search_query = st.sidebar.text_input("Search Query", "Machine Learning")
    api_key = st.sidebar.text_input("Semantic Scholar API Key", type="password")

    def search_papers(query, api_key):
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields=title,abstract,url"
        headers = {"x-api-key": api_key}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                return data.get("data", [])
            else:
                st.error("Unexpected response format from the API.")
                st.text(data)
                return []
        else:
            st.error(f"API request failed with status code {response.status_code}")
            return []
            
    def summarize_text(text):
        # inputs = tokenizer.encode("summarize: " + text, return_tensors="tf", max_length=1024, truncation=True)
        # summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        # summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        # return summary

        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
        return summary

    if st.sidebar.button("Search"):
        if api_key and search_query:
            papers = search_papers(search_query, api_key)
            if papers:
                # Display search results
                st.header("Search Results")
                for paper in papers:
                    st.subheader(paper["title"])
                    st.write(paper["abstract"])
                    st.write(f"[Read more]({paper['url']})")
                    if st.button(f"Summarize {paper['title']}"):
                        summary = summarize_text(paper["abstract"])
                        st.write(f"**Summary:** {summary}")
            else:
                st.error("No papers found.")
        else:
            st.warning("Please enter a valid API Key and a search query.")

if __name__ == '__main__':
    main()