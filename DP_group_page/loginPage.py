# import streamlit as st
# import requests
# import base64

# # Backend Base URL (replace with your actual backend API URL)
# BASE_URL = "http://your-backend-url.com"

# # Helper function to convert images to base64
# def image_to_base64(image):
#     if image is not None:
#         img_bytes = image.read()
#         return base64.b64encode(img_bytes).decode('utf-8')
#     return None

# # Main App Function
# def main():
#     st.title("Group Management System")
    
#     # Create a sidebar for navigation
#     menu = ["Add New Group", "View Groups", "Edit Group"]
#     choice = st.sidebar.selectbox("Navigation", menu)

#     if choice == "Add New Group":
#         add_group()
#     elif choice == "View Groups":
#         view_groups()
#     elif choice == "Edit Group":
#         edit_group()

# # Add New Group Functionality
# def add_group():
#     st.header("Add New Group")
    
#     # Group Basic Information
#     group_no = st.text_input("Group Number")
#     project_name = st.text_input("Project Name")
#     description = st.text_area("Project Description")
    
#     # Faculty Members
#     st.subheader("Faculty Members")
#     num_faculty = st.number_input("Number of Faculty", min_value=1, max_value=5, value=1)
#     faculty_members = []
#     for i in range(num_faculty):
#         faculty_name = st.text_input(f"Faculty Member {i+1} Name")
#         faculty_members.append(faculty_name)
    
#     # Group Members
#     st.subheader("Group Members")
#     num_members = st.number_input("Number of Members", min_value=1, max_value=8, value=1)
#     members = []
#     for i in range(num_members):
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             name = st.text_input(f"Member {i+1} Name")
#         with col2:
#             roll_no = st.text_input(f"Roll Number")
#         with col3:
#             contribution = st.text_area(f"Contribution")
        
#         members.append({
#             "name": name,
#             "roll_no": roll_no,
#             "contribution": contribution
#         })
    
#     # Image Upload
#     uploaded_images = st.file_uploader("Upload Group Images", 
#                                        type=['png', 'jpg', 'jpeg'], 
#                                        accept_multiple_files=True)
    
#     # Convert images to base64
#     image_data = [image_to_base64(img) for img in uploaded_images]
    
#     # Submit Button
#     if st.button("Submit Group Details"):
#         # Validate inputs
#         if not group_no or not project_name:
#             st.error("Group Number and Project Name are required!")
#             return
        
#         # Prepare payload
#         payload = {
#             "group_no": group_no,
#             "project_name": project_name,
#             "description": description,
#             "faculty_members": [f for f in faculty_members if f],  # Remove empty faculty names
#             "members": [m for m in members if m['name']],  # Remove members without names
#             "images": image_data
#         }
        
#         try:
#             # Send POST request to backend
#             response = requests.post(f"{BASE_URL}/groups", json=payload)
            
#             if response.status_code in [200, 201]:
#                 st.success("Group added successfully!")
#             else:
#                 st.error(f"Failed to add group: {response.text}")
        
#         except requests.exceptions.RequestException as e:
#             st.error(f"Error submitting group: {e}")

# # View Groups Functionality
# def view_groups():
#     st.header("View Groups")
    
#     # Option to view all or specific group
#     view_option = st.radio("View Option", ["All Groups", "Specific Group"])
    
#     if view_option == "All Groups":
#         # Fetch all groups
#         try:
#             response = requests.get(f"{BASE_URL}/groups")
#             if response.status_code == 200:
#                 groups = response.json()
                
#                 if not groups:
#                     st.info("No groups found.")
#                 else:
#                     for group in groups:
#                         with st.expander(f"Group {group.get('group_no', 'N/A')} - {group.get('project_name', 'Untitled')}"):
#                             st.json(group)
#             else:
#                 st.error(f"Failed to fetch groups: {response.text}")
        
#         except requests.exceptions.RequestException as e:
#             st.error(f"Error fetching groups: {e}")
    
#     else:
#         # View specific group
#         group_no = st.text_input("Enter Group Number")
        
#         if st.button("Search"):
#             try:
#                 response = requests.get(f"{BASE_URL}/groups/{group_no}")
                
#                 if response.status_code == 200:
#                     group = response.json()
#                     st.subheader(f"Group {group.get('group_no', 'N/A')}")
#                     st.json(group)
                
#                 elif response.status_code == 404:
#                     st.warning(f"No group found with number {group_no}")
                
#                 else:
#                     st.error(f"Failed to fetch group: {response.text}")
            
#             except requests.exceptions.RequestException as e:
#                 st.error(f"Error fetching group: {e}")

# # Edit Group Functionality
# def edit_group():
#     st.header("Edit Group Details")
    
#     # Search for group to edit
#     group_no = st.text_input("Enter Group Number to Edit")
    
#     if st.button("Fetch Group Details"):
#         try:
#             response = requests.get(f"{BASE_URL}/groups/{group_no}")
            
#             if response.status_code == 200:
#                 group = response.json()
                
#                 # Prefill form with existing group details
#                 st.subheader("Edit Group Information")
                
#                 project_name = st.text_input("Project Name", value=group.get('project_name', ''))
#                 description = st.text_area("Project Description", value=group.get('description', ''))
                
#                 # Edit Faculty Members
#                 st.subheader("Faculty Members")
#                 faculty_members = group.get('faculty_members', [])
#                 updated_faculty = []
#                 for i, faculty in enumerate(faculty_members, 1):
#                     updated_faculty_name = st.text_input(f"Faculty Member {i}", value=faculty)
#                     updated_faculty.append(updated_faculty_name)
                
#                 # Add option to add more faculty members
#                 add_more_faculty = st.checkbox("Add More Faculty Members")
#                 if add_more_faculty:
#                     new_faculty = st.text_input("New Faculty Member Name")
#                     if new_faculty:
#                         updated_faculty.append(new_faculty)
                
#                 # Edit Group Members
#                 st.subheader("Group Members")
#                 members = group.get('members', [])
#                 updated_members = []
                
#                 for i, member in enumerate(members, 1):
#                     st.subheader(f"Member {i}")
#                     name = st.text_input(f"Member {i} Name", value=member.get('name', ''))
#                     roll_no = st.text_input(f"Roll Number", value=member.get('roll_no', ''))
#                     contribution = st.text_area(f"Contribution", value=member.get('contribution', ''))
                    
#                     updated_members.append({
#                         "name": name,
#                         "roll_no": roll_no,
#                         "contribution": contribution
#                     })
                
#                 # Option to add more members
#                 add_more_members = st.checkbox("Add More Members")
#                 if add_more_members:
#                     new_name = st.text_input("New Member Name")
#                     new_roll_no = st.text_input("New Member Roll Number")
#                     new_contribution = st.text_area("New Member Contribution")
                    
#                     if new_name:
#                         updated_members.append({
#                             "name": new_name,
#                             "roll_no": new_roll_no,
#                             "contribution": new_contribution
#                         })
                
#                 # Update Button
#                 if st.button("Update Group Details"):
#                     payload = {
#                         "project_name": project_name,
#                         "description": description,
#                         "faculty_members": [f for f in updated_faculty if f],
#                         "members": [m for m in updated_members if m['name']]
#                     }
                    
#                     try:
#                         update_response = requests.put(f"{BASE_URL}/groups/{group_no}", json=payload)
                        
#                         if update_response.status_code == 200:
#                             st.success("Group details updated successfully!")
#                         else:
#                             st.error(f"Failed to update group: {update_response.text}")
                    
#                     except requests.exceptions.RequestException as e:
#                         st.error(f"Error updating group: {e}")
            
#             elif response.status_code == 404:
#                 st.warning(f"No group found with number {group_no}")
            
#             else:
#                 st.error(f"Failed to fetch group: {response.text}")
        
#         except requests.exceptions.RequestException as e:
#             st.error(f"Error fetching group: {e}")

# # Run the app
# if __name__ == "__main__":
#     main()








































import streamlit as st
import requests
import base64
import pandas as pd

# Backend Base URL (replace with your actual backend API URL)
# BASE_URL = "http://gatherhub-r7yr.onrender.com/user/conference/DP2024/groups/"
BASE_URL = "http://localhost:27017/user/conference/DP2024"
# Helper function to convert images to base64

def image_to_base64(image):
    if image is not None:
        img_bytes = image.read()
        return base64.b64encode(img_bytes).decode('utf-8')
    return None

# Main App Function
def main():
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
        payload = {
            "Group_number": int(group_no),
            "project_name": project_name,
            "Description": description,
            "Faculty": [f for f in faculty_members if f],  # Remove empty faculty names
            "members": [m for m in members if m['name']],  # Remove members without names
            "image": image_data
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


# Edit Group Functionality
def edit_group():
    st.header("Edit Group Details")
    
    # Initialize session state variables
    if 'new_members' not in st.session_state:
        st.session_state.new_members = []  # Stores newly added members
    if 'add_more_members' not in st.session_state:
        st.session_state.add_more_members = False  # Tracks if more members are being added

    # Helper function to toggle 'add_more_members'
    def toggle_add_more_members():
        st.session_state.add_more_members = not st.session_state.add_more_members

    # Search for group to edit
    group_no = st.text_input("Enter Group Number to Edit", key="edit_group_no")
    
    if st.button("Fetch Group Details", key="edit_fetch_button"):
        try:
            url = f"{BASE_URL}/groups/{group_no}"
            response = requests.get(url)
            
            if response.status_code == 200:
                group = response.json()
                
                # Prefill form with existing group details
                st.subheader("Edit Group Information")
                project_name = st.text_input("Project Name", value=group.get('project_name', ''), key="edit_project_name")
                description = st.text_area("Project Description", value=group.get('Description', ''), key="edit_description")
                
                # Edit Faculty Members
                st.subheader("Faculty Members")
                faculty_members = group.get('Faculty', [])
                updated_faculty = []
                for i, faculty in enumerate(faculty_members, 1):
                    updated_faculty_name = st.text_input(f"Faculty Member {i}", value=faculty, key=f"edit_faculty_{i}")
                    updated_faculty.append(updated_faculty_name)
                
                # Option to add more faculty members
                add_more_faculty = st.checkbox("Add More Faculty Members", key="edit_add_faculty_checkbox")
                if add_more_faculty:
                    new_faculty = st.text_input("New Faculty Member Name", key="edit_new_faculty")
                    if new_faculty:
                        updated_faculty.append(new_faculty)
                
                # Edit Group Members
                st.subheader("Group Members")
                members = group.get('members', [])
                updated_members = []
                
                for i, member in enumerate(members, 1):
                    st.subheader(f"Member {i}")
                    name = st.text_input(f"Member {i} Name", value=member.get('name', ''), key=f"edit_member_name_{i}")
                    roll_no = st.text_input(f"Roll Number", value=member.get('roll_no', ''), key=f"edit_member_roll_{i}")
                    contribution = st.text_area(f"Contribution", value=member.get('contribution', ''), key=f"edit_member_contribution_{i}")
                    
                    updated_members.append({
                        "name": name,
                        "roll_no": roll_no,
                        "contribution": contribution
                    })
                
                # Add More Members Section
                st.subheader("Add More Members")
                if st.checkbox("Add More Members", key="edit_add_members_checkbox", value=st.session_state.add_more_members, 
                               on_change=toggle_add_more_members):
                    new_name = st.text_input("New Member Name", key="edit_new_member_name")
                    new_roll_no = st.text_input("New Member Roll Number", key="edit_new_member_roll")
                    new_contribution = st.text_area("New Member Contribution", key="edit_new_member_contribution")
                    
                    if st.button("Add Member", key="add_member_button"):
                        if new_name:
                            st.session_state.new_members.append({
                                "name": new_name,
                                "roll_no": new_roll_no,
                                "contribution": new_contribution
                            })
                
                # Display newly added members
                if st.session_state.new_members:
                    st.subheader("New Members")
                    for i, new_member in enumerate(st.session_state.new_members, 1):
                        st.write(f"{i}. Name: {new_member['name']}, Roll Number: {new_member['roll_no']}, Contribution: {new_member['contribution']}")
                
                # Combine updated members and newly added members
                all_members = updated_members + st.session_state.new_members
                
                # Update Button
                if st.button("Update Group Details", key="edit_update_button"):
                    payload = {
                        "project_name": project_name,
                        "description": description,
                        "faculty_members": [f for f in updated_faculty if f],
                        "members": [m for m in all_members if m['name']]
                    }
                    
                    try:
                        update_response = requests.put(f"{BASE_URL}/groups/{group_no}", json=payload)
                        
                        if update_response.status_code == 200:
                            st.success("Group details updated successfully!")
                            # Reset state after successful update
                            st.session_state.add_more_members = False
                            st.session_state.new_members = []
                        else:
                            st.error(f"Failed to update group: {update_response.text}")
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error updating group: {e}")
            
            elif response.status_code == 404:
                st.warning(f"No group found with number {group_no}")
            
            else:
                st.error(f"Failed to fetch group: {response.text}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching group: {e}")


# Run the app
if __name__ == "__main__":
    main()