import streamlit as st
from pydantic import BaseModel, Field
import os
import datetime # Import the datetime module

# Assuming 'main' module and 'TripCrew' class exist in main.py
from main import TripCrew

# Define the input schema (can be used for validation if needed, though Streamlit handles UI)
class InputSchema(BaseModel):
    origin: str = Field(..., description="The origin city of the user, e.g. 'Bangalore'")
    interests: str = Field(..., description="The interests of the user, e.g. 'food, trucking, adventure, history, watersports, beautiful_locations'")
    cities: str = Field(..., description="The cities to consider for the trip, e.g. 'paris,london,berlin,japan'")
    start_date: datetime.date = Field(..., description="The start date for the trip, e.g. '2023-01-01'")
    end_date: datetime.date = Field(..., description="The end date for the trip, e.g. '2023-12-31'")

st.set_page_config(page_title="AI Tourist Assistant")

st.title("Welcome to AI Tourist Assistant")
st.markdown("Plan your dream trip with the help of AI!")

# --- Sidebar for Model and API Key Configuration ---
st.sidebar.header("Configuration")

# Dropdown for Gemini Models
gemini_models = ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
selected_gemini_model = st.sidebar.selectbox(
    "Select Gemini Model",
    gemini_models,
    index=0
)

# Text input for Gemini API Key
gemini_api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    placeholder="Enter your Gemini API key here"
)

# Text input for Browserless API Key
browserless_api_key = st.sidebar.text_input(
    "Browserless API Key",
    type="password",
    placeholder="Enter your Browserless API key here"
)

# Text input for Serper API Key
serper_api_key = st.sidebar.text_input(
    "Serper API Key",
    type="password",
    placeholder="Enter your Serper API key here"
)

# Function to save API keys to .env file
def save_api_keys_to_env(gemini_key, browserless_key, serper_key):
    """Saves the provided API keys to a .env file."""
    env_path = ".env"
    try:
        with open(env_path, "w") as f:
            f.write(f"GEMINI_API_KEY=\"{gemini_key}\"\n")
            f.write(f"BROWSERLESS_API_KEY=\"{browserless_key}\"\n")
            f.write(f"SERPER_API_KEY=\"{serper_key}\"\n")
        st.sidebar.success(f"API keys saved to {env_path}")
        return True
    except Exception as e:
        st.sidebar.error(f"Failed to save API keys to .env: {e}")
        return False

# Button to trigger saving API keys to .env
if st.sidebar.button("Save"):
    if gemini_api_key and browserless_api_key and serper_api_key:
        save_api_keys_to_env(gemini_api_key, browserless_api_key, serper_api_key)
    else:
        st.sidebar.warning("Please enter all API keys before saving to .env.")


# --- Main Application Input Fields ---
origin = st.text_input("Origin City", placeholder="e.g., Bangalore")
interests = st.text_input("Your Interests", placeholder="e.g., food, adventure, history")
cities = st.text_input("Cities to Consider (comma-separated)", placeholder="e.g., Paris,London,Berlin")

# Get today's date
today = datetime.date.today()

# Date pickers for start and end dates with min_value set to today
start_date = st.date_input("Start Date", today, min_value=today)
end_date = st.date_input("End Date", today + datetime.timedelta(days=7), min_value=start_date) # End date cannot be before start date


if st.button("Plan My Trip"):
    
    # Ensure end_date is not before start_date (this check is now partly handled by min_value)
    # However, it's good to keep a final check before processing
    if end_date < start_date:
        st.error("End Date cannot be before Start Date. Please adjust your dates.")
    else:
        # Format the date objects to strings for the 'date_range'
        date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"

        # Check if all required fields, including sidebar inputs, are filled
        if not all([origin, interests, cities, selected_gemini_model, gemini_api_key, browserless_api_key, serper_api_key]):
            st.error("Please fill in all the required fields, including all API Keys and Gemini Model in the sidebar.")
        else:
            try:
                with st.spinner("Planning your trip... This might take a moment."):
                    crew = TripCrew(
                        origin=origin,
                        cities=cities,
                        interests=interests,
                        date_range=date_range, # Pass the combined date_range string
                        gemini_model=str('gemini/'+selected_gemini_model)
                    )

                    output = crew.run_crew()

                st.success("Trip Planning Complete!")
                st.subheader("Your Trip Plan:")
                
                
                st.markdown(output)

               
            except Exception as e:
                st.error(f"An error occurred during trip planning: {e}")