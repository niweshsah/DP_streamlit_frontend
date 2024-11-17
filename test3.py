import streamlit as st
import hashlib
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
def connect_to_mongodb():
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://sahniwesh:Cg1pipueVvULDzdk@testing.4soqq.mongodb.net/')
    client = MongoClient(MONGO_URI)
    db = client['conferences']
    return db

def show_home_page():
    st.title("Home Page")
    st.write(f"Welcome to the Dashboard, {st.session_state.eventname}!")
    
    # Add your dashboard content here
    st.header("Dashboard Content")
    st.write("This is your personalized dashboard.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Sales", value="$12,345", delta="↑ 2.5%")
    
    with col2:
        st.metric(label="Active events", value="1,234", delta="↑ 15%")
    
    with col3:
        st.metric(label="Performance", value="98%", delta="↑ 4%")
    
    # Example chart
    chart_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Value': [10, 20, 15, 25, 30]
    }
    st.line_chart(chart_data)
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.eventname = None
        st.rerun()

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def login_event(eventname, password):
    db = connect_to_mongodb()
    events_collection = db['events']
    
    # Find event
    event = events_collection.find_one({'eventname': eventname})
    
    if event and event['password'] == hash_password(password):
        # Update last login
        events_collection.update_one(
            {'eventname': eventname},
            {
                '$set': {
                    'last_login': datetime.now()
                }
            }
        )
        return True
    return False

def create_event(eventname, password):
    db = connect_to_mongodb()
    events_collection = db['events']
    
    # Check if eventname already exists
    if events_collection.find_one({'eventname': eventname}):
        return False
    
    # Create new event
    event_data = {
        'eventname': eventname,
        'password': hash_password(password),
        'created_at': datetime.now(),
        'last_login': None
    }
    
    try:
        events_collection.insert_one(event_data)
        return True
    except Exception as e:
        print(f"Error creating event: {e}")
        return False

def show_login_page():
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        login_eventname = st.text_input("eventname", key="login_eventname")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login_event(login_eventname, login_password):
                st.session_state.logged_in = True
                st.session_state.eventname = login_eventname
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid eventname or password")
    
    with tab2:
        st.subheader("Create New Account")
        new_eventname = st.text_input("eventname", key="new_eventname")
        new_password = st.text_input("Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long")
            elif create_event(new_eventname, new_password):
                st.success("Account created successfully! Please login.")
            else:
                st.error("eventname already exists")

def main():
    st.set_page_config(page_title="Login System", layout="centered")
    
    # Add custom CSS
    st.markdown("""
        <style>
        .stButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
        .stTextInput>div>div>input {
            color: #4A4A4A;
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.eventname = None
    
    # Show different pages based on login state
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_home_page()

if __name__ == "__main__":
    main()