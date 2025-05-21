import http.client # This import is not actually used, can be removed if you stick with requests
import json
import os
import requests 
from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader

class SearchTools:
    @tool('search_internet')
    def search_internet(query: str) -> str:
        """
        Search the internet for information on a given query.
        This tool Returns a list from google search engine.
        """
        return SearchTools.search(query)
    
    @tool('search_instagram')
    def search_instagram(query: str) -> str:
        """
        Use this tool to Search Instagram for information on a given query.
        This tool Returns  5 results from instagram search engine.
        """
        return SearchTools.search(f"site:instagram.com {query}", limit=5)
    
    @tool('open_page')
    def open_page(url: str) -> str:
        """
        Use this tool to open a web page.
        This tool Returns the content of the web page.
        """
        loader = WebBaseLoader(url)
        return loader.load()
    
    @staticmethod 
    def search(query, limit=5): 
        url="https://google.serper.dev/search"

        payload = json.dumps({
            "q": query,
            "num": limit
        })
        
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status() 
            results = response.json().get('organic', []) 

            string = []
            for result in results:
                title = result.get('title', 'No Title') 
                snippet = result.get('snippet', 'No Snippet')
                link = result.get('link', '#')
                string.append(f"{title}\n{snippet}\n{link}\n\n")

            if not string:
                return f"No search results found for '{query}'."
            return f"Search results for '{query}':\n\n" + "".join(string)
        except requests.exceptions.RequestException as e:
            return f"Error during search request: {e}"
        except KeyError as e:
            return f"Error parsing search results (missing key: {e}): {response.text if 'response' in locals() else 'No response data'}"
        except json.JSONDecodeError:
            return f"Error decoding JSON from search results: {response.text if 'response' in locals() else 'No response data'}"


if __name__ == "__main__":
    # Ensure your .env file is in the project root (E:\Projects\Python\Instagram_marketing\.env)
    # and main.py or similar has loaded it, OR load it here for standalone testing
    from dotenv import load_dotenv
    import sys
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    dotenv_path = os.path.join(project_root, '.env')
    
    if not os.getenv('SERPER_API_KEY'):
        print(f"SERPER_API_KEY not found in environment. Attempting to load from: {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)

    serper_key = os.getenv('SERPER_API_KEY')
    if not serper_key:
        print("SERPER_API_KEY is not set in the environment variables or .env file.")
        print("Please ensure it's correctly set up to test the search tools.")
    else:
        print(f"Using SERPER_API_KEY: {serper_key[:5]}...{serper_key[-4:]}") 
        print("\n--- Testing Internet Search ---")
        print(SearchTools.search_internet("Latest AI art trends 2025"))
        print("\n--- Testing Instagram Search ---")
        print(SearchTools.search_instagram("AI art trends 2025"))
        print("\n--- Testing Open Page ---")
        print(SearchTools.open_page("https://www.google.com"))
