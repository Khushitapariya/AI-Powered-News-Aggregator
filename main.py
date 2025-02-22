from flask import Flask, render_template
import requests
from textblob import TextBlob
from newsapi import NewsApiClient

app = Flask(__name__)

# Initialize NewsAPI client
NEWS_API_KEY = "c3d18f0e3bdf4b738072c4340066070d" 
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Predefined categories
CATEGORIES = ["technology", "sports", "business", "health", "entertainment", "science"]

def fetch_news(category):
    """
    Fetch news articles for a given category using NewsAPI.
    """
    try:
        response = newsapi.get_top_headlines(category=category, language="en", page_size=10)
        return response["articles"]
    except Exception as e:
        print(f"Error fetching news for {category}: {e}")
        return []

def categorize_article(text):
    """
    Categorize an article based on its content using TextBlob.
    """
    blob = TextBlob(text)
    nouns = blob.noun_phrases  # Extract noun phrases to identify topics

    # Match nouns with predefined categories
    for noun in nouns:
        for category in CATEGORIES:
            if category in noun:
                return category
    return "general"  # Default category

def summarize_article(text, max_sentences=2):
    """
    Generate a summary of the article using TextBlob.
    """
    blob = TextBlob(text)
    sentences = blob.sentences
    summary = " ".join([str(sentence) for sentence in sentences[:max_sentences]])
    return summary

def analyze_headline(headline):
    """
    Analyze a headline to detect misleading content.
    """
    blob = TextBlob(headline)
    
    # Check for sensational or exaggerated language
    sensational_words = ["shocking", "unbelievable", "amazing", "mind-blowing", "must-see"]
    sensational_count = sum(headline.lower().count(word) for word in sensational_words)
    
    # Check for negative sentiment (can indicate bias)
    sentiment = blob.sentiment.polarity
    
    # Classify as misleading if sensational language is present or sentiment is highly negative
    if sensational_count > 1 or sentiment < -0.5:
        return "Misleading"
    else:
        return "Reliable"

@app.route("/")
def home():
    """
    Render the home page with categorized news articles.
    """
    categorized_news = {category: [] for category in CATEGORIES}

    # Fetch and categorize news articles
    for category in CATEGORIES:
        articles = fetch_news(category)
        for article in articles:
            title = article["title"]
            description = article["description"]
            url = article["url"]
            image = article["urlToImage"]

            # Summarize the article
            classification = analyze_headline(title) 

            # Add the article to the categorized news dictionary
            categorized_news[category].append({
                "title": title,
                "description": description,
                "url": url,
                "image": image
                "classification": classification
            })

    return render_template("index.html", categorized_news=categorized_news)

if __name__ == "__main__":
    app.run(debug=True)
