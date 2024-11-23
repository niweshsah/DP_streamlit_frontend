

import streamlit as st
import requests
import os

rest_api_url = os.getenv("REST_API_URL")

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

def main_attendance_accepted():
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
        ATTENDEES_TOTAL_URL = f"{rest_api_url}/user/conference/{conference_code}/eventCard/total-attendees"
        
        ATTENDEES_FALSE_URL = f"{rest_api_url}/user/conference/{conference_code}/eventCard/attendees-false"
        
        ATTENDEES_TRUE_URL = f"{rest_api_url}/user/conference/{conference_code}/eventCard/attendees-true"
        
        ATTENDEES_ACCEPTED_URL = f"{rest_api_url}/user/conference/{conference_code}/eventCard/getAcceptedAttendees"
        
        ATTENDEES_NOT_ACCEPTED_URL = f"{rest_api_url}/user/conference/{conference_code}/eventCard/attendees-not-accepted"
        

        # Fetch data
        attendee_total_count, attendee_total = fetch_attendees(ATTENDEES_TOTAL_URL, conference_code)
        
        # attendee_not_accepted_count, attendee_not_accepted = fetch_attendees(ATTENDEES_FALSE_URL, conference_code)
        
        # attendee_accepted_count, attendee_accepted = fetch_attendees(ATTENDEES_TRUE_URL, conference_code)
        
        attendee_accepted_count, attendee_accepted = fetch_attendees(ATTENDEES_ACCEPTED_URL, conference_code)
        
        attendee_not_accepted_count, attendee_not_accepted = fetch_attendees(ATTENDEES_NOT_ACCEPTED_URL, conference_code)

        # Calculate statistics
        # total_attendees = attendee_total_count
        # total_responded = attendee_accepted_count + attendee_not_accepted_count
        
        # print(total_responded)

        # Calculate rates
        if attendee_total_count > 0:
            acceptance_rate = (attendee_accepted_count / attendee_total_count) * 100
            attendance_rate = (attendee_accepted_count / attendee_total_count) * 100
        else:
            acceptance_rate = 0
            attendance_rate = 0

        # Display statistics
        st.markdown("""
            <div class="attendance-stats">
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Total Invited</div>
                    </div>
                    <div>
                        <div class="stat-number">{}</div>
                        <div class="stat-label">Accepted Invites</div>
                    </div>
                    <div>
                        <div class="stat-number">{:.1f}%</div>
                        <div class="stat-label">Acceptance Rate</div>
                    </div>
        
            </div>
        """.format(attendee_total_count, attendee_accepted_count, acceptance_rate), unsafe_allow_html=True)

        # Display attendees in columns
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
                <div class="section-attendee invited">
                    <h3>📝 Not Responded ({attendee_not_accepted_count})</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # for attendee in attendee_total:
            #     if attendee not in attendee_accepted and attendee not in attendee_not_accepted:
            #         st.markdown(create_attendee_card(attendee), unsafe_allow_html=True)
            
            for attendee in attendee_not_accepted:
                st.markdown(create_attendee_card(attendee), unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="section-attendee accepted">
                    <h3>✅ Accepted ({attendee_accepted_count})</h3>
                </div>
            """, unsafe_allow_html=True)
            
            for attendee in attendee_accepted:
                st.markdown(create_attendee_card(attendee), unsafe_allow_html=True)


    else:
        st.info("👋 Please enter a conference code to view attendance.")

if __name__ == "__main__":
    main_attendance_accepted()