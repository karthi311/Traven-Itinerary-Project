import streamlit as st
import requests
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()  
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

# Validate API Key
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Function to fetch Wikipedia summary
def search_travel_info(destination):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{destination}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No information found.")
    return "No results found."

# Function to generate travel itinerary using Groq API
def generate_itinerary(start_location, budget, duration, destination, purpose, preferences):
    search_results = search_travel_info(destination)
    
    # Create prompt template
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are an expert travel guide. Provide a detailed travel itinerary."),
        HumanMessage(content=f"""
            Create a {duration}-day travel itinerary for a traveler going from {start_location} to {destination}.
            
            ### 🏷️ Traveler Information:
            - Budget: {budget}
            - Purpose of Travel: {purpose}
            - Preferences: {preferences}
            
            ### 🚆 Day-wise Itinerary:
            - 📍 Activities (morning, afternoon, evening)
            - 🎭 Attractions (landmarks & hidden gems)
            - 🍽️ Food recommendations
            - 🏨 Accommodation options
            - 🚗 Transportation details
            
            ### 📌 Additional Travel Info:
            {search_results}
        """)
    ])
    
    # Initialize Groq Chat Model (Llama3-8B)
    llm = ChatGroq(temperature=0,model_name="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
    
    # Generate response
    response = llm.invoke(prompt_template.format())
    
    return response.content if response else "Error: Unable to generate itinerary."

# Streamlit UI
st.title("AI-Powered Travel Planner 🧳")
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