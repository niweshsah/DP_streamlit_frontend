import streamlit as st
import hashlib
import sqlite3
from datetime import datetime

# Create separate files for different pages
# home.py
def show_home_page():
    st.title("Home Page")
    st.write("Welcome to the Dashboard!")
    
    # Add your dashboard content here
    st.header("Dashboard Content")
    st.write("This is your personalized dashboard.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Sales", value="$12,345", delta="↑ 2.5%")
    
    with col2:
        st.metric(label="Active Users", value="1,234", delta="↑ 15%")
    
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
        st.rerun()

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT,
                  last_login DATETIME)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('SELECT password FROM users WHERE username=?', (username,))
    result = c.fetchone()
    
    if result is not None:
        stored_password = result[0]
        if stored_password == hash_password(password):
            c.execute('UPDATE users SET last_login=? WHERE username=?', 
                     (datetime.now(), username))
            conn.commit()
            conn.close()
            return True
    conn.close()
    return False

def create_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                 (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def show_login_page():
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login_user(login_username, login_password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Username", key="new_username")
        new_password = st.text_input("Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long")
            elif create_user(new_username, new_password):
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists")

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
    
    init_db()
    
    # Show different pages based on login state
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_home_page()

if __name__ == "__main__":
    main()