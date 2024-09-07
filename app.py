from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# News API key from your .env file (use dotenv to load)
NEWS_API_KEY = "ee4835dda4cb4f0b988f2eeeb2af1f16"

# Fetch articles from the API with topic and pagination support
def fetch_articles(page=1, topic=None):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': NEWS_API_KEY,
        'pageSize': 4,  # 4 articles per page
        'page': page
    }
    
    if topic:
        params['category'] = topic  # Add topic to API parameters if provided
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['articles'], data['totalResults']  # return articles and total result count
    else:
        return [], 0  # return empty if error occurs

# Index route handling both topic and page
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    topic = request.args.get('topic')  # Get the topic parameter from the request
    articles, total_results = fetch_articles(page=page, topic=topic)
    
    total_pages = (total_results + 3) // 4  # Calculate total pages (4 articles per page)
    
    return render_template('index.html', articles=articles, page=page, total_pages=total_pages, topic=topic)

if __name__ == '__main__':
    app.run(debug=True)
