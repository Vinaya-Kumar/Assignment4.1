

import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants for API configuration
SERPER_DEV_API_KEY = os.getenv('SERPER_DEV_API_KEY')
SEARCH_URL = "https://google.serper.dev/search"
HEADERS = {
    "X-API-KEY": SERPER_DEV_API_KEY,
    "Content-Type": "application/json"
}

def get_news_summary(personality):
    """
    Fetches recent news articles about a personality and generates a summary article.
    
    The summary includes:
      - A list of the top 5 articles with title, snippet, and read-more link.
      - A generated summary article grouped into 3-sentence paragraphs.
    """
    # Prepare and send the POST request
    payload = json.dumps({"q": personality})
    response = requests.post(SEARCH_URL, headers=HEADERS, data=payload)
    
    if response.status_code != 200:
        return "Error fetching news. Please try again later."
    
    data = response.json()
    articles = data.get("organic", [])
    
    if not articles:
        return "No recent news found for this personality."
    
    # Build the articles summary and combine snippets for article content
    articles_summary = ""
    combined_content = ""
    
    for article in articles[:5]:
        title = article.get("title", "No Title")
        snippet = article.get("snippet", "No Summary Available")
        link = article.get("link", "#")
        
        articles_summary += f"**{title}**\n{snippet}\n[Read more]({link})\n\n"
        combined_content += f"{snippet} "
    
    # Create the summary article by splitting into sentences and grouping them into paragraphs
    sentences = combined_content.split('. ')
    article_text = "\n\n".join([". ".join(sentences[i:i+3]) for i in range(0, len(sentences), 3)])
    
    return articles_summary + "\n### Summary Article\n" + article_text

def main():
    st.title("News Summarizer Bot")
    st.write("Enter a personality's name to get the most recent news summarized in an article.")
    
    personality = st.text_input("Personality Name:")
    
    if st.button("Get News Summary"):
        if personality:
            with st.spinner("Fetching latest news..."):
                summary = get_news_summary(personality)
                st.markdown(summary)
        else:
            st.warning("Please enter a personality's name.")

if __name__ == "__main__":
    main()
