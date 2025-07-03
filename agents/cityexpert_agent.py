from crewai import Agent,LLM
from tools.webscraping_tool import WebScraper
from tools.websearch_tool import Web_search
from langchain_core.language_models.chat_models import BaseChatModel
import outlines

class CityExpertAagent:
    
    def __init__(self,llm: BaseChatModel = None):
        
        if llm is None:
            self.llm = LLM(model="gemini/gemini-2.0-flash")
        else:
            self.llm = llm
        self.web_search_tool = WebScraper()
        self.web_scraper_tool = Web_search()

    def create_agent(self):
        try:
            agent = Agent(
                role='city expert',
                goal='Provide the BEST insights about the selected city',
                backstory="A knowledable tour guide with extensive knowledge about the city, and its history, culture it's attractions and customs",
                allow_delegation=False,
                llm=self.llm,
                tools=[self.web_search_tool, self.web_scraper_tool],
                verbose=True
            )
        except Exception as e:
            raise ValueError(f'CityExpertAagent not working {str(e)}') 
        return agent
    