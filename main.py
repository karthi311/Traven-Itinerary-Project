import streamlit as st
import requests
import subprocess
import platform
import os
import ollama

# Function to download a file with progress bar
def download_file(url, output_path):
    # st.write(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 64000  # 64 KB chunks

    progress_bar = st.progress(0)
    downloaded = 0

    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)
                progress_bar.progress(downloaded / total_size)

    # st.success(f"Downloaded {output_path} successfully.")
    print(f"Downloaded {output_path} successfully.")
    

# Function to install Ollama
def install_ollama():
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # st.success("✅ Ollama is already installed.")
        print("✅ Ollama is already installed.")
        return True
    except FileNotFoundError:
        # st.warning("⚙️ Ollama is not installed. Installing now...")
        print("⚙️ Ollama is not installed. Installing now...")
        system = platform.system().lower()

        if system == "windows":
            installer_url = "https://ollama.ai/download/OllamaSetup.exe"
            installer_path = "OllamaSetup.exe"

            download_file(installer_url, installer_path)
            subprocess.run([installer_path, "/S"], check=True)
            os.remove(installer_path)

            # st.success("✅ Ollama installed successfully on Windows.")
            print("✅ Ollama installed successfully on Windows.")
            return True

        elif system == "linux":
            subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
            # st.success("✅ Ollama installed successfully on Ubuntu.")
            print("✅ Ollama installed successfully on Ubuntu.")
            return True

        elif system == "darwin":
            subprocess.run("brew install ollama", shell=True, check=True)
            # st.success("✅ Ollama installed successfully on macOS.")
            print("✅ Ollama installed successfully on macOS.")
            return True

        else:
            # st.error(f"❌ Unsupported OS: {system}")
            print(f"❌ Unsupported OS: {system}")
            
            return False

# Function to download LLaMA model
def download_llama_model(model_name="llama3.2:1b"):
    # st.write(f"🚀 Downloading {model_name} using Ollama...")
    print(f"🚀 Downloading {model_name} using Ollama...")
    
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        # st.success(f"✅ Model {model_name} downloaded successfully.")
        print(f"✅ Model {model_name} downloaded successfully.")
        
    except subprocess.CalledProcessError as e:
        # st.error(f"❌ Failed to download {model_name}: {e}")
        print(f"❌ Failed to download {model_name}: {e}")
        

# Install Ollama & Download Model on Startup
if install_ollama():
    download_llama_model()

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
    prompt = f"""
        You are an expert travel planner. Create a detailed {duration}-day travel itinerary for a traveler going from {start_location} to {destination}. 

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

    response = ollama.chat(model="llama3.2:1b", messages=[{"role": "system", "content": "You are an expert travel guide."},
                                                     {"role": "user", "content": prompt}])
    return response["message"]["content"]

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

