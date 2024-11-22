import streamlit as st
import requests
from datetime import datetime

def fetch_conference_events(conference_code):
    """Fetch all events for a conference."""
    try:
        url = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/events"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('events', {})
        elif response.status_code == 404:
            st.error("❌ Conference not found!")
        else:
            st.error(f"❌ Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to fetch events: {e}")
    return {}

def format_event_time(time_str):
    """Format event time string."""
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.strftime("%I:%M %p")
    except:
        return time_str

def create_attendee_card(attendee):
    """Create HTML for an attendee card"""
    timestamp = attendee.get('timestamp', '')
    if timestamp:
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            timestamp = timestamp.strftime("%Y-%m-%d %I:%M %p")
        except:
            pass
    
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
                {f'''<div class="detail-item">
                    <span class="detail-label">⏰ Check-in:</span>
                    <span class="detail-value">{timestamp}</span>
                </div>''' if timestamp else ''}
            </div>
        </div>
    """

def main_event_attendance():
    """Main function to render the Streamlit app."""
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .event-card {
            background-color: #f7fafc;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            border: 1px solid #e2e8f0;
            cursor: pointer;
        }
        .event-card:hover {
            background-color: #edf2f7;
        }
        .event-card.selected {
            border: 2px solid #4299e1;
            background-color: #ebf8ff;
        }
        .event-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2d3748;
        }
        .event-details {
            font-size: 0.9rem;
            color: #4a5568;
            margin-top: 0.5rem;
        }
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
        </style>
    """, unsafe_allow_html=True)

    st.title("👥 Event Attendance Tracker")
    
    conference_code = st.session_state.get('current_user', 'Guest')

    if conference_code:
        # Add refresh button
        col1, col2, col3 = st.columns([3, 1, 3])
        with col2:
            if st.button("🔄 Refresh Data", key="refresh"):
                st.cache_data.clear()

        # Fetch conference events
        events = fetch_conference_events(conference_code)
        
        if events:
            # Create tabs for "Events Overview" and "Detailed View"
            tab1, tab2 = st.tabs(["📊 Events Overview", "🔍 Detailed View"])
            
            with tab1:
                # Display summary statistics for all events
                total_events = len(events)
                total_attended = sum(len(event.get('attendeesTrueForEvent', [])) for event in events.values())
                
                st.markdown(f"""
                    <div class="attendance-stats">
                        <div style="display: flex; justify-content: space-around; text-align: center;">
                            <div>
                                <div class="stat-number">{total_events}</div>
                                <div class="stat-label">Total Events</div>
                            </div>
                            <div>
                                <div class="stat-number">{total_attended}</div>
                                <div class="stat-label">Total Check-ins</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Display all events with their attendance statistics
                for event_id, event_data in events.items():
                    attendees = event_data.get('attendeesTrueForEvent', [])
                    attendance_count = len(attendees)
                    
                    st.markdown(f"""
                        <div class="event-card">
                            <div class="event-title">{event_data['title']}</div>
                            <div class="event-details">
                                🕒 {format_event_time(event_data['time'])} | 📍 {event_data['venue']}
                                <br>👥 Attendance: {attendance_count} checked in
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                # Event selection
                event_titles = [(event_id, event_data['title']) for event_id, event_data in events.items()]
                selected_event_id = st.selectbox(
                    "Select Event",
                    options=[eid for eid, _ in event_titles],
                    format_func=lambda x: next(title for eid, title in event_titles if eid == x)
                )
                
                if selected_event_id:
                    event_data = events[selected_event_id]
                    attendees = event_data.get('attendeesTrueForEvent', [])
                    
                    # Display event details
                    st.markdown(f"""
                        <div class="attendance-stats">
                            <h2>{event_data['title']}</h2>
                            <p>🕒 Time: {format_event_time(event_data['time'])}</p>
                            <p>📍 Venue: {event_data['venue']}</p>
                            <p>🎫 Event Code: {event_data['eventCode']}</p>
                            <p>👥 Total Checked-in: {len(attendees)}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display attendees
                    if attendees:
                        st.markdown("""
                            <div class="section-attended">
                                <h3>✅ Checked-in Attendees</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        for attendee in attendees:
                            st.markdown(create_attendee_card(attendee), unsafe_allow_html=True)
                    else:
                        st.info("No attendees have checked in yet.")

    else:
        st.info("👋 Please enter a conference code to view attendance.")

if __name__ == "__main__":
    main_event_attendance()