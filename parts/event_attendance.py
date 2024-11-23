# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# def fetch_attendees(url, conference_code = 'DP2024'):
#     """Fetch attendees list and count from the given API URL."""
#     try:
#         response = requests.get(f"{url}")
#         if response.status_code == 200:
#             data = response.json()
#             return data.get('count', 0), data.get('attendees', [])
#         elif response.status_code == 404:
#             st.error("❌ Conference not found!")
#         else:
#             st.error(f"❌ Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
#     except requests.exceptions.RequestException as e:
#         st.error(f"❌ Failed to fetch data: {e}")
#     return 0, []

# def main():
#     st.title("Conference Events Attendance Dashboard")
    
#     conference_code = st.session_state.get('current_user', 'DP2024')
#     # st.write(f"Hello from about tab, {conference_code}!")
    
    
#     # Configuration for the API endpoint
#     API_BASE_URL = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/" # Replace with your actual API URL
    
#     ATTENDANCE_ACCEPTED_URL = f"{API_BASE_URL}/getAcceptedAttendees"
    
#     # Fetch attendees data
#     total_attendees, attendees = fetch_attendees(ATTENDANCE_ACCEPTED_URL)
    
    
    
    
    
#     try:
#         # Fetch events data
#         response = requests.get(f"{API_BASE_URL}/get-conference-events")
        
#         if response.status_code == 200:
#             events_data = response.json()
            
#             if not events_data:
#                 st.warning("No events found")
#                 return
                
#             # Create DataFrame
#             df = pd.DataFrame(events_data)
            
#             # Calculate maximum possible attendees (you might want to adjust this)
#             MAX_ATTENDEES = 100  # Example maximum capacity
#             df['attendance_percentage'] = (df['totalAttendees'] / MAX_ATTENDEES * 100).round(2)
            
#             # Summary Statistics
#             st.header("Events Overview")
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Total Events", len(df))
#             with col2:
#                 st.metric("Average Attendance", f"{df['totalAttendees'].mean():.1f}")
#             with col3:
#                 st.metric("Total Attendees", df['totalAttendees'].sum())
            
#             # Bar Chart
#             st.header("Attendance by Event")
#             fig = px.bar(df, 
#                         x='title', 
#                         y='attendance_percentage',
#                         title='Event Attendance Percentages',
#                         labels={'title': 'Event Title', 
#                                'attendance_percentage': 'Attendance %'},
#                         text='attendance_percentage')
            
#             fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
#             fig.update_layout(yaxis_range=[0, 100])  # Set y-axis from 0 to 100%
#             st.plotly_chart(fig, use_container_width=True)
            
#             # Detailed Table
#             st.header("Detailed Event Information")
#             # Create a formatted table
#             table_data = df[['title', 'time', 'venue', 'totalAttendees', 'attendance_percentage']]
#             table_data = table_data.rename(columns={
#                 'title': 'Event Title',
#                 'time': 'Time',
#                 'venue': 'Venue',
#                 'totalAttendees': 'Total Attendees',
#                 'attendance_percentage': 'Attendance %'
#             })
            
#             # Format the attendance percentage
#             table_data['Attendance %'] = table_data['Attendance %'].apply(lambda x: f"{x:.1f}%")
            
#             # Display as a static table
#             st.dataframe(
#                 table_data,
#                 column_config={
#                     "Event Title": st.column_config.TextColumn(width="large"),
#                     "Venue": st.column_config.TextColumn(width="medium"),
#                 },
#                 hide_index=True,
#             )
            
#             # Attendance Gauge Chart
#             st.header("Overall Attendance Status")
#             total_attendance_percentage = (df['totalAttendees'].sum() / (MAX_ATTENDEES * len(df)) * 100)
            
#             gauge = go.Figure(go.Indicator(
#                 mode = "gauge+number",
#                 value = total_attendance_percentage,
#                 domain = {'x': [0, 1], 'y': [0, 1]},
#                 title = {'text': "Overall Attendance Percentage"},
#                 gauge = {
#                     'axis': {'range': [0, 100]},
#                     'bar': {'color': "darkblue"},
#                     'steps': [
#                         {'range': [0, 30], 'color': "red"},
#                         {'range': [30, 70], 'color': "yellow"},
#                         {'range': [70, 100], 'color': "green"}
#                     ],
#                     'threshold': {
#                         'line': {'color': "red", 'width': 4},
#                         'thickness': 0.75,
#                         'value': 80
#                     }
#                 }
#             ))
            
#             st.plotly_chart(gauge, use_container_width=True)
            
#             # Download Data Option
#             csv = df.to_csv(index=False)
#             st.download_button(
#                 label="Download Event Data as CSV",
#                 data=csv,
#                 file_name="event_attendance.csv",
#                 mime="text/csv",
#             )
            
#         else:
#             st.error("Failed to fetch events data")
            
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     st.set_page_config(
#         page_title="Event Attendance Dashboard",
#         page_icon="📊",
#         layout="wide"
#     )
#     main()








































# import streamlit as st
# import requests
# import pandas as pd
# from datetime import datetime

# def fetch_data(url, endpoint):
#     """Generic function to fetch data from API"""
#     try:
#         response = requests.get(f"{url}/{endpoint}")
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Failed to fetch data: {str(e)}")
#         return None

# @st.cache_data(ttl=300)  # Cache for 5 minutes
# def load_conference_data(conference_code):
#     """Load all conference data with caching"""
#     base_url = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard"
    
#     # Fetch attendees
#     attendees_data = fetch_data(base_url, "getAcceptedAttendees")
#     total_attendees = attendees_data.get('count', 0) if attendees_data else 0
    
#     # Fetch events
#     events_data = fetch_data(base_url, "get-conference-events")
    
#     return total_attendees, events_data

# def format_percentage(value):
#     """Format a number as percentage string"""
#     return f"{value:.1f}%"

# def main_event_attendance():
#     st.title("Conference Events Dashboard")
    
#     # Get conference code from session state
#     conference_code = st.session_state.get('current_user', 'DP2024')
    
#     # Add settings in sidebar
#     with st.sidebar:
#         st.title("Dashboard Settings")
#         max_capacity = st.number_input(
#             "Maximum Attendees per Event",
#             min_value=10,
#             max_value=1000,
#             value=100
#         )
    
#     # Load data
#     with st.spinner("Loading dashboard data..."):
#         total_attendees, events_data = load_conference_data(conference_code)
        
#         if not events_data:
#             st.warning("No events found for this conference")
#             return
            
#         # Create DataFrame
#         df = pd.DataFrame(events_data)
#         df['attendance_percentage'] = (df['totalAttendees'] / max_capacity * 100).round(2)
        
#         # Summary metrics
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric("Total Events", len(df))
#         with col2:
#             st.metric("Average Attendance", f"{df['totalAttendees'].mean():.1f}")
#         with col3:
#             st.metric("Total Attendees", df['totalAttendees'].sum())
#         with col4:
#             st.metric("Highest Attendance", df['totalAttendees'].max())
        
#         # Events bar chart using st.bar_chart
#         st.header("Event Attendance")
#         st.bar_chart(
#             data=df.set_index('title')['attendance_percentage'],
#             use_container_width=True
#         )
        
#         # Detailed table
#         st.header("Event Details")
        
#         # Format datetime
#         df['formatted_time'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M')
        
#         # Display table
#         st.dataframe(
#             df[['title', 'formatted_time', 'venue', 'totalAttendees', 'attendance_percentage']].rename(columns={
#                 'title': 'Event Title',
#                 'formatted_time': 'Time',
#                 'venue': 'Venue',
#                 'totalAttendees': 'Total Attendees',
#                 'attendance_percentage': 'Attendance %'
#             }).assign(**{
#                 'Attendance %': lambda x: x['attendance_percentage'].apply(format_percentage)
#             }).drop(columns=['attendance_percentage']),
#             hide_index=True,
#             use_container_width=True
#         )
        
#         # Overall attendance status
#         st.header("Overall Attendance Status")
#         overall_percentage = (df['totalAttendees'].sum() / (max_capacity * len(df)) * 100)
#         st.progress(min(overall_percentage / 100, 1.0))
#         st.write(f"Overall attendance: {format_percentage(overall_percentage)}")
        
#         # Download option
#         st.download_button(
#             label="Download Event Data (CSV)",
#             data=df.to_csv(index=False),
#             file_name=f"event_attendance_{datetime.now().strftime('%Y%m%d')}.csv",
#             mime="text/csv"
#         )

# if __name__ == "__main__":
#     st.set_page_config(
#         page_title="Event Attendance Dashboard",
#         page_icon="📊",
#         layout="wide"
#     )
#     main_event_attendance()




































import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def fetch_data(url, endpoint):
    """Generic function to fetch data from API"""
    try:
        response = requests.get(f"{url}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data: {str(e)}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_conference_data(conference_code):
    """Load all conference data with caching"""
    base_url = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard"
    
    # Fetch attendees
    attendees_data = fetch_data(base_url, "getAcceptedAttendees")
    total_attendees = attendees_data.get('count', 0) if attendees_data else 0
    
    # Fetch events
    events_data = fetch_data(base_url, "get-conference-events")
    
    return total_attendees, events_data

def main_event_attendance():
    st.title("Conference Events Dashboard")
    
    # Get conference code from session state
    conference_code = st.session_state.get('current_user', 'DP2024')
    
    # Add settings in sidebar
    # with st.sidebar:
    #     st.title("Dashboard Settings")
    #     max_capacity = st.number_input(
    #         "Maximum Attendees per Event",
    #         min_value=10,
    #         max_value=1000,
    #         value=100
    #     )
    
    # Load data
    with st.spinner("Loading dashboard data..."):
        total_attendees, events_data = load_conference_data(conference_code)
        
        if not events_data:
            st.warning("No events found for this conference")
            return
            
        # Create DataFrame
        df = pd.DataFrame(events_data)
        
        # Calculate attendance percentage
        df['attendance_percentage'] = (df['totalAttendees'] / total_attendees * 100).round(1)
        
        # Format time
        df['formatted_time'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Add percentage symbol
        df['attendance_display'] = df['attendance_percentage'].astype(str) + '%'
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Events", len(df))
        with col2:
            st.metric("Average Attendance", f"{df['totalAttendees'].mean():.1f}")
        with col3:
            st.metric("Total Attendees", df['totalAttendees'].sum())
        with col4:
            st.metric("Highest Attendance", df['totalAttendees'].max())
        
        # Events bar chart
        st.header("Event Attendance")
        st.bar_chart(
            data=df.set_index('title')['attendance_percentage'],
            use_container_width=True
        )
        
        # Detailed table
        st.header("Event Details")
        
        # Create display DataFrame
        display_df = pd.DataFrame({
            'Event Title': df['title'],
            'Time': df['formatted_time'],
            'Venue': df['venue'],
            'Total Attendees': df['totalAttendees'],
            'Attendance %': df['attendance_display']
        })
        
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True
        )
        
        # Overall attendance status
        st.header("Overall Attendance Status")
        overall_percentage = (df['totalAttendees'].sum() / (total_attendees * len(df)) * 100)
        st.progress(min(overall_percentage / 100, 1.0))
        st.write(f"Overall attendance: {overall_percentage:.1f}%")
        
        # Download option
        st.download_button(
            label="Download Event Data (CSV)",
            data=df.to_csv(index=False),
            file_name=f"event_attendance_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    st.set_page_config(
        page_title="Event Attendance Dashboard",
        page_icon="📊",
        layout="wide"
    )
    main_event_attendance()