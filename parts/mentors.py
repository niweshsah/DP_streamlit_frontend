import streamlit as st
import requests
import base64
from PIL import Image
import io
from datetime import datetime
import json

def convert_image_to_base64(image_file):
    """Convert a PIL Image to base64 string"""
    if image_file is not None:
        # Open the image using PIL
        img = Image.open(image_file)
        
        # Convert image to RGB if it's not
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Resize image if it's too large (optional)
        max_size = (800, 800)
        img.thumbnail(max_size, Image.LANCZOS)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    return None

def upload_mentor(name, profession, photo_base64, conference_code="qwerty"):
    """Upload mentor data to the API"""
    url = f"http://localhost:27017/user/conference/{conference_code}/eventCard/addNewMentor"
    
    payload = {
        "name": name,
        "profession": profession,
        "photo": photo_base64,
        "lastModified": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True, "Mentor uploaded successfully!"
    except requests.exceptions.RequestException as e:
        return False, f"Error uploading mentor: {str(e)}"

def view_existing_mentors(conference_code="qwerty"):
    """Fetch existing mentors from the API"""
    url = f"http://localhost:27017/user/conference/{conference_code}/eventCard/mentors"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Extract mentors from the conferenceMentors key
        return data
    except requests.exceptions.RequestException:
        return None

def delete_image(name, conference_code="qwerty"):
    """Delete an image from the API by name"""
    url = f"http://localhost:27017/user/conference/{conference_code}/eventCard/deleteMentor"
    
    payload = {"name": name}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True, "Mentor deleted successfully!"
    except requests.exceptions.RequestException as e:
        return False, f"Error deleting image: {str(e)}"


def main_mentors():
    # st.set_page_config(page_title="Mentor Management System", layout="wide")
    
    conference_code = st.session_state.get('current_user', 'Guest')
    print(f"Hello, {conference_code}!")

    
    # Add some custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton button {
            width: 100%;
        }
        .mentor-card {
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Mentor Management System")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Upload New Mentor", "View Existing Mentors"])
    
    with tab1:
        st.header("Upload New Mentor")
        
        # Create a form for mentor details
        with st.form("mentor_upload_form"):
            name = st.text_input("Mentor Name")
            profession = st.text_input("Profession")
            photo_file = st.file_uploader("Upload Photo", type=['jpg', 'jpeg', 'png'])
            
            # Preview image if uploaded
            if photo_file:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(photo_file, caption="Preview", use_column_width=True)
            
            submit_button = st.form_submit_button("Upload Mentor")
            
            if submit_button:
                if not name or not profession or not photo_file:
                    st.error("Please fill all fields and upload a photo")
                else:
                    with st.spinner("Uploading mentor..."):
                        # Convert image to base64
                        photo_base64 = convert_image_to_base64(photo_file,conference_code)
                        
                        # Upload to API
                        success, message = upload_mentor(name, profession, photo_base64,conference_code)
                        
                        if success:
                            st.success(message)
                            # Clear form (hack: rerun the app)
                            st.rerun()
                        else:
                            st.error(message)
    
    with tab2:
        st.header("Existing Mentors")
        
        # Add refresh button
        if st.button("Refresh List"):
            st.rerun()
        
        # Fetch and display existing mentors
        mentors = view_existing_mentors()
        
        if mentors is None:
            st.error("Failed to fetch mentors. Please try again later.")
        elif not mentors:
            st.info("No mentors found.")
        else:
            # Display mentors in a grid
            cols = st.columns(3)
            for idx, mentor in enumerate(mentors):
                with cols[idx % 3]:
                    with st.container():
                        st.markdown("""
                            <div class="mentor-card">
                            """, unsafe_allow_html=True)
                        
                        # Display mentor photo
                        if 'photo' in mentor and mentor['photo']:
                            try:
                                # Handle both full data URI and raw base64
                                if ',' in mentor['photo']:
                                    img_data = mentor['photo'].split(',')[1]
                                else:
                                    img_data = mentor['photo']
                                st.image(base64.b64decode(img_data), width=200)
                            except Exception:
                                st.image("https://via.placeholder.com/200", width=200)
                        
                        # Display mentor details
                        st.subheader(mentor.get('name', 'Unknown'))
                        st.write(mentor.get('profession', 'Profession not specified'))
                        
                        # Display last modified date if available
                        if 'lastModified' in mentor:
                            try:
                                modified_date = datetime.fromisoformat(mentor['lastModified'])
                                st.caption(f"Last updated: {modified_date.strftime('%Y-%m-%d %H:%M')}")
                            except ValueError:
                                pass
                            
                            
                            # Delete button
                        if st.button("Delete", key=f"delete_{idx}"):
                            with st.spinner("Deleting image..."):
                                success, message = delete_image(mentor.get('name'),conference_code = conference_code)
                                
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                        
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            
            # Add export functionality
            # if st.button("Export Mentors Data"):
            #     # Prepare data for export
            #     export_data = json.dumps(mentors, indent=2)
                
            #     # Create download button
            #     st.download_button(
            #         label="Download JSON",
            #         data=export_data,
            #         file_name="mentors_data.json",
            #         mime="application/json"
            #     )

if __name__ == "__main__":
    main_mentors()