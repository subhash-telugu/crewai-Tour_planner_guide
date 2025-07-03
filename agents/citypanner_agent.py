from crewai import Agent,LLM
from tools.webscraping_tool import WebScraper
from tools.websearch_tool import Web_search
from langchain_core.language_models.chat_models import BaseChatModel


class CityPannerAgent:
    def __init__(self,llm: BaseChatModel = None):
        
        if llm is None:
            #self.llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
            self.llm = LLM(model="gemini/gemini-2.0-flash")
        else:
            self.llm = llm
        self.web_search_tool = WebScraper()
        self.web_scraper_tool = Web_search()

    def create_agent(self):
        try:
            agent = Agent(
                role='City Panner',
                goal='Plan a trip to a city based on the user\'s preferences and available resources.',
                backstory="You're a travel planner specialized in creating personalized city itineraries.",
                allow_delegation=False,
                llm=self.llm,
                tools=[self.web_search_tool, self.web_scraper_tool],
                verbose=True
            )
        except Exception as e:
            raise ValueError(f'CityPannerAgent not working {str(e)}')     
        return agent
    
    
