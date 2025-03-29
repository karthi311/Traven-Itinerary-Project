# Travel-Itinerary-Project


# AI-Powered Travel Planner 🏝️✈️

An AI-driven travel itinerary generator that creates customized travel plans based on user preferences, budget, and duration. This app uses **Streamlit**, **Grow (llama-3.3-70b-versatile)**, and **Wikipedia API** to provide detailed travel recommendations.

## 🚀 Features
- Generates multi-day travel itineraries based on user input.
- Suggests **famous attractions, hidden gems, food spots, and accommodations**.
- Includes **transportation options, cultural experiences, and local events**.
- Fetches relevant travel information from **Wikipedia**.
- Simple **Streamlit UI** for easy interaction.

## 🛠️ Technologies & Libraries Used
- **Python**: Core programming language
- **Streamlit**: Web-based UI framework
- **GroqAPIKEY**: llama-3.3-70b-versatile model for itinerary generation
- **Requests**: API calls to fetch travel information
- **Wikipedia API**: Fetches destination details

## 🎯 How It Works
1. User enters **starting location, destination, budget, trip duration, purpose, and preferences**.
2. The app **fetches information** from Wikipedia about the destination.
3. A **detailed itinerary** is generated using **Groq(llama-3.3-70b-versatile)**.
4. The AI-generated travel plan is displayed in the **Streamlit UI**.

## 📌 Installation Guide

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/karthi311/Traven-Itinerary-Project.git
cd Traven-Itinerary-Project
```

### 2️⃣ Install Dependencies

Make sure you have Python 3.8+ installed. Then, run:
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit App

Start the app using:

```sh
streamlit run app.py
```

## 📜 License

This project is open-source. Feel free to modify and improve it!
