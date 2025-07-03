from crewai import Task
from textwrap import dedent


class CityGuideTask():

    def guide_task(self, agent, origin, interests, range):
            
            task=Task(description=dedent(f"""
                As a local expert on this city you must compile an
                in-depth guide for someone traveling there and wanting
                to have THE BEST trip ever!
                Gather information about  key attractions, local customs,
                special events, and daily activity recommendations.
                Find the best spots to go to, the kind of place only a
                local would know.
                This guide should provide a thorough overview of what
                the city has to offer, including hidden gems, cultural
                hotspots, must-visit landmarks, weather forecasts, and
                high level costs.

                The final answer must be a comprehensive city guide,
                rich in cultural insights and practical tips,
                tailored to enhance the travel experience.
            

                Trip Date: {range}
                Traveling from: {origin}
                Traveler Interests: {interests}
            """),
                expected_output="A comprehensive city guide with cultural insights and practical tips.",
                agent=agent)
            return task  