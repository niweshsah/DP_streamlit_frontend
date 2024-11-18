import streamlit as st
import requests
import json

# Set page config
# st.set_page_config(
#     page_title="Conference About Section Editor",
#     layout="wide"
# )

# Custom CSSL
def add_custom_css():
    return """
    <style>
        /* General Page Styling */
        .css-1d391kg {background-color: #fafafa;} /* Background color for the page */
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
            margin-top: 20px;
        }
        
        /* Form container styling */
        .form-container {
            padding: 30px;
            border-radius: 10px;
            background-color: #fff;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        
        .form-title {
            color: #333;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        /* Input Styling */
        .stTextInput, .stTextArea {
            font-size: 16px;
            padding: 10px;
            margin-top: 10px;
            width: 100%;
            border-radius: 5px;
            border: 1px solid #ddd;
        }

        /* Button Styling */
        .stButton {
            background-color: #4CAF50;
            color: #fff;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        
        .stButton:hover {
            background-color: #45a049;
        }

        /* Success Message */
        .success-message {
            color: #8bc34a;
            font-size: 16px;
            margin-top: 20px;
        }

        /* Error Message */
        .error-message {
            color: #f44336;
            font-size: 16px;
            margin-top: 20px;
        }

        /* Info Message */
        .info-message {
            color: #2196F3;
            font-size: 16px;
            margin-top: 20px;
        }
        
        /* Column Layout */
        .stColumn {
            margin-top: 20px;
        }

        /* Spinner Styling */
        .css-1v0mbdj { 
            background-color: rgba(0, 0, 0, 0.2);
        }
    </style>
    """

# Load custom CSS
st.markdown(add_custom_css(), unsafe_allow_html=True)

def load_current_about(conference_code):
    """Load the current about section data"""
    try:
        # Replace with your actual API endpoint
        response = requests.get(f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/about")
        if response.status_code == 200:
            data = response.json()
            return data.get('about', {'title': '', 'description': ''})
        return {'title': '', 'description': ''}
    except Exception as e:
        st.error(f"Error loading current data: {str(e)}")
        return {'title': '', 'description': ''}

def update_about_section(conference_code, title, description):
    """Update the about section via API"""
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        payload = {
            'title': title,
            'description': description
        }
        
        response = requests.post(
            f"https://gatherhub-r7yr.onrender.com/user//conference/{conference_code}/eventCard/addAbout",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            st.success("🎉 About section updated successfully!")
            return True
        else:
            st.error(f"❌ Error updating about section: {response.json().get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return False

def main_about():
    st.markdown("<h1 class='title'>✏️ Conference About Section Editor</h1>", unsafe_allow_html=True)
    
    # Conference code input
    conference_code = st.session_state.get('current_user', 'Guest')
    st.write(f"Hello from about tab, {conference_code}!")
    
    if conference_code:
        # Load current about section data
        current_about = load_current_about(conference_code)
        
        # Create form container
        with st.form("about_form", clear_on_submit=True):
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.subheader("Edit About Section 📝")
            
            col1, col2 = st.columns([1, 3])

            # Show current title and allow editing
            col1.write("Current Title:")
            col2.write(f"**{current_about['title']}**")
            new_title = st.text_input("New Title (leave empty to keep current)", "")
            
            # Show current description and allow editing
            col1.write("Current Description:")
            col2.write(f"**{current_about['description']}**")
            new_description = st.text_area("New Description (leave empty to keep current)", "")
            
            # Submit button
            submitted = st.form_submit_button("Update About Section")
            
            if submitted:
                # Use new values if provided, otherwise keep current values
                final_title = new_title if new_title else current_about['title']
                final_description = new_description if new_description else current_about['description']
                
                # Update only if at least one field has changed
                if final_title != current_about['title'] or final_description != current_about['description']:
                    success = update_about_section(
                        conference_code,
                        final_title,
                        final_description
                    )
                    if success:
                        st.balloons()
                else:
                    st.info("🔹 No changes detected")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main_about()
