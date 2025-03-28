import streamlit as st
import requests
from transformers import pipeline

# Load Hugging Face Model
pipe = pipeline("text-generation", model="unsloth/Llama-3.2-1B", max_length=1024, pad_token_id=50256)

# Function to fetch Wikipedia summary
def search_travel_info(destination):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{destination}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No information found.")
    return "No results found."

# Function to generate travel itinerary
def generate_itinerary(start_location, budget, duration, destination, purpose, preferences):
    search_results = search_travel_info(destination)
    
    # System Prompt
    system_prompt = "You are an expert travel guide. Your goal is to create a well-structured, detailed itinerary based on the user's preferences."

    # User Prompt
    user_prompt = f"""
    {system_prompt}

    ### 🏷️ **Traveler Information**:
    - **Budget**: {budget}
    - **Purpose of Travel**: {purpose}
    - **Preferences**: {preferences}

    ### 🚆 **Day-wise Itinerary**:
    - 📍 Day-by-day activities, including morning, afternoon, and evening plans
    - 🎭 Must-visit attractions (famous landmarks + hidden gems)
    - 🍽️ Local cuisines and top dining recommendations
    - 🏨 Best places to stay (based on budget)
    - 🚗 Transportation options (from {start_location} to {destination} and local travel)

    ### 📌 **Additional Considerations**:
    - 🌎 Cultural experiences, festivals, or seasonal events
    - 🛍️ Shopping and souvenir recommendations
    - 🔹 Safety tips, best times to visit, and local customs
    - 🗺️ Alternative plans for bad weather days

    ### ℹ️ **Additional Information from External Sources**:
    {search_results}

    Make sure the itinerary is engaging, practical, and customized based on the user’s budget and preferences.
    """

    # Generate Response
    response = pipe(user_prompt)[0]["generated_text"]
    return response

# Streamlit UI
st.title("AI-Powered Travel Planner")
st.write("Plan your next trip with AI!")

start_location = st.text_input("Starting Location")
destination = st.text_input("Destination")
budget = st.selectbox("Select Budget", ["Low", "Moderate", "Luxury"])
duration = st.number_input("Trip Duration (days)", min_value=1, max_value=30, value=3)
purpose = st.text_area("Purpose of Trip")
preferences = st.text_area("Your Preferences (e.g., adventure, food, history)")

if st.button("Generate Itinerary"):
    if start_location and destination and purpose and preferences:
        itinerary = generate_itinerary(start_location, budget, duration, destination, purpose, preferences)
        st.subheader("Your AI-Generated Itinerary:")
        st.write(itinerary)
    else:
        st.warning("Please fill in all fields.")


