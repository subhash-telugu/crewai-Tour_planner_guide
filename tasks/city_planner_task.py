from crewai import Task
from textwrap import dedent


class cityPlannerTask():
    def __validate_inputs(self, origin, cities, interests, date_range):
        if not origin or not cities or not interests or not date_range:
            raise ValueError("All input parameters must be provided")
        return True

    def planner_task(self, agent, origin, cities, interests, range):
        self.__validate_inputs(origin, cities, interests, range)
        return Task(description=dedent(f"""
            Analyze and select the best city for the trip based
            on specific criteria such as weather patterns, seasonal
            events, and travel costs. This task involves comparing
            multiple cities, considering factors like current weather
            conditions, upcoming cultural or seasonal events, and
            overall travel expenses.

            Your final answer must be a detailed
            report on the chosen city, and everything you found out
            about it, including the actual flight costs, weather
            forecast and attractions.

            Traveling from: {origin}
            City Options: {cities}
            Trip Date: {range}
            Traveler Interests: {interests}
          """),
            expected_output="A detailed report on the chosen city with flight costs, weather forecast, and attractions.",
            agent=agent)