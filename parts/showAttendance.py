import streamlit as st
import requests

conference_code = st.session_state.get('current_user', 'Guest')
print(f"Hello, {conference_code}!")


# Backend API URLs
ATTENDEES_FALSE_URL = f"http://localhost:27017/user/conference/{conference_code}/eventCard/attendees-false"  # Replace with your actual API URL
ATTENDEES_TRUE_URL = f"http://localhost:27017/user/conference/{conference_code}/eventCard/attendees-true"  # Replace with your actual API URL

def fetch_attendees(url, conference_code):
    """Fetch attendees list and count from the given API URL."""
    try:
        response = requests.get(f"{url}")
        if response.status_code == 200:
            data = response.json()
            return data.get('count', 0), data.get('attendees', [])
        elif response.status_code == 404:
            st.error("Conference not found!")
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
    return 0, []

def main_show_attendance():
    """Main function to render the Streamlit app."""
    st.title("Attendees Management")

    # Input field for conference code
    # conference_code = st.text_input("Enter Conference Code:", placeholder="e.g., TC2024")
    
    conference_code = st.session_state.get('current_user', 'Guest')
    print(f"Hello showattendance, {conference_code}!")

    if conference_code:
        # Fetch attendeesFalse and attendeesTrue from respective endpoints
        # st.write("Fetching attendees data...")
        false_count, attendees_false = fetch_attendees(ATTENDEES_FALSE_URL, conference_code)
        true_count, attendees_true = fetch_attendees(ATTENDEES_TRUE_URL, conference_code)

        # Display attendees side by side
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Not Attended (False)")
            st.write(f"Total: {false_count}")
            for attendee in attendees_false:
                st.write(
                    f"- **{attendee['name']}**\n"
                    f"  - Username: {attendee['username']}\n"
                    f"  - Email: {attendee['email']}"
                )

        with col2:
            st.subheader("Attended (True)")
            st.write(f"Total: {true_count}")
            for attendee in attendees_true:
                st.write(
                    f"- **{attendee['name']}**\n"
                    f"  - Username: {attendee['username']}\n"
                    f"  - Email: {attendee['email']}"
                )

# Run the main function
if __name__ == "__main__":
    main_show_attendance()
