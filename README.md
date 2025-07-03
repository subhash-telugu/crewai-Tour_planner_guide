✈️ Tour Planner Guide AI API with crewAI and FastAPI
Welcome to the Tour Planner Guide AI API! This project implements a sophisticated multi-agent AI system for personalized travel planning, exposed as a robust RESTful API using FastAPI. Leveraging the crewAI framework, it automates the creation of detailed travel itineraries, provides deep city insights, and offers concierge services based on user preferences.

✨ Features
Multi-Agent Orchestration: A collaborative team of specialized AI agents works in harmony:

City Expert Agent: Provides in-depth knowledge and recommendations for specific destinations.

City Planner Agent: Crafts the core travel itinerary, considering origin, desired cities, user interests, and date ranges.

Travel Concierge Agent: Offers personalized advice and assists with specific travel logistics and experience recommendations.

Personalized Itinerary Generation: Dynamically creates comprehensive travel plans that are highly tailored to user-defined interests (e.g., food, adventure, history, watersports, beautiful locations) and specified date ranges.

Gemini LLM Integration: Utilizes Google Gemini models (gemini-2.0-flash or other specified models) for powerful and efficient Large Language Model inference, ensuring quick and responsive itinerary generation.

Robust API Interface: Built with FastAPI to provide a well-documented, scalable, and easy-to-use API for programmatically accessing the travel planning capabilities.

Integrated Tooling: Agents are equipped with various tools for enhanced capabilities:

Web Scraping Tool: (via Browserless.io API) for extracting information from websites.

Web Search Tool: (via Serper API) for general information retrieval.

Calculator Tool: For performing calculations as needed during planning.

Dynamic Configuration: API keys and LLM models can be configured and updated dynamically via a dedicated API endpoint, enhancing flexibility and deployment ease.

Modular and Scalable: The crewAI framework allows for easy expansion by adding new agents, tasks, and tools to handle even more complex travel scenarios.

🛠️ Technical Stack
Python: Core programming language.

crewAI: Framework for building and orchestrating multi-agent systems.

FastAPI: High-performance web framework for building the API.

uvicorn: ASGI server for running the FastAPI application.

Google Gemini API: Primary Large Language Model for agent capabilities.

pydantic: For data validation and settings management.

python-dotenv: For managing environment variables.

Browserless.io API: For web scraping.

Serper API: For search capabilities.

🚀 Getting Started
Follow these steps to get your Tour Planner AI API up and running.

Prerequisites
Python 3.10 to 3.12

Git

Installation
Clone the repository:

Bash
```
git clone https://github.com/subhash-telugu/crewai-Tour_planner_guide.git
```
cd crewai-Tour_planner_guide
```
Install uv (recommended for dependency management):
```
Bash
```
pip install uv
```
Install project dependencies:

Bash
```
uv pip install -r requirements.txt
```
(If requirements.txt is missing, you can create one after installing uv by running pip freeze > requirements.txt)

API Key Configuration
This application requires several API keys to function. You can set these directly via the /config API endpoint or manually in a .env file. Using the /config endpoint is recommended for initial setup.

Required API Keys:

GEMINI_API_KEY: Obtain from Google AI Studio.

BROWSERLESS_API_KEY: Obtain from Browserless.io.

SERPER_API_KEY: Obtain from Serper.dev.

🔌 API Usage
The API provides endpoints for configuring your keys and for triggering the trip planning process.

1. Start the FastAPI Server
From the root of your project directory, run:

Bash
```
uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```
The --reload flag is useful for development as it restarts the server on code changes. For production, remove it.

The API will be available at http://127.0.0.1:8001. You can access the auto-generated API documentation (Swagger UI) at http://127.0.0.1:8001/docs.

2. Configure API Keys (POST /config)
Before planning a trip, you must configure your API keys.

Endpoint: POST /config
Content-Type: application/json

Request Body Example:

JSON
```
{
  "gemini_model": "gemini-2.0-flash",
  "gemini_api_key": "YOUR_GEMINI_API_KEY",
  "browserless_api_key": "YOUR_BROWSERLESS_API_KEY",
  "serper_api_key": "YOUR_SERPER_API_KEY"
}
```
Example using curl:

Bash
```
curl -X POST "http://127.0.0.1:8001/config" \
-H "Content-Type: application/json" \
-d '{
  "gemini_model": "gemini-2.0-flash",
  "gemini_api_key": "YOUR_GEMINI_API_KEY_HERE",
  "browserless_api_key": "YOUR_BROWSERLESS_API_KEY_HERE",
  "serper_api_key": "YOUR_SERPER_API_KEY_HERE"
}'
```
3. Check Configuration Status (GET /check_config_status)
You can verify if the keys are loaded:

Endpoint: GET /check_config_status

Example using curl:

Bash
```
curl "http://127.0.0.1:8001/check_config_status"
Expected Response:
{"configured": true} or {"configured": false}
```
4. Plan Your Trip (POST /tourist_assistant)
Once configured, you can request a trip plan.

Endpoint: POST /tourist_assistant
Content-Type: application/json

Request Body Example:

JSON
```
{
  "origin": "Bengaluru",
  "cities": "paris,london,berlin",
  "interests": "food,history,art,museums",
  "date_range": "2025-09-10 to 2025-09-20"
}
```
Example using curl:

Bash
```
curl -X POST "http://127.0.0.1:8001/tourist_assistant" \
-H "Content-Type: application/json" \
-d '{
  "origin": "Bengaluru",
  "cities": "paris,london,berlin",
  "interests": "food,history,art,museums",
  "date_range": "2025-09-10 to 2025-09-20"
}'
```
Expected Response (example):

JSON
```
{
  "trip_plan": "Your 10-day trip from Bengaluru covering Paris, London, and Berlin:\n\nDay 1-3: Paris\n• Explore the Eiffel Tower, Louvre Museum, Notre Dame.\n• Enjoy French cuisine in Le Marais.\n• Visit Montmartre and Sacré-Cœur Basilica.\n\nDay 4-6: London\n• Discover the Tower of London, British Museum, Westminster Abbey.\n• Catch a show in West End.\n• Stroll through Hyde Park.\n\nDay 7-10: Berlin\n• Visit Brandenburg Gate, Reichstag Building, Berlin Wall Memorial.\n• Explore Museum Island.\n• Experience Berlin's vibrant nightlife.\n\nEnjoy your trip!"
}
```
📂 Project Structure
```
.
├── agents/                     # Defines individual AI agents
│   ├── __init__.py
│   ├── cityexpert_agent.py
│   ├── citypanner_agent.py
│   └── travel_concierge_agent.py
├── tasks/                      # Defines the tasks assigned to each agent
│   ├── __init__.py
│   ├── city_planner_task.py
│   ├── local_guide_task.py
│   └── travel_concierge_task.py
├── tools/                      # Contains custom tools used by agents
│   ├── __init__.py
│   ├── calculator_tool.py
│   ├── webscraping_tool.py
│   └── websearch_tool.py
├── .gitignore                  # Specifies intentionally untracked files to ignore
├── .python-version             # Specifies the Python version (e.g., for pyenv)
├── README.md                   # This README file
├── app.py                      # Main FastAPI server application
├── main.py                     # Contains the TripCrew class that orchestrates agents and tasks
└── .env                        # Environment variables (created by /config endpoint 
```