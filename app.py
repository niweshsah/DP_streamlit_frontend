import streamlit as st
from parts.sidebar import render_sidebar
# from parts.sidebar import sidebar_radio
# from parts.Image import Image
# from parts.sponsors import sponsors

# Load custom CSS file to style the app
#page config 
st.set_page_config(page_title="GatherHub Admin",page_icon="🛰️",initial_sidebar_state="expanded")
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file for custom styling
local_css("styles.css")

# Main function to handle page rendering
def main():
    # page = st.sidebar.radio("Navigation", ["Introduction", "Irrigation Monitoring", "NDVI Map", "Soil Moisture"])
    
    render_sidebar()
    # Render the appropriate page based on selection
    # if page == "Introduction":
    #     intro()
    # elif page == "Irrigation Monitoring":
    #     maps_visualization()
    #     irrigation_monitoring()
    # elif page == "NDVI Map":
    #     webpage()
    # elif page == "Soil Moisture":
    #     on_page()



# Run the app
if __name__ == "__main__":
    main()
