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
        img = Image.open(image_file)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        max_size = (800, 800)
        img.thumbnail(max_size, Image.LANCZOS)
        
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    return None

def upload_image(name, photo_base64, conference_code="qwerty"):
    """Upload image data to the API"""
    url = f"http://localhost:27017/user/conference/{conference_code}/eventCard/addNewSponsors"
    
    payload = {
        "name": name,
        "photo": photo_base64,
        "lastModified": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True, "Image uploaded successfully!"
    except requests.exceptions.RequestException as e:
        return False, f"Error uploading image: {str(e)}"

def view_existing_images(conference_code="qwerty"):
    """Fetch existing images from the API"""
    
    url = f"http://localhost:27017/user/conference/{conference_code}/eventCard/sponsors"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        return None

def delete_image(name, conference_code="qwerty"):
    """Delete an image from the API by name"""
    url = f"http://localhost:27017/user/conference/{conference_code}/eventCard/deleteSponsor"
    
    payload = {"name": name}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True, "Sponsor deleted successfully!"
    except requests.exceptions.RequestException as e:
        return False, f"Error deleting image: {str(e)}"

def main_sponsor():
    # st.set_page_config(page_title="Image Management System", layout="wide")
    
    conference_code = st.session_state.get('current_user', 'Guest')
    print(f"Hello, {conference_code}!")

    st.markdown("""
        <style>
        .main_sponsor { padding: 2rem; }
        .stButton button { width: 100%; }
        .image-card { 
            padding: 1rem; 
            border: 1px solid #ddd; 
            border-radius: 10px; 
            margin-bottom: 1rem; 
            background-color: #f9f9f9; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .image-card:hover { 
            background-color: #f1f1f1; 
        }
        .stTextInput, .stTextArea {
            padding: 10px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ddd;
            margin-top: 10px;
        }
        .stButton {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        .stButton:hover {
            background-color: #45a049;
        }
        .stSuccess {
            color: #4CAF50;
            font-size: 16px;
            margin-top: 10px;
        }
        .stError {
            color: #f44336;
            font-size: 16px;
            margin-top: 10px;
        }
        .stInfo {
            color: #2196F3;
            font-size: 16px;
            margin-top: 10px;
        }
        .tab-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Sponsor Management System")

    tab1, tab2 = st.tabs(["Upload New Image", "View Existing Images"])
    
    with tab1:
        st.markdown("<div class='tab-title'>Upload New Image</div>", unsafe_allow_html=True)
        
        with st.form("image_upload_form"):
            name = st.text_input("Sponsor Name")
            photo_file = st.file_uploader("Upload Sponsor Logo", type=['jpg', 'jpeg', 'png'])
            
            if photo_file:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(photo_file, caption="Preview", use_column_width=True)
            
            submit_button = st.form_submit_button("Upload Image")
            
            if submit_button:
                if not name or not photo_file:
                    st.error("Please provide a sponsor name and upload a photo.")
                else:
                    with st.spinner("Uploading image..."):
                        photo_base64 = convert_image_to_base64(photo_file)
                        success, message = upload_image(name, photo_base64, conference_code=conference_code)
                        
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
    
    with tab2:
        st.markdown("<div class='tab-title'>Existing Images</div>", unsafe_allow_html=True)
        
        if st.button("Refresh List"):
            st.rerun()
        
        images = view_existing_images(conference_code=conference_code)
        
        if images is None:
            st.error("Failed to fetch images. Please try again later.")
        elif not images:
            st.info("No sponsors found.")
        else:
            cols = st.columns(3)
            for idx, image in enumerate(images):
                with cols[idx % 3]:
                    with st.container():
                        st.markdown("<div class='image-card'>", unsafe_allow_html=True)
                        
                        if 'photo' in image and image['photo']:
                            try:
                                if ',' in image['photo']:
                                    img_data = image['photo'].split(',')[1]
                                else:
                                    img_data = image['photo']
                                st.image(base64.b64decode(img_data), width=200)
                            except Exception:
                                st.image("https://via.placeholder.com/200", width=200)
                        
                        st.subheader(image.get('name', 'Unknown'))
                        
                        if 'lastModified' in image:
                            try:
                                modified_date = datetime.fromisoformat(image['lastModified'])
                                st.caption(f"Last updated: {modified_date.strftime('%Y-%m-%d %H:%M')}")
                            except ValueError:
                                pass
                            
                            # Delete button
                        if st.button("Delete", key=f"delete_{idx}"):
                            with st.spinner("Deleting image..."):
                                success, message = delete_image(image.get('name'), conference_code=conference_code)
                                
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                        
                        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main_sponsor()
