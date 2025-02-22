from textblob import TextBlob
from newsapi import NewsApiClient

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
        response = newsapi.get_top_headlines(category=category, language="en", page_size=5)  # Fetch top 5 articles
        return response["articles"]
    except Exception as e:
        print(f"Error fetching news for {category}: {e}")
        return []

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

def display_news():
    """
    Fetch, analyze, and display news articles in the terminal.
    """
    print("Welcome to the AI-Powered News Aggregator!\n")
    
    for category in CATEGORIES:
        print(f"=== {category.upper()} ===")
        articles = fetch_news(category)
        
        if not articles:
            print("No articles found.\n")
            continue
        
        for i, article in enumerate(articles, 1):
            title = article["title"]
            description = article["description"]
            url = article["url"]
            classification = analyze_headline(title)
            
            print(f"\nArticle {i}:")
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"Classification: {classification}")
            print(f"URL: {url}")
        
        print("\n" + "=" * 30 + "\n")

if __name__ == "__main__":
    display_news()
