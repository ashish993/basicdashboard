import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time

# Set page configuration
st.set_page_config(
    page_title="Restaurant Booking Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define color scheme
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#E74C3C',
    'background': '#ECF0F1',
    'text': '#2C3E50',
    'accent': '#3498DB'
}

# Add auto-refresh
if 'refresh_counter' not in st.session_state:
    st.session_state.refresh_counter = 0

st.session_state.refresh_counter += 1

# Custom CSS for modern card styling
st.markdown(f"""
    <style>
    .main-header {{
        color: {COLORS['primary']};
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 2rem 0;
        padding: 1.5rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .booking-card {{
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .booking-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}
    
    .customer-name {{
        color: {COLORS['primary']};
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    
    .booking-details {{
        color: {COLORS['text']};
        font-size: 1.1rem;
        margin: 0.5rem 0;
    }}
    
    .guest-count {{
        background-color: {COLORS['accent']};
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
    }}
    
    .date-time {{
        color: {COLORS['secondary']};
        font-weight: 500;
    }}
    
    .stApp {{
        background-color: {COLORS['background']};
    }}

    div[data-testid="stHorizontalBlock"] {{
        gap: 2rem;
        padding: 0.5rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<p class="big-font">🍽️ Restaurant Booking Dashboard</p>', unsafe_allow_html=True)

def fetch_bookings():
    try:
        response = requests.get('https://basicapi1310.azurewebsites.net/api/bookings')
        if response.status_code == 200:
            data = response.json()
            # Convert to DataFrame and clean data
            df = pd.DataFrame(data)
            # Remove rows with null or empty values
            df = df.dropna()
            df = df[df['name'] != '']
            df = df[df['totalPax'] != 'None']
            # Convert totalPax to numeric
            df['totalPax'] = pd.to_numeric(df['totalPax'])
            # Convert date to datetime and format it
            df['date'] = pd.to_datetime(df['date'])
            df['date'] = df['date'].dt.strftime('%d-%b')
            # Sort by ID in descending order
            df = df.sort_values('id', ascending=False)
            return df
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def create_booking_card(name, total_pax, date, time):
    return f"""
    <div class="booking-card">
        <div class="customer-name">👤 {name}</div>
        <div class="booking-details">
            <span class="guest-count">🪑 {total_pax} Guests</span>
        </div>
        <div class="booking-details date-time">
            📅 {date} at ⏰ {time}
        </div>
    </div>
    """

def main():
    # Display title
    st.markdown('<h1 class="main-header">🍽️ Restaurant Booking System</h1>', unsafe_allow_html=True)
    
    # Fetch data
    df = fetch_bookings()
    
    if df is not None:
        # Create a container for the cards
        container = st.container()
        
        # Display bookings in a grid layout
        cols = st.columns(3)  # Create 3 columns
        
        # Iterate through the bookings and create cards
        for idx, row in df.iterrows():
            with cols[idx % 3]:  # Distribute cards across columns
                st.markdown(
                    create_booking_card(
                        row['name'],
                        int(float(row['totalPax'])),
                        row['date'],
                        row['time']
                    ),
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()
    # Auto refresh every 3 seconds
    time.sleep(3)
    st.rerun()
