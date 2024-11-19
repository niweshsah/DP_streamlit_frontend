import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import re

# Configuration
API_BASE_URL = "http://gatherhub-r7yr.onrender.com/user/"

def format_phone_number(number):
    """Format phone number to (XXX) XXX-XXXX or +XX XXXXX XXXXX format"""
    if not number:
        return ""
    
    # Convert to string and remove non-numeric characters
    number_str = re.sub(r'\D', '', str(number))
    
    # Format based on length
    if len(number_str) == 10:  # US format
        return f"({number_str[:3]}) {number_str[3:6]}-{number_str[6:]}"
    elif len(number_str) > 10:  # International format
        return f"+{number_str[:2]} {number_str[2:7]} {number_str[7:]}"
    else:
        return number_str

def validate_phone_number(number):
    """Validate phone number format"""
    if not number:
        return False
    # Remove all non-numeric characters
    number_str = re.sub(r'\D', '', str(number))
    # Check if length is valid (10 digits for domestic, 11-15 for international)
    return 10 <= len(number_str) <= 15

def get_helplines(conference_code):
    """Fetch all helplines for a conference"""
    try:
        response = requests.get(f"{API_BASE_URL}/conference/{conference_code}/eventCard/helplines")
        if response.status_code == 200:
            data = response.json()
            # Format phone numbers in response
            for helpline in data:
                helpline['formatted_number'] = format_phone_number(helpline['number'])
            return data
        else:
            st.error(f"Error fetching helplines: {response.json()['message']}")
            return []
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        return []

def add_helpline(conference_code, name, number):
    """Add a new helpline"""
    try:
        # Remove any formatting from the number before sending
        clean_number = re.sub(r'\D', '', str(number))
        response = requests.post(
            f"{API_BASE_URL}/conference/{conference_code}/eventCard/addNewHelpline",
            json={"name": name, "number": int(clean_number)}
        )
        if response.status_code == 200:
            st.success("✅ Helpline added successfully!")
            return True
        else:
            st.error(f"❌ Error adding helpline: {response.json()['message']}")
            return False
    except Exception as e:
        st.error(f"❌ Error connecting to server: {str(e)}")
        return False

def delete_helpline(conference_code, name):
    """Delete a helpline"""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/conference/{conference_code}/eventCard/helpline/{name}"
        )
        if response.status_code == 200:
            st.success("✅ Helpline deleted successfully!")
            return True
        else:
            st.error(f"❌ Error deleting helpline: {response.json()['message']}")
            return False
    except Exception as e:
        st.error(f"❌ Error connecting to server: {str(e)}")
        return False

def main_helpline():
    # Custom CSS for better styling and visibility
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
            padding: 0.5rem;
        }
        .helpline-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 0.8rem 0;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .helpline-card:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .helpline-name {
            color: #1f1f1f;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .number-display {
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
            color: #2c5282;
            background-color: #ebf8ff;
            padding: 0.5rem;
            border-radius: 0.3rem;
            display: inline-block;
        }
        /* Updated button styling */
        .stButton button {
            width: 100%;
            background-color: #f0f0f0; /* Neutral light gray */
            color: #333333; /* Dark text color for contrast */
            border: 1px solid #d0d0d0; /* Subtle border for definition */
            border-radius: 0.3rem;
            padding: 0.6rem;
            transition: all 0.2s ease;
        }
        .stButton button:hover {
            background-color: #e0e0e0; /* Slightly darker gray on hover */
            border-color: #b0b0b0;
        }
        /* Delete button styling */
        .delete-button button {
            background-color: #fc8181; /* Soft red */
            color: white;
        }
        .delete-button button:hover {
            background-color: #f56565; /* Brighter red on hover */
        }
        .st-emotion-cache-18ni7ap {
            background-color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📞 Conference Helpline Management")
    
    conference_code = st.session_state.get('current_user', 'Guest')
    
    if conference_code:
        tab1, tab2, tab3 = st.tabs([
            "📋 View Helplines",
            "➕ Add Helpline",
            "🗑️ Delete Helpline"
        ])
        
        with tab1:
            st.header("Current Helplines")
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("🔄 Refresh", key="refresh"):
                    st.session_state.helplines = get_helplines(conference_code)
            
            if 'helplines' not in st.session_state:
                st.session_state.helplines = get_helplines(conference_code)
            
            if st.session_state.helplines:
                for helpline in st.session_state.helplines:
                    with st.container():
                        st.markdown(f"""
                            <div class="helpline-card">
                                <div class="helpline-name">{helpline['name']}</div>
                                <div class="number-display">{format_phone_number(helpline['number'])}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("📭 No helplines found for this conference.")
        
        with tab2:
            st.header("Add New Helpline")
            with st.form("add_helpline_form"):
                name = st.text_input("👤 Contact Name", placeholder="Enter contact name")
                phone_input = st.text_input(
                    "📱 Contact Number",
                    placeholder="Enter 10-digit number",
                    help="Enter number in format: 1234567890 or +1234567890"
                )
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submit_button = st.form_submit_button("➕ Add Helpline")
                
                if submit_button:
                    if name and phone_input:
                        if validate_phone_number(phone_input):
                            if add_helpline(conference_code, name, phone_input):
                                st.session_state.helplines = get_helplines(conference_code)
                        else:
                            st.error("❌ Please enter a valid phone number (10-15 digits)")
                    else:
                        st.warning("⚠️ Please fill in both name and number.")
        
        with tab3:
            st.header("Delete Helpline")
            if st.session_state.helplines:
                helpline_names = [h['name'] for h in st.session_state.helplines]
                name_to_delete = st.selectbox(
                    "Select Helpline to Delete",
                    options=helpline_names
                )
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🗑️ Delete Selected Helpline", type="primary", use_container_width=True):
                        if delete_helpline(conference_code, name_to_delete):
                            st.session_state.helplines = get_helplines(conference_code)
            else:
                st.info("📭 No helplines available to delete.")
    
    else:
        st.info("👋 Please enter a conference code to manage helplines.")

    # Footer with styling
    st.markdown("""
        <style>
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #ffffff;
                padding: 10px;
                text-align: center;
                border-top: 1px solid #e0e0e0;
                color: #4a5568;
            }
        </style>
        <div class="footer">
            🌟 Conference Helpline Management System
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main_helpline()