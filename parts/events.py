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
    operation = st.radio("Choose an operation:", ["📅 Add Events", "🗑️ Delete Events"])

    # Common Inputs
    conference_code = st.session_state.get('current_user', 'Guest')
    print(f"Hello, {conference_code}!")
    
    date = st.date_input("Event Date").strftime('%Y-%m-%d')

    # Custom time formatting
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

    # Custom CSS for styling
    st.markdown("""
        <style>
        .main-container {
            padding: 2rem;
        }
        .event-form input, .event-form select {
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-radius: 0.25rem;
            border: 1px solid #ddd;
        }
        .event-card {
            background-color: #fff;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .event-card:hover {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .event-header {
            color: #1f1f1f;
            font-size: 1.5rem;
            font-weight: 600;
        }
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
    """, unsafe_allow_html=True)

    # Main Layout
    st.title("🎉 Conference Event Manager")
    
    with st.container():
        if operation == "📅 Add Events":
            st.header("Add New Events")

            # Form for Adding Event
            with st.form("event_add_form"):
                event_title = st.text_input("Event Title", placeholder="Enter event title")
                hour, minute = clock_input("Event Time")
                event_time = format_time_12hr(hour, minute)
                event_venue = st.text_input("Event Venue", placeholder="Enter event venue")

                submit_button = st.form_submit_button("Submit Event")

                if submit_button:
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

        elif operation == "🗑️ Delete Events":
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

    # Footer with styling
    st.markdown("""
        <div class="footer">
            🌟 Conference Event Manager
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main_event()
