from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import re

# Assuming 'main' module and 'TripCrew' class exist in main.py
# Make sure your main.py file is in the same directory as this file.
# NOTE: For this to work, your main.py (where TripCrew is defined)
# must be updated to accept the gemini_model and API keys as arguments
# and load them from os.environ or directly use the passed arguments
# for the LLM initialization within TripCrew.
from main import TripCrew # Ensure TripCrew in main.py can accept/use environment variables set here.

# Define the input schema for the main trip planning API endpoint
class InputSchema(BaseModel):
    origin: str = Field(..., description="The origin city of the user, e.g. 'Bangalore'")
    interests: str = Field(..., description="The interests of the user, e.g. 'food, trucking, adventure, history, watersports, beautiful_locations'")
    cities: str = Field(..., description="The cities to consider for the trip, e.g. 'paris,london,berlin,japan'")
    date_range: str = Field(..., description="The date range for the data to be fetched, e.g. '2023-01-01 to 2023-12-31'")

# Define the input schema for the /config endpoint
class ConfigInputSchema(BaseModel):
    gemini_model: str = Field(..., description="The Gemini model to use, e.g., 'gemini-2.0-flash'")
    gemini_api_key: str = Field(..., description="Your Gemini API Key")
    browserless_api_key: str = Field(..., description="Your Browserless API Key")
    serper_api_key: str = Field(..., description="Your Serper API Key")


# Initialize the FastAPI application
app = FastAPI(
    title="CrewAI Tourist Assistant API",
    description="API to plan trips using CrewAI agents and external tools.",
    version="1.0.0",
)

# Configure CORS (useful if a separate frontend will consume this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint to check if API keys are configured
@app.get("/check_config_status")
async def check_config_status():
    """
    Checks if the necessary API keys (Gemini, Browserless, Serper) and Gemini model
    are set as environment variables.
    """
    configured = all([
        os.getenv("GEMINI_MODEL"),
        os.getenv("GEMINI_API_KEY"),
        os.getenv("BROWSERLESS_API_KEY"),
        os.getenv("SERPER_API_KEY")
    ])
    return JSONResponse(content={"configured": configured}, status_code=200)


# POST endpoint for configuration
@app.post('/config')
def set_configuration(config_data: ConfigInputSchema):
    """
    Sets the Gemini model and API keys as environment variables for the application
    and saves them to a .env file.
    These keys will be used by the /tourist_assistant endpoint.
    """
    env_file_path = ".env"
    try:
        # Set environment variables for the current runtime of the FastAPI process
        os.environ["GEMINI_MODEL"] = config_data.gemini_model
        os.environ["GEMINI_API_KEY"] = config_data.gemini_api_key
        os.environ["BROWSERLESS_API_KEY"] = config_data.browserless_api_key
        os.environ["SERPER_API_KEY"] = config_data.serper_api_key

        # Save the content to a .env file for persistence across restarts
        with open(env_file_path, "w") as f:
            f.write(f"GEMINI_MODEL=\"{config_data.gemini_model}\"\n")
            f.write(f"GEMINI_API_KEY=\"{config_data.gemini_api_key}\"\n")
            f.write(f"BROWSERLESS_API_KEY=\"{config_data.browserless_api_key}\"\n")
            f.write(f"SERPER_API_KEY=\"{config_data.serper_api_key}\"\n")

        return JSONResponse(content={"message": f"Configuration updated and saved to {env_file_path} successfully!"}, status_code=200)
    except Exception as e:
        # Log the error if saving to .env fails, but still raise HTTPException
        print(f"Warning: Failed to save configuration to .env file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to set configuration: {e}")


# POST endpoint for the tourist assistant
@app.post('/tourist_assistant')
def planner(input_data: InputSchema):
    """
    Triggers the CrewAI travel planning process with the provided input.
    Requires API keys to be configured via the /config endpoint first.
    """
    try:
        # Validate input data
        if not input_data.origin or not input_data.cities or not input_data.interests or not input_data.date_range:
            raise HTTPException(
                status_code=400,
                detail="All fields (origin, cities, interests, date_range) are required."
            )

        # Retrieve API keys and model from environment variables
        gemini_model = os.getenv("GEMINI_MODEL")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
        serper_api_key = os.getenv("SERPER_API_KEY")

        # Validate that all necessary environment variables are set
        if not all([gemini_model, gemini_api_key, browserless_api_key, serper_api_key]):
            raise HTTPException(
                status_code=400,
                detail="API keys and Gemini model are not configured. Please POST to /config first."
            )

        try:
            # Instantiate TripCrew with all necessary parameters
            # IMPORTANT: TripCrew in main.py MUST be able to read these env vars or accept them directly.
            crew = TripCrew(
                origin=input_data.origin,
                cities=input_data.cities,
                interests=input_data.interests,
                date_range=input_data.date_range,
            )

            # Run the crew to get the output
            output = crew.run_crew()

            # Convert the output to string if it's not already
            if not isinstance(output, str):
                output = str(output)

            # Convert markdown to plain text for a cleaner JSON response
            output = output.replace('#', '') # Remove markdown headers
            output = output.replace('**', '').replace('*', '') # Remove markdown bold/italic markers
            output = output.replace('- ', '• ') # Convert markdown list markers to bullet points
            output = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', output) # Remove markdown links (keep text)
            output = re.sub(r'\n\s*\n', '\n\n', output) # Normalize multiple newlines
            output = output.strip() # Remove leading/trailing whitespace

            # Return the output as a JSON response
            return JSONResponse(content={"trip_plan": output}, status_code=200)

        except Exception as e:
            print(f"An error occurred during trip planning: {e}") # Log the error for debugging
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred during trip planning: {str(e)}"
            )

    except HTTPException as he:
        # Re-raise HTTPException directly if it was already raised
        raise he
    except Exception as e:
        print(f"An unexpected error occurred in the main planner function: {e}") # Log unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)