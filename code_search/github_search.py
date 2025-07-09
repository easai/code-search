import requests
from typing import List, Dict
import base64

class GitHubSearcher:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
    def search_code(self, keywords: List[str], language: str = None, 
                   max_results: int = 10) -> List[Dict]:
        """Search for code snippets on GitHub"""
        # Build search query
        query_parts = keywords
        if language:
            query_parts.append(f"language:{language}")
            
        query = " ".join(query_parts)
        
        endpoint = f"{self.base_url}/search/code"
        params = {
            "q": query,
            "per_page": max_results,
            "sort": "indexed"
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                print(data)
                for item in data.get("items", []):
                    # Get file content
                    content = self._get_file_content(item["url"])
                    
                    result = {
                        "name": item["name"],
                        "path": item["path"],
                        "repository": item["repository"]["full_name"],
                        "url": item["html_url"],
                        "content": content,
                        "language": self._detect_language(item["name"])
                    }
                    results.append(result)
                    
                return results
            else:
                print(f"GitHub API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error searching GitHub: {str(e)}")
            return []
            
    def _get_file_content(self, url: str) -> str:
        """Get the content of a file from GitHub"""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                # Decode base64 content
                content = base64.b64decode(data["content"]).decode('utf-8')
                # Limit content size for display
                if len(content) > 1000:
                    content = content[:1000] + "\n... (truncated)"
                return content
            return "Content unavailable"
        except:
            return "Content unavailable"
            
    def _detect_language(self, filename: str) -> str:
        """Simple language detection based on file extension"""
        extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.ts': 'typescript'
        }
        
        for ext, lang in extensions.items():
            if filename.lower().endswith(ext):
                return lang
        return 'unknown'