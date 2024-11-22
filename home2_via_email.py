

import streamlit as st # type: ignore
from parts.sponsors import main_sponsor  # Assuming this module exists
from parts.attendees import main_add_attendee  # Assuming this module exists
from parts.showAttendance import main_show_attendance  # Assuming this module exists
from parts.events import main_event  # Assuming this module exists
from parts.mentors import main_mentors  # Assuming this module exists
from parts.food import main_food  # Assuming this module exists
from parts.sliding_images import main_sliding_images  # Assuming this module exists
from parts.about import main_about  # Assuming this module exists
from parts.helpline import main_helpline  # Assuming this module exists
from parts.attendeeAccepted import main_attendance_accepted  # Assuming this module exists
from parts.add_attendee_csv import main_attendee_csv  # Assuming this module exists

def main_home2():
    # Page config must be the first Streamlit command
    # st.set_page_config(
    #     page_title="Dynamic Single Page App",
    #     layout="wide",
    #     initial_sidebar_state="collapsed"
    # )

    # Hide the default menu and footer
    hide_menu = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    
    st.markdown(hide_menu, unsafe_allow_html=True)

    # Sidebar Logout Button
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
        # st.button("Logout", key="logout", help="Click to logout")

    # Initialize session state for page tracking if not exists
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

    st.title("Gatherhub")

    # Create a clean button layout
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        if st.button("Add attendees", key="add_attendees", use_container_width=True):
            st.session_state.current_page = 'add_attendees'
            
        if st.button("Sponsors", key="Sponsors", use_container_width=True):
            st.session_state.current_page = 'Sponsors'
            
        if st.button("Mentors", key="Mentors", use_container_width=True):
            st.session_state.current_page = 'Mentors'

    with col2:
        if st.button("View attendance", key="view_attendance", use_container_width=True):
            st.session_state.current_page = 'view_attendance'
            
        if st.button("SlidingImage", key="SlidingImage", use_container_width=True):
            st.session_state.current_page = 'SlidingImage'
            
        if st.button("Helplines", key="Helpline", use_container_width=True):
            st.session_state.current_page = 'Helpline'

    with col3:
        if st.button("About", key="about", use_container_width=True):
            st.session_state.current_page = 'about'
            
        if st.button("Event Schedule", key="event_schedule", use_container_width=True):
            st.session_state.current_page = 'event_schedule'
            
        if st.button("Food", key="food", use_container_width=True):
            st.session_state.current_page = 'food'
        if st.button("Attendance Accepted", key="attendance_accepted", use_container_width=True):
            st.session_state.current_page = 'attendance_accepted'

    # Add a divider
    st.divider()

    # Content section
    if st.session_state.current_page == 'home':
        st.header("Home")
        st.write("Welcome to our application! Click any button above to explore different sections.")
        
    elif st.session_state.current_page == 'add_attendees':
        main_attendee_csv()
        
    elif st.session_state.current_page == 'Sponsors':
        main_sponsor()

    elif st.session_state.current_page == 'Mentors':
        main_mentors()

    elif st.session_state.current_page == 'view_attendance':
        main_show_attendance()

    elif st.session_state.current_page == 'SlidingImage':
        main_sliding_images()

    elif st.session_state.current_page == 'event_schedule':
        main_event()
        
    elif st.session_state.current_page == 'about':
        main_about()
        
    elif st.session_state.current_page == 'Helpline':
        main_helpline()
        
    elif st.session_state.current_page == 'food':
        main_food()
    elif st.session_state.current_page == 'attendance_accepted':
        main_attendance_accepted()

    # Add some spacing at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)


# Run the main function
if __name__ == "__main__":
    main_home2()
