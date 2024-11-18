import streamlit as st
import requests
import json
from datetime import datetime
from home import main_home


# Configure page settings
# st.set_page_config(page_title="Conference Login System", layout="centered")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
    



# API endpoints
BASE_URL = "https://gatherhub-r7yr.onrender.com/user/conference/"  # Replace with your actual API base URL
# BASE_URL = "http://localhost:27017/user/conference/"  # Replace with your actual API base URL
ENDPOINTS = {
    'login': f"{BASE_URL}/login",
    'create_account': f"{BASE_URL}/createNewConference",
    'check_username': f"{BASE_URL}/checkConferenceCode"
}



def check_conference_code(conference_code):
    """Check if conference code is available"""
    try:
        response = requests.post(
            ENDPOINTS['check_username'],
            json={'conferenceCode': conference_code}
        )
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        return False



def create_account(user_data):
    """Create a new account"""
    try:
        response = requests.post(
            ENDPOINTS['create_account'],
            json=user_data
        )
        return response.status_code == 200, response.json()
    except requests.exceptions.RequestException as e:
        return False, {'error': str(e)}





def login(conference_code, password):
    """Authenticate user"""
    try:
        response = requests.post(
            ENDPOINTS['login'],
            json={
                'conferenceCode': conference_code,
                'password': password
            }
        )
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        return False, None




def show_login_page():
    """Display login form"""
    st.title("Conference Login")
    
    with st.form("login_form"):
        conference_code = st.text_input("Conference Code")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if not conference_code or not password:
                st.error("Please fill in all fields")
            else:
                success, user_data = login(conference_code, password)
                print("user data: ", user_data)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_data
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")




def show_signup_page():
    """Display signup form"""
    st.title("Create Conference Account")
    
    with st.form("signup_form"):
        conference_code = st.text_input("Conference Code")
        name = st.text_input("Name")
        location = st.text_input("Location")
        # time = st.date_input("Time")
        time = st.date_input("Time")
        time2 = time.isoformat()  # Converts to YYYY-MM-DD format
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit_button = st.form_submit_button("Create Account")
        
        if submit_button:
            if not all([conference_code, name, location, time2, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                # Check if conference code is available
                if check_conference_code(conference_code):
                    print("time: ",time2)
                    user_data = {
                    "name": name,
                    "startDate": time2,
                    # "endDate": "2024-12-03T17:00:00Z",
                    "conferenceCode": conference_code,
                    "password": password,
                    "location": location
                                }
                    success, response = create_account(user_data)
                    if success:
                        st.success("Account created successfully! Please login.")
                        st.session_state.show_login = True
                        st.rerun()
                    else:
                        st.error(f"Error creating account: {response.get('error', 'Unknown error')}")
                else:
                    st.error("Conference code is already taken")





def show_logged_in_page():
    """Display logged in user's dashboard"""
    # st.title("Welcome to Your Dashboard")
    # st.write(f"Welcome back!")
    main_home()
    
    
   

def main():
    """Main application logic"""
    # Initialize session state for page navigation
    if 'show_login' not in st.session_state:
        st.session_state.show_login = True

    # Sidebar for navigation
    if not st.session_state.logged_in:
        with st.sidebar:
            if st.button("Login" if not st.session_state.show_login else "Sign Up"):
                st.session_state.show_login = not st.session_state.show_login
                st.rerun()

        if st.session_state.show_login:
            show_login_page()
        else:
            show_signup_page()
    else:
        show_logged_in_page()

if __name__ == "__main__":
    main()