import json
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, LLM
import os
from pydantic import BaseModel, Field
from unstructured.partition.html import partition_html
from crewai.tools import BaseTool
load_dotenv()

class WebSearchRequest(BaseModel):
    query: str = Field(..., description="The search query to perform on the web.")


class Web_search(BaseTool):    
    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize a website content"
    args_schema: type[BaseModel] = WebSearchRequest
    def _run(self, query: str) -> str:
        """
        Perform a web search using the provided query.
        
        Args:
            query (str): The search query to perform on the web.
        
        Returns:
            str: The search results or an error message.
        """
      
        try:
            url="https://google.serper.dev/search"
            payload={
                "q": query,
            }
            headers = {
                "X-API-KEY": os.getenv('SERPER_API_KEY'),
                "Content-Type": "application/json",
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))


            if response.status_code != 200:
                return f"Error: Search API request failed. Status code: {response.status_code}"
            
            res=response.json()
            query = "Python programming language"
            results=res['organic'] if 'organic' in res else "No organic results found."
            string = []
            for result in results[:4]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}", 
                        f"url: {result['link']}",
                        f"Snippet: {result['snippet']}", 
                        "\n-----------------"
                    ]))
                except KeyError:
                    continue
            return '\n'.join(string) if string else "No valid results found"
        except requests.RequestException as e:
            return f"Error: An error occurred while making the request. {str(e)}"



