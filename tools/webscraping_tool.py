from dotenv import load_dotenv
import json
import requests
import os
from unstructured.partition.html import partition_html
from langchain_core.language_models.chat_models import BaseChatModel
from crewai import Agent, Task, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
load_dotenv()


class WebScraperRequest(BaseModel):
    website: str = Field(..., description="The URL of the website to scrape and summarize.")


class WebScraper(BaseTool): 

    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize a website content"
    args_schema: type[BaseModel] = WebScraperRequest
 
    def _run(self, website: str) -> str:
        """
        Scrape the content of a given website and summarize it.
        
        Args:
            website (str): The URL of the website to scrape and summarize.
        
        Returns:
            str: The summarized content of the website.
        """
        try:
            url = f"https://chrome.browserless.io/content?token={os.getenv('BROWSERLESS_API_KEY')}"
            payload = json.dumps({"url": website})
            headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload)
            
            if response.status_code != 200:
                return f"Error: Failed to fetch website content. Status code: {response.status_code}"
            
        except requests.RequestException as e:
            return f"Error: An error occurred while making the request.to the website scraping {str(e)}"


        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        
        #llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
        llm = LLM(model="gemini/gemini-2.0-flash")
        
        for chunk in content:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing researches and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                allow_delegation=False,
                llm=llm
            )
            task = Task(
                description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}',
                agent=agent
            )
            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)

        