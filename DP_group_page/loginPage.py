


import streamlit as st
import requests
import base64
import pandas as pd
from PIL import Image
from io import BytesIO

# Backend Base URL (replace with your actual backend API URL)
BASE_URL = "http://gatherhub-r7yr.onrender.com/user/conference/DP2024"
# BASE_URL = "http://localhost:27017/user/conference/DP2024"
# Helper function to convert images to base64


def image_to_base64(image, max_width=500, max_height=500, quality=60):
    """60
    Convert an image to a Base64 string with optional resizing and compression.

    Args:
        image: File-like object (e.g., an uploaded image).
        max_width: Maximum width for resizing (default: 500 pixels).
        max_height: Maximum height for resizing (default: 500 pixels).
        quality: Compression quality (1-100) for JPEG/WebP (default: 85).

    Returns:
        str: Base64-encoded string of the processed image.
    """
    if image is not None:
        # Open the image using PIL
        img = Image.open(image)

        # Resize the image while maintaining aspect ratio
        img.thumbnail((max_width, max_height))

        # Convert the image to a compressed format (JPEG/WebP)
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)

        # Encode the image to Base64
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    return None

# Main App Function
def main_group():
    st.title("Group Management System")
    
    # Create a sidebar for navigation
    menu = ["Add New Group", "View Groups", "Edit Group"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Add New Group":
        add_group()
    elif choice == "View Groups":
        # view_groups()
        display_group_list()
        
    elif choice == "Edit Group":
        edit_group()

# Add New Group Functionality
def add_group():
    st.header("Add New Group")
    
    # Group Basic Information
    group_no = st.text_input("Group Number", key="add_group_no")
    project_name = st.text_input("Project Name", key="add_project_name")
    description = st.text_area("Project Description", key="add_description")
    
    # Faculty Members
    st.subheader("Faculty Members")
    num_faculty = st.number_input("Number of Faculty", min_value=1, max_value=5, value=1, key="add_num_faculty")
    faculty_members = []
    for i in range(num_faculty):
        faculty_name = st.text_input(f"Faculty Member {i+1} Name", key=f"add_faculty_name_{i}")
        faculty_members.append(faculty_name)
    
    # Group Members
    st.subheader("Group Members")
    num_members = st.number_input("Number of Members", min_value=1, max_value=8, value=1, key="add_num_members")
    members = []
    for i in range(num_members):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input(f"Member {i+1} Name", key=f"add_member_name_{i}")
        with col2:
            roll_no = st.text_input(f"Roll Number", key=f"add_member_roll_{i}")
        with col3:
            contribution = st.text_area(f"Contribution", key=f"add_member_contribution_{i}")
        
        members.append({
            "name": name,
            "roll_no": roll_no,
            "contribution": contribution
        })
    
    # Image Upload
    uploaded_images = st.file_uploader("Upload Group Images", 
                                       type=['png', 'jpg', 'jpeg'], 
                                       accept_multiple_files=True,
                                       key="add_image_uploader")
    
    # Convert images to base64
    image_data = [image_to_base64(img) for img in uploaded_images]
    # image_data = ["abc", "def"]
    
    # Submit Button
    if st.button("Submit Group Details", key="add_submit_button"):
        # Validate inputs
        if not group_no or not project_name:
            st.error("Group Number and Project Name are required!")
            return
        
        # Prepare payload
        emailUsed = "Not Provided"
        
        if st.session_state.get('emailUsed'):
            emailUsed = st.session_state.get('emailUsed')
        
        payload = {
            "Group_number": int(group_no),
            "project_name": project_name,
            "Description": description,
            "Faculty": [f for f in faculty_members if f],  # Remove empty faculty names
            "members": [m for m in members if m['name']],  # Remove members without names
            "image": image_data,
            "emailUsed" : emailUsed
        }
        # print("hello")
        
        try:
            # Send POST request to backend
            # print("test")
            
            response = requests.post(f"{BASE_URL}/groups", json=payload)
            # print("test2")
            # print("payload: ", payload)
            
            if response.status_code in [200, 201]:
                st.success("Group added successfully!")
            else:
                st.error(f"Failed to add group: {response.text}")
            
            # print("response: ", response.status_code)
            # print("test")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error submitting group: {e}")
            # print("test")
            

# View Groups Functionality
# View Groups Functionality
def view_groups():
    st.header("View Groups")
    
    # Option to view all or specific group
    view_option = st.radio("View Option", ["All Groups", "Specific Group"], key="view_option")
    
    if view_option == "All Groups":
        # Fetch all groups
        try:
            response = requests.get(f"{BASE_URL}/groups")
            if response.status_code == 200:
                groups = response.json()
                print(groups)
                
                if not groups:
                    st.info("No groups found.")
                else:
                    for group in groups:
                        with st.expander(f"Group {group.get('groupNumber', 'N/A')} - {group.get('projectName', 'Untitled')}"):
                            st.json(group)
            else:
                st.error(f"Failed to fetch groups: {response.text}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching groups: {e}")
    
    else:
        # View specific group
        group_no = st.text_input("Enter Group Number", key="view_group_no")
        
        if st.button("Search", key="view_search_button"):
            try:
                response = requests.get(f"{BASE_URL}/{group_no}")
                
                if response.status_code == 200:
                    group = response.json()
                    st.subheader(f"Group {group.get('groupNumber', 'N/A')}")
                    st.json(group)
                
                elif response.status_code == 404:
                    st.warning(f"No group found with number {group_no}")
                
                else:
                    st.error(f"Failed to fetch group: {response.text}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching group: {e}")


# Function to fetch and display the group list
def display_group_list(api_url = 'http://gatherhub-r7yr.onrender.com/user/conference/DP2024/groups/groupList'):
    """
    Fetch and display the group list from the backend API.

    Parameters:
        api_url (str): The URL of the backend API endpoint.
    """
    @st.cache_data  # Cache the response to optimize performance
    def fetch_group_list():
        try:
            response = requests.get(api_url)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Failed to fetch group list. Status code: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")
            return []

    # Fetch group list
    group_list = fetch_group_list()

    # Display the group list
    st.title("📋 Group List")
    if group_list:
        # Convert list of groups to a DataFrame for display
        df = pd.DataFrame(group_list)

        # Show data in a table
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No group data available.")

# Run the app
if __name__ == "__main__":
    main_group()