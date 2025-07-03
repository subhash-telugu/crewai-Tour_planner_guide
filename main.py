
from crewai import Crew,LLM
from agents.travel_concierge_agent import TravelConciergeAgent
from agents.cityexpert_agent import CityExpertAagent
from agents.citypanner_agent import CityPannerAgent
from tasks.city_planner_task import cityPlannerTask
from tasks.travel_concierge_task import TravelConciergeTask
from tasks.local_guide_task import CityGuideTask
from langchain_groq import ChatGroq

from typing import TypedDict
from dotenv import load_dotenv
import os
load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

llm=ChatGroq(model='gemma2-9b-it')


class TripCrew:
    def __init__(self, origin, cities, interests, date_range):
        self.orgin=origin
        self.cities=cities
        self.interests=interests
        self.data_range=date_range
        self.llm = LLM(model='gemini/gemini-2.0-flash')
        

    def  run_crew(self):
        try:
            city_expert_agent = CityExpertAagent(self.llm).create_agent()
            city_planner_agent=CityPannerAgent(self.llm).create_agent()
            travel_concierge_agent=TravelConciergeAgent(self.llm).create_agent()   
            city_planner_task=cityPlannerTask().planner_task(city_planner_agent,self.orgin,self.cities,self.interests,self.data_range)
            city_expert_task=CityGuideTask().guide_task(city_expert_agent,self.orgin,self.interests,self.data_range)
            travel_concierge_task=TravelConciergeTask().plan_task(travel_concierge_agent,self.orgin,self.interests,self.data_range)

            crew=Crew(
                agents=[city_planner_agent,city_expert_agent,travel_concierge_agent],
                tasks=[city_planner_task,city_expert_task,travel_concierge_task],
                verbose=True,                
            )


            result=crew.kickoff()
            
            
            return result
        except Exception as e:
            raise ValueError(f'crew not working {str(e)}') 


if __name__ == "__main__":
    crew=TripCrew( origin='Bangalore',
    cities='paris,london,berlin,japan',
    interests='food,trucking,adventure,history,watersports,beautiful_locations',
    date_range= '2025-06-01 to 2025-06-10')
    crew.run_crew()
