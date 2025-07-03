from crewai import Task
from textwrap import dedent


class TravelConciergeTask():
   
    

    def plan_task(self, agent, origin, interests, range):
        return Task(description=dedent(f"""
            Expand this guide into a full travel
            itinerary for this time {range} with detailed per-day plans, including
            weather forecasts, places to eat, packing suggestions,
            and a budget breakdown.

            You MUST suggest actual places to visit, actual hotels
            to stay and actual restaurants to go to.

            This itinerary should cover all aspects of the trip,
            from arrival to departure, integrating the city guide
            information with practical travel logistics.

            Your final answer MUST be a complete expanded travel plan,
            encompassing a daily schedule,daily burget in country current and in Rupees conversion, 
            anticipated weather conditions, recommended clothing and
            items to pack, and a detailed budget, ensuring THE BEST
            TRIP EVER, Be specific and give it a reason why you picked
            Output the response in string format only,
            # up each place, what make them special! 
            Format as markdown without ```

            

            Trip Date: {range}
            Traveling from: {origin}
            Traveler Interests: {interests}
            """),
            expected_output="A complete travel plan, formatted as markdown, with a daily schedule and budget.",
            output_file='report.md',
            agent=agent)
