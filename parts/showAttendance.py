# import streamlit as st
# import requests

# conference_code = st.session_state.get('current_user', 'Guest')
# print(f"Hello, {conference_code}!")


# # Backend API URLs
# ATTENDEES_FALSE_URL = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/attendees-false"  # Replace with your actual API URL
# ATTENDEES_TRUE_URL = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/attendees-true"  # Replace with your actual API URL

# def fetch_attendees(url, conference_code):
#     """Fetch attendees list and count from the given API URL."""
#     try:
#         response = requests.get(f"{url}")
#         if response.status_code == 200:
#             data = response.json()
#             return data.get('count', 0), data.get('attendees', [])
#         elif response.status_code == 404:
#             st.error("Conference not found!")
#         else:
#             st.error(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
#     except requests.exceptions.RequestException as e:
#         st.error(f"Failed to fetch data: {e}")
#     return 0, []

# def main_show_attendance():
#     """Main function to render the Streamlit app."""
#     st.title("Attendees Management")

#     # Input field for conference code
#     # conference_code = st.text_input("Enter Conference Code:", placeholder="e.g., TC2024")
    
#     conference_code = st.session_state.get('current_user', 'Guest')
#     print(f"Hello showattendance, {conference_code}!")

#     if conference_code:
#         # Fetch attendeesFalse and attendeesTrue from respective endpoints
#         # st.write("Fetching attendees data...")
#         false_count, attendees_false = fetch_attendees(ATTENDEES_FALSE_URL, conference_code)
        
#         true_count, attendees_true = fetch_attendees(ATTENDEES_TRUE_URL, conference_code)

#         # Display attendees side by side
#         col1, col2 = st.columns(2)

#         with col1:
#             st.subheader("Not Attended (False)")
#             st.write(f"Total: {false_count}")
#             for attendee in attendees_false:
#                 st.write(
#                     f"- **{attendee['name']}**\n"
#                     f"  - Username: {attendee['username']}\n"
#                     f"  - Email: {attendee['email']}"
#                 )

#         with col2:
#             st.subheader("Attended (True)")
#             st.write(f"Total: {true_count}")
#             for attendee in attendees_true:
#                 st.write(
#                     f"- **{attendee['name']}**\n"
#                     f"  - Username: {attendee['username']}\n"
#                     f"  - Email: {attendee['email']}"
#                 )

# # Run the main function
# if __name__ == "__main__":
#     main_show_attendance()














































import streamlit as st
import requests

def fetch_attendees(url, conference_code):
    """Fetch attendees list and count from the given API URL."""
    try:
        response = requests.get(f"{url}")
        if response.status_code == 200:
            data = response.json()
            return data.get('count', 0), data.get('attendees', [])
        elif response.status_code == 404:
            st.error("❌ Conference not found!")
        else:
            st.error(f"❌ Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to fetch data: {e}")
    return 0, []

def create_attendee_card(attendee):
    """Create HTML for an attendee card"""
    return f"""
        <div class="attendee-card">
            <div class="attendee-name">{attendee['name']}</div>
            <div class="attendee-details">
                <div class="detail-item">
                    <span class="detail-label">👤 Username:</span>
                    <span class="detail-value">{attendee['username']}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">📧 Email:</span>
                    <span class="detail-value">{attendee['email']}</span>
                </div>
            </div>
        </div>
    """

def main_show_attendance():
    """Main function to render the Streamlit app."""
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .attendance-stats {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #2c5282;
            margin-bottom: 0.5rem;
        }
        .stat-label {
            color: #4a5568;
            font-size: 0.9rem;
        }
        .attendee-card {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.8rem;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .attendee-card:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .attendee-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 0.5rem;
        }
        .attendee-details {
            font-size: 0.9rem;
            color: #4a5568;
        }
        .detail-item {
            margin-bottom: 0.3rem;
        }
        .detail-label {
            color: #718096;
            margin-right: 0.5rem;
        }
        .detail-value {
            color: #2d3748;
        }
        .section-not-attended {
            border-top: 3px solid #fc8181;
            padding-top: 1rem;
        }
        .section-attended {
            border-top: 3px solid #68d391;
            padding-top: 1rem;
        }
        .refresh-button {
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("👥 Attendees Management")
    
    conference_code = st.session_state.get('current_user', 'Guest')
    
    if conference_code:
        # Add refresh button
        col1, col2, col3 = st.columns([3, 1, 3])
        with col2:
            if st.button("🔄 Refresh Data", key="refresh"):
                st.cache_data.clear()

        # Backend API URLs
        ATTENDEES_FALSE_URL = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/attendees-false"
        ATTENDEES_TRUE_URL = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/attendees-true"

        # Fetch data
        false_count, attendees_false = fetch_attendees(ATTENDEES_FALSE_URL, conference_code)
        true_count, attendees_true = fetch_attendees(ATTENDEES_TRUE_URL, conference_code)

        # Display total statistics
        total_attendees = true_count + false_count
        if total_attendees > 0:
            attendance_rate = (true_count / total_attendees) * 100
        else:
            attendance_rate = 0

        st.markdown("""
            <div class="attendance-stats">
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Total Registered</div>
                    </div>
                    <div>
                        <div class="stat-number">{:.1f}%</div>
                        <div class="stat-label">Attendance Rate</div>
                    </div>
                </div>
            </div>
        """.format(total_attendees, attendance_rate), unsafe_allow_html=True)

        # Display attendees in columns
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
                <div class="section-not-attended">
                    <h3>📝 Not Attended ({false_count})</h3>
                </div>
            """, unsafe_allow_html=True)
            
            for attendee in attendees_false:
                st.markdown(create_attendee_card(attendee), unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="section-attended">
                    <h3>✅ Attended ({true_count})</h3>
                </div>
            """, unsafe_allow_html=True)
            
            for attendee in attendees_true:
                st.markdown(create_attendee_card(attendee), unsafe_allow_html=True)

    else:
        st.info("👋 Please enter a conference code to view attendance.")

if __name__ == "__main__":
    main_show_attendance()