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










































import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Constants
MAX_ATTENDEES = 100  # Default maximum capacity
CACHE_TTL = 300  # Cache timeout in seconds

class ConferenceAPI:
    def __init__(self, base_url, conference_code):
        self.base_url = base_url
        self.conference_code = conference_code
        
    def _make_request(self, endpoint):
        """Make API request with error handling"""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return None
            
    @st.cache_data(ttl=CACHE_TTL)
    def fetch_attendees(self):
        """Fetch attendees with caching"""
        data = self._make_request(f"getAcceptedAttendees")
        if data:
            return data.get('count', 0), data.get('attendees', [])
        return 0, []
        
    @st.cache_data(ttl=CACHE_TTL)
    def fetch_events(self):
        """Fetch events with caching"""
        return self._make_request("get-conference-events")

class DashboardUI:
    def __init__(self):
        self.setup_page_config()
        self.setup_sidebar()
        
    def setup_page_config(self):
        st.set_page_config(
            page_title="Conference Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
    def setup_sidebar(self):
        with st.sidebar:
            st.title("📈 Dashboard Settings")
            st.session_state.max_attendees = st.number_input(
                "Maximum Attendees per Event",
                min_value=10,
                max_value=1000,
                value=MAX_ATTENDEES
            )
            st.info("💡 Data refreshes every 5 minutes")
            
    def show_loading_spinner(self):
        """Show loading animation"""
        with st.spinner("Loading dashboard data..."):
            time.sleep(0.5)  # Brief pause for UX

    def render_metrics(self, df):
        """Render summary metrics"""
        st.header("📊 Events Overview")
        metrics_cols = st.columns(4)
        
        with metrics_cols[0]:
            st.metric("Total Events", len(df))
        with metrics_cols[1]:
            st.metric("Average Attendance", f"{df['totalAttendees'].mean():.1f}")
        with metrics_cols[2]:
            st.metric("Total Attendees", df['totalAttendees'].sum())
        with metrics_cols[3]:
            st.metric(
                "Highest Attendance",
                df['totalAttendees'].max(),
                delta=f"{df['totalAttendees'].max() - df['totalAttendees'].mean():.1f} vs avg"
            )

    def render_attendance_chart(self, df):
        """Render attendance bar chart"""
        st.header("📈 Attendance by Event")
        
        # Calculate attendance percentages
        df['attendance_percentage'] = (df['totalAttendees'] / st.session_state.max_attendees * 100).round(2)
        
        fig = px.bar(
            df,
            x='title',
            y='attendance_percentage',
            title='Event Attendance Percentages',
            labels={'title': 'Event Title', 'attendance_percentage': 'Attendance %'},
            text='attendance_percentage',
            color='attendance_percentage',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        fig.update_layout(
            yaxis_range=[0, 100],
            height=500,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def render_events_table(self, df):
        """Render detailed events table"""
        st.header("📋 Event Details")
        
        # Format datetime if it's a string
        df['formatted_time'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Prepare table data
        table_data = df[[
            'title', 'formatted_time', 'venue',
            'totalAttendees', 'attendance_percentage'
        ]].copy()
        
        table_data = table_data.rename(columns={
            'title': 'Event Title',
            'formatted_time': 'Time',
            'venue': 'Venue',
            'totalAttendees': 'Total Attendees',
            'attendance_percentage': 'Attendance %'
        })
        
        table_data['Attendance %'] = table_data['Attendance %'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(
            table_data,
            column_config={
                "Event Title": st.column_config.TextColumn(width="large"),
                "Time": st.column_config.TextColumn(width="medium"),
                "Venue": st.column_config.TextColumn(width="medium"),
            },
            hide_index=True,
            height=400
        )

    def render_gauge_chart(self, df):
        """Render overall attendance gauge"""
        st.header("🎯 Overall Attendance Status")
        
        total_attendance_percentage = (
            df['totalAttendees'].sum() / 
            (st.session_state.max_attendees * len(df)) * 
            100
        )
        
        gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=total_attendance_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Attendance Percentage"},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightcoral"},
                    {'range': [30, 70], 'color': "khaki"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        gauge.update_layout(height=400)
        st.plotly_chart(gauge, use_container_width=True)

    def render_download_button(self, df):
        """Render data download option"""
        st.download_button(
            label="📥 Download Event Data (CSV)",
            data=df.to_csv(index=False),
            file_name=f"event_attendance_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

def main():
    # Initialize dashboard UI
    dashboard = DashboardUI()
    
    # Set up API connection
    conference_code = st.session_state.get('current_user', 'DP2024')
    api_base = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard"
    api = ConferenceAPI(api_base, conference_code)
    
    # Show loading state
    dashboard.show_loading_spinner()
    
    # Fetch data
    total_attendees, attendees = api.fetch_attendees()
    events_data = api.fetch_events()
    
    if not events_data:
        st.warning("⚠️ No events found for this conference")
        return
        
    # Create DataFrame
    df = pd.DataFrame(events_data)
    
    # Render dashboard components
    dashboard.render_metrics(df)
    col1, col2 = st.columns(2)
    
    with col1:
        dashboard.render_attendance_chart(df)
    with col2:
        dashboard.render_gauge_chart(df)
        
    dashboard.render_events_table(df)
    dashboard.render_download_button(df)

if __name__ == "__main__":
    main()