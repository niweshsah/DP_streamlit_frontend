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
    url = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/addNewMentor"
    
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
    url = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/mentors"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        return None

def delete_image(name, conference_code="qwerty"):
    """Delete an image from the API by name"""
    url = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/deleteMentor"
    
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
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
            padding: 0.5rem;
        }
        .mentor-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 0.8rem 0;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .mentor-card:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .mentor-name {
            color: #1f1f1f;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .profession-display {
            font-size: 1.1rem;
            color: #2c5282;
            background-color: #ebf8ff;
            padding: 0.5rem;
            border-radius: 0.3rem;
            display: inline-block;
        }
        .delete-button button {
            background-color: #fc8181;
        }
        .delete-button button:hover {
            background-color: #f56565;
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

    st.title("👨‍🏫 Mentor Management System")
    
    if conference_code:
        tab1, tab2 = st.tabs(["📤 Upload New Mentor", "👀 View Existing Mentors"])
        
        with tab1:
            st.header("Upload New Mentor")
            
            with st.form("mentor_upload_form"):
                name = st.text_input("Mentor Name")
                profession = st.text_input("Profession")
                photo_file = st.file_uploader("Upload Photo", type=['jpg', 'jpeg', 'png'])
                
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
                            photo_base64 = convert_image_to_base64(photo_file)
                            success, message = upload_mentor(name, profession, photo_base64, conference_code)
                            
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
        
        with tab2:
            st.header("Existing Mentors")
            
            if st.button("🔄 Refresh List"):
                st.rerun()
            
            mentors = view_existing_mentors(conference_code)
            
            if mentors is None:
                st.error("Failed to fetch mentors. Please try again later.")
            elif not mentors:
                st.info("No mentors found.")
            else:
                cols = st.columns(3)
                for idx, mentor in enumerate(mentors):
                    with cols[idx % 3]:
                        with st.container():
                            st.markdown(f'<div class="mentor-card">', unsafe_allow_html=True)
                            
                            # Display mentor photo
                            if 'photo' in mentor and mentor['photo']:
                                try:
                                    img_data = mentor['photo'].split(',')[1] if ',' in mentor['photo'] else mentor['photo']
                                    st.image(base64.b64decode(img_data), width=200)
                                except Exception:
                                    st.image("https://via.placeholder.com/200", width=200)
                            
                            # Display mentor details
                            st.subheader(mentor.get('name', 'Unknown'))
                            st.write(f"Profession: {mentor.get('profession', 'Not specified')}")
                            
                            # Display last modified date
                            if 'lastModified' in mentor:
                                try:
                                    modified_date = datetime.fromisoformat(mentor['lastModified'])
                                    st.caption(f"Last updated: {modified_date.strftime('%Y-%m-%d %H:%M')}")
                                except ValueError:
                                    pass
                            
                            # Delete button
                            if st.button(f"🗑️ Delete {mentor.get('name')}", key=f"delete_{idx}"):
                                with st.spinner("Deleting mentor..."):
                                    success, message = delete_image(mentor.get('name'), conference_code)
                                    
                                    if success:
                                        st.success(message)
                                        st.rerun()
                                    else:
                                        st.error(message)
                            
                            st.markdown(f'</div>', unsafe_allow_html=True)
    
    else:
        st.info("👋 Please enter a conference code to manage mentors.")

    # Footer with styling
    st.markdown("""
        <div class="footer">
            🌟 Mentor Management System
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main_mentors()
