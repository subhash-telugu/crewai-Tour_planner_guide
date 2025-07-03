from crewai import Agent,LLM
from tools.webscraping_tool import WebScraper
from tools.websearch_tool import Web_search
from tools.calculator_tool import CalculatorTools
from langchain_core.language_models.chat_models import BaseChatModel

class TravelConciergeAgent:
    def __init__(self,llm: BaseChatModel = None):
        if llm is None:
            #self.llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
            self.llm = LLM(model="gemini/gemini-2.0-flash")
        else:
            self.llm = llm
        self.web_search_tool = WebScraper()
        self.web_scraper_tool = Web_search()
        self.calculator_tool=CalculatorTools()

    def create_agent(self):
        try:
            agent = Agent(
                role='Amazing Travel Concierge',
                goal="""Create the most amazing travel itineraries with budget and 
            packing suggestions for the city""",
                backstory="""Specialist in travel planning and logistics with 
            decades of experience""",
                tools=[self.web_search_tool,self.web_scraper_tool, self.calculator_tool],
                allow_delegation=False,
                llm=self.llm,
                verbose=True
            )
        except Exception as e:                    
            raise ValueError(f'TravelConciergeAgent not working {str(e)}')     
        return agent

