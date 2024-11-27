import streamlit as st
import requests
import json

# Configuration - replace with your actual backend API URL
API_BASE_URL = "http://localhost:3000/groups"  # Adjust this to your actual backend URL

def create_group(group_data):
    """Create a new group"""
    try:
        response = requests.post(API_BASE_URL, json=group_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating group: {e}")
        return None

def get_all_groups():
    """Retrieve all groups"""
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching groups: {e}")
        return []

def get_group_by_id(group_id):
    """Retrieve a specific group by ID"""
    try:
        response = requests.get(f"{API_BASE_URL}/{group_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching group: {e}")
        return None

def update_group(group_id, group_data):
    """Update an existing group"""
    try:
        response = requests.put(f"{API_BASE_URL}/{group_id}", json=group_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating group: {e}")
        return None

def delete_group(group_id):
    """Delete a group"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{group_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting group: {e}")
        return False

def main():
    st.title("Group Management System")
    
    # Sidebar for navigation
    menu = ["Create", "View", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    # Create Group
    if choice == "Create":
        st.subheader("Create New Group")
        
        # Dynamic form fields based on your Group model
        name = st.text_input("Group Name")
        description = st.text_area("Group Description")
        
        # Add more fields as needed based on your Group model
        
        if st.button("Create Group"):
            group_data = {
                "name": name,
                "description": description
                # Add more fields as needed
            }
            
            result = create_group(group_data)
            if result:
                st.success("Group created successfully!")
                st.json(result)
    
    # View Groups
    elif choice == "View":
        st.subheader("View Groups")
        
        # Option to view all or by specific ID
        view_mode = st.radio("View Mode", ["All Groups", "Specific Group"])
        
        if view_mode == "All Groups":
            groups = get_all_groups()
            if groups:
                for group in groups:
                    st.write(f"ID: {group.get('_id')}")
                    st.json(group)
        else:
            group_id = st.text_input("Enter Group ID")
            if st.button("Fetch Group"):
                group = get_group_by_id(group_id)
                if group:
                    st.json(group)
    
    # Update Group
    elif choice == "Update":
        st.subheader("Update Group")
        
        group_id = st.text_input("Group ID to Update")
        
        # Fetch existing group details
        if st.button("Fetch Group Details"):
            group = get_group_by_id(group_id)
            if group:
                # Prepopulate fields
                name = st.text_input("Group Name", group.get('name', ''))
                description = st.text_area("Group Description", group.get('description', ''))
                
                if st.button("Update Group"):
                    updated_data = {
                        "name": name,
                        "description": description
                        # Add more fields as needed
                    }
                    
                    result = update_group(group_id, updated_data)
                    if result:
                        st.success("Group updated successfully!")
                        st.json(result)
    
    # Delete Group
    elif choice == "Delete":
        st.subheader("Delete Group")
        
        group_id = st.text_input("Group ID to Delete")
        
        if st.button("Delete Group"):
            if delete_group(group_id):
                st.success("Group deleted successfully!")

if __name__ == "__main__":
    main()