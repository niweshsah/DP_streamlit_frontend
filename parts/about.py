import streamlit as st
import requests
import json

def load_current_about(conference_code):
    """Load the current about section data"""
    try:
        # Replace with your actual API endpoint
        response = requests.get(f"http://localhost:27017/user/conference/{conference_code}/eventCard/about")
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
            f"http://localhost:27017/user/conference/{conference_code}/eventCard/addAbout",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            st.success("About section updated successfully!")
            return True
        else:
            st.error(f"Error updating about section: {response.json().get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def main_about():
    st.title("Conference About Section Editor")
    
    # Conference code input
    # conference_code = st.text_input("Enter Conference Code")
    
    conference_code = st.session_state.get('current_user', 'Guest')
    print(f"Hello from about tab, {conference_code}!")
    
    if conference_code:
        # Load current about section data
        current_about = load_current_about(conference_code)
        
        # Create form
        with st.form("about_form"):
            st.subheader("Edit About Section")
            
            # Show current title and allow editing
            st.text("Current Title: " + current_about['title'])
            new_title = st.text_input("New Title (leave empty to keep current)", "")
            
            # Show current description and allow editing
            st.text("Current Description: " + current_about['description'])
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
                    st.info("No changes detected")

if __name__ == "__main__":
    main_about()