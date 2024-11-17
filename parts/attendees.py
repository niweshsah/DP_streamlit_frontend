import streamlit as st
import requests
import pandas as pd
from typing import List, Dict

def fetch_attendees(url: str) -> List[Dict]:
    """Fetch attendees from the API"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching attendees: {str(e)}")
        return []

def post_selected_attendees(url: str, selected_attendees: List[Dict]) -> bool:
    """Post selected attendees to the API"""
    try:
        payload = {"attendees": selected_attendees}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        st.error(f"Error posting attendees: {str(e)}")
        return False

def main_add_attendee():
    st.title("Conference Attendee Management")
    
    conference_code = st.session_state.get('current_user', 'Guest')
    print(f"Hello, {conference_code}!")
    
    fetch_url = "http://localhost:27017/user/"
    post_url = f"http://localhost:27017/user/conference/{conference_code}/eventCard/registerAttendees"
    
    # Configuration section with URLs
    # with st.sidebar:
    #     st.header("Configuration")
    #     fetch_url = st.text_input(
    #         "Fetch URL",
    #         value="http://localhost:27017/user/",
    #         help="Enter the URL to fetch attendees from"
    #     )
    #     post_url = st.text_input(
    #         "Post URL",
    #         value="http://localhost:27017/user/conference/abcdef/eventCard/registerAttendees",
    #         help="Enter the URL to post selected attendees to"
    #     )

    # Fetch button with loading state
    if st.button("Fetch Attendees", type="primary"):
        with st.spinner("Fetching attendees..."):
            attendees_data = fetch_attendees(fetch_url)
            
            if attendees_data:
                # Store the fetched data in session state
                st.session_state.attendees = attendees_data
                st.success("Successfully fetched attendees!")
            else:
                st.error("No attendees data received")

    # Display attendees if they exist in session state
    if hasattr(st.session_state, 'attendees'):
        st.header("Available Attendees")
        
        # Convert attendees to DataFrame for better display
        df = pd.DataFrame(st.session_state.attendees)
        
        # Create selection interface
        if not df.empty:
            # Create multiselect using attendee information
            selected_indices = st.multiselect(
                "Select Attendees",
                range(len(df)),
                format_func=lambda x: f"{df.iloc[x]['name']} ({df.iloc[x]['email']})",
                help="Select the attendees you want to register"
            )
            
            # Display selected attendees in a table
            if selected_indices:
                st.subheader("Selected Attendees")
                selected_df = df.iloc[selected_indices][['name', 'username', 'email']]
                st.dataframe(selected_df, use_container_width=True)
                
                # Submit button for selected attendees
                # if st.button("Submit Selected Attendees", type="primary"):
                #     selected_attendees = df.iloc[selected_indices].to_dict('records')
                #     # Make a GET request to an external API (e.g., OpenWeather API)
                #     response = requests.get('http://localhost:27017/user/conference/qwerty/eventCard/email/sendEmails')

                #     if response.status_code == 200:
                #         # Process and display the data from the response
                #         data = response.json()
                #         st.write(data)  # Display the data in Streamlit
                #     else:
                #         # st.write(f"Error: {response.status_code}")
                #         st.error("Failed to send Email")
                        
                    
                #     with st.spinner("Submitting selected attendees..."):
                #         if post_selected_attendees(post_url, selected_attendees):
                #             st.success(f"Successfully submitted {len(selected_attendees)} attendees!")
                            
                #             # Show detailed success message
                #             st.write("Submitted the following attendees:")
                #             for attendee in selected_attendees:
                #                 st.write(f"✓ {attendee['name']} ({attendee['email']})")
                #         else:
                #             st.error("Failed to submit attendees")
                if st.button("Submit Selected Attendees", type="primary"):
                    # Extract selected attendees from the DataFrame (or other source)
                    selected_attendees = df.iloc[selected_indices].to_dict('records')

                    # Show spinner while waiting for the response
                    with st.spinner("Sending emails..."):
                        # Make a GET request to the external API
                        response = requests.get('http://localhost:27017/user/conference/qwerty/eventCard/email/sendEmails')

                        # Wait for the response and handle it
                        if response.status_code == 200:
                            # Process the successful response
                            data = response.json()  # assuming the response is in JSON format
                            st.write(data)  # Display the data in Streamlit
                        else:
                            # Display an error message if the API call fails
                            st.error(f"Error: {response.status_code} - Failed to send emails")

                    # Proceed with submitting the selected attendees only after receiving the response
                    with st.spinner("Submitting selected attendees..."):
                        if post_selected_attendees(post_url, selected_attendees):  # Replace with your actual function
                            st.success(f"Successfully submitted {len(selected_attendees)} attendees!")

                            # Display the submitted attendees
                            st.write("Submitted the following attendees:")
                            for attendee in selected_attendees:
                                st.write(f"✓ {attendee['name']} ({attendee['email']})")
                        else:
                            st.error("Failed to submit attendees")
                            
            
            
            # Add a button to clear the selection
            if st.button("Clear Selection"):
                st.session_state.attendees = []
                st.rerun()
        else:
            st.info("No attendees available to display")

    # Add some helpful instructions
    # with st.sidebar:
    #     st.markdown("""
    #     ### Instructions
    #     1. Enter the API URLs in the configuration section
    #     2. Click 'Fetch Attendees' to load the list
    #     3. Select attendees from the list
    #     4. Click 'Submit' to register selected attendees
        
    #     ### Tips
    #     - You can select multiple attendees at once
    #     - Use the search box in the multiselect to find specific attendees
    #     - Click 'Clear Selection' to start over
    #     """)

if __name__ == "__main__":
    main_add_attendee()