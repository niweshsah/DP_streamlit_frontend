import streamlit as st
import requests
import datetime
from datetime import datetime as dt

def main_event():
    # Streamlit page configuration
    # st.set_page_config(page_title="Conference Event Manager", layout="centered")

    # Define API URL
    API_BASE_URL = "http://localhost:27017/user/conference/"

    # Select POST or DELETE operation
    operation = st.radio("Choose an operation:", ["Add Events", "Delete Events"])

    # Common Inputs
    # conference_code = st.text_input("Conference Code", placeholder="Enter conference code (e.g., AI2024)")
    conference_code = st.session_state.get('current_user', 'Guest')
    # st.write(f"Hello, {conference_code}!")
    print(f"Hello, {conference_code}!")
    
    date = st.date_input("Event Date").strftime('%Y-%m-%d')

    def format_time_12hr(hour, minute):
        time = dt.strptime(f"{hour:02}:{minute:02}", "%H:%M")
        return time.strftime("%I:%M %p").strip()

    # Custom Clock Input (Hour and Minute)
    def clock_input(label):
        st.subheader(label)
        
        col1, col2 = st.columns(2)
        
        with col1:
            hour = st.selectbox("Hour", list(range(0, 24)), format_func=lambda x: f"{x:02}")
        with col2:
            minute = st.selectbox("Minute", list(range(0, 60)), format_func=lambda x: f"{x:02}")
        
        return hour, minute

    # POST Operation: Add New Events
    if operation == "Add Events":
        st.header("Add New Events")

        # Input for single event
        event_title = st.text_input("Event Title", placeholder="Enter event title")
        hour, minute = clock_input("Event Time")
        event_time = format_time_12hr(hour, minute)
        event_venue = st.text_input("Event Venue", placeholder="Enter event venue")

        # Submit single event
        if st.button("Submit Event"):
            if conference_code and date and event_title and event_time and event_venue:
                event_data = {
                    "date": date,
                    "title": event_title,
                    "time": event_time,
                    "venue": event_venue
                }

                response = requests.post(
                    f"{API_BASE_URL}/{conference_code}/eventCard/addNewEvent",
                    json=event_data
                )

                if response.status_code == 200:
                    st.success(f"Event '{event_title}' added successfully!")
                else:
                    st.error(f"Failed to add event: {response.text}")
            else:
                st.error("Please fill in all fields (Conference Code, Date, Title, Time, and Venue).")

    # DELETE Operation: Delete Events
    elif operation == "Delete Events":
        st.header("Delete Events")

        event_titles_to_delete = st.text_area(
            "Event Titles to Delete", 
            placeholder="Enter event titles separated by commas (e.g., Keynote Speech, Networking Session)"
        )

        if st.button("Delete Events"):
            titles_list = [title.strip() for title in event_titles_to_delete.split(",") if title.strip()]

            if conference_code and date and titles_list:
                response = requests.delete(
                    f"{API_BASE_URL}/{conference_code}/eventCard/{date}",
                    json={"eventTitles": titles_list}
                )
                if response.status_code == 200:
                    st.success("Events deleted successfully!")
                else:
                    st.error(f"Failed to delete events: {response.text}")
            else:
                st.error("Please provide Conference Code, Date, and Event Titles.")

# Run the main function
if __name__ == "__main__":
    main_event()