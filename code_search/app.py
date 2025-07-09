import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from keyword_extractor import KeywordExtractorFactory
from github_search import GitHubSearcher

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize components
github_token = os.getenv('GITHUB_TOKEN')
cortical_api_key = os.getenv('CORTICAL_API_KEY')

if not github_token:
    raise ValueError("Please set GITHUB_TOKEN in .env file")

github_searcher = GitHubSearcher(github_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query', '')
        language = data.get('language', '')
        extraction_method = data.get('extraction_method', 'rake')
        num_keywords = data.get('num_keywords', 5)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Extract keywords
        extractor = KeywordExtractorFactory.create_extractor(
            method=extraction_method,
            api_key=cortical_api_key
        )
        keywords = extractor.extract_keywords(query, num_keywords)
        
        if not keywords:
            return jsonify({'error': 'No keywords extracted'}), 400
        
        # Search GitHub
        results = github_searcher.search_code(
            keywords=keywords,
            language=language,
            max_results=10
        )
        
        return jsonify({
            'keywords': keywords,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)