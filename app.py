import streamlit as st
import pandas as pd
import numpy as np
import random
import folium
from folium.plugins import MarkerCluster
import plotly.express as px
import streamlit.components.v1 as components

# --- Page config ---
st.set_page_config(page_title="Australian House Price Predictor 🏡", layout="centered")

# --- Title ---
st.title("🏡 Australian House Price Predictor & Suburb Recommender")
st.write("Find your dream suburb based on your budget, room preferences, and lifestyle needs in Australia!")

# --- Suburbs List ---
suburbs = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra", "Hobart", "Darwin"]

# --- User Inputs ---
st.header("🔎 Search Filters")
col1, col2 = st.columns(2)

with col1:
    suburb = st.selectbox("Choose a Suburb", suburbs)
    rooms = st.slider("Select Number of Bedrooms", 1, 6)
    budget = st.slider("Your Budget (AUD)", 300000, 2000000, step=50000)
    
with col2:
    near_transport = st.checkbox("🚉 Require Public Transport Nearby?")
    pet_friendly = st.checkbox("🐶 Pet Friendly Housing?")
    low_crime = st.checkbox("🛡️ Prefer Low Crime Area?")

# --- Function to generate interactive map ---
def generate_map():
    m = folium.Map(location=[-25.2744, 133.7751], zoom_start=5, tiles="Stamen Terrain")
    marker_cluster = MarkerCluster().add_to(m)

    suburb_data = {
        "Sydney": [-33.8688, 151.2093, 1200000],
        "Melbourne": [-37.8136, 144.9631, 950000],
        "Brisbane": [-27.4698, 153.0251, 800000],
        "Perth": [-31.9505, 115.8605, 750000]
    }

    for suburb, data in suburb_data.items():
        folium.Marker(
            location=[data[0], data[1]],
            popup=f"{suburb}: ${data[2]:,.0f}",
            icon=folium.Icon(color="blue")
        ).add_to(marker_cluster)

    return m

# --- Show map in Streamlit ---
st.header("📍 House Prices in Different Suburbs")
st.write("Click on a marker to see the estimated price.")
map_ = generate_map()
st.markdown(f'<iframe srcdoc="{map_._repr_html_()}" width="100%" height="500"></iframe>', unsafe_allow_html=True)

# --- Simulate a prediction ---
st.header("🏠 Your Results")

# Fake logic to simulate price prediction
base_price = random.randint(400000, 1200000)
price_adjustment = rooms * 25000
location_factor = suburbs.index(suburb) * 30000
feature_bonus = 0

if near_transport:
    feature_bonus += 20000
if pet_friendly:
    feature_bonus += 15000
if low_crime:
    feature_bonus += 25000

predicted_price = base_price + price_adjustment + location_factor + feature_bonus

# --- Show prediction ---
st.subheader(f"Predicted House Price in {suburb}:")
st.success(f"Around **${predicted_price:,.0f} AUD** 🏡")

# --- Recommend if fits budget ---
if predicted_price <= budget:
    st.balloons()
    st.success(f"🎯 Great choice! This property fits your budget of **${budget:,.0f} AUD**.")
else:
    st.warning(f"⚡ Oops! You might need to increase your budget by about **${predicted_price - budget:,.0f} AUD**.")

# --- Suburb Comparison ---
st.header("🔍 Suburb Comparison")
suburb1 = st.selectbox("Choose First Suburb", suburbs, key="suburb1")
suburb2 = st.selectbox("Choose Second Suburb", suburbs, key="suburb2")

# Simulate the logic for price prediction for both suburbs
def compare_suburbs(suburb1, suburb2):
    price1 = random.randint(400000, 1200000) + rooms * 25000 + suburbs.index(suburb1) * 30000
    price2 = random.randint(400000, 1200000) + rooms * 25000 + suburbs.index(suburb2) * 30000
    return price1, price2

price1, price2 = compare_suburbs(suburb1, suburb2)

# Display comparison
st.write(f"**{suburb1} Price**: ${price1:,.0f}")
st.write(f"**{suburb2} Price**: ${price2:,.0f}")

# --- Price Trend (Simulated Data) ---
def plot_price_trends(suburb):
    years = np.arange(2015, 2025)
    prices = [random.randint(500000, 800000) + random.randint(0, 100000) for _ in years]

    fig = px.line(x=years, y=prices, labels={'x': "Year", 'y': "Price (AUD)"}, title=f"Price Trend for {suburb}")
    st.plotly_chart(fig)

# Call the function to display the trend of selected suburb
plot_price_trends(suburb)

# --- Personalized Recommendation ---
def recommend_suburbs(budget, near_transport, pet_friendly, low_crime):
    recommendations = []
    for suburb in suburbs:
        score = 0
        price = random.randint(400000, 1200000) + rooms * 25000 + suburbs.index(suburb) * 30000
        
        if price <= budget:
            score += 1
        if near_transport:
            score += 1
        if pet_friendly:
            score += 1
        if low_crime:
            score += 1
        
        recommendations.append((suburb, score, price))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)  # Sort by score
    return recommendations

recommendations = recommend_suburbs(budget, near_transport, pet_friendly, low_crime)

# Display top 3 recommended suburbs
st.header("🌟 Recommended Suburbs for You")
for suburb, score, price in recommendations[:3]:
    st.write(f"**{suburb}**: ${price:,.0f} (Score: {score})")

# --- Social Media Sharing ---
st.header("📱 Share Your Results")
st.write("Share your results with your friends on social media!")
components.html('<a href="https://twitter.com/intent/tweet?text=Check%20out%20this%20Australian%20House%20Price%20Predictor!%20'+str(predicted_price)+'%20AUD&url=https://yourwebsite.com" target="_blank">Share on Twitter</a>', height=30)

# --- Footer ---
st.write("---")
st.caption("Made with ❤️ for the Australian Data Science Market!")
