import streamlit as st
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate with Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Opens a web browser for authentication
drive = GoogleDrive(gauth)

# Streamlit UI
st.title("Upload Your Photos to Google Drive")

# Get the login name from the user
login_name = st.text_input("Enter your login name")

if login_name:
    # Check if a folder named with the user's login name exists
    folder_list = drive.ListFile({'q': f"title='{login_name}' and mimeType='application/vnd.google-apps.folder'"}).GetList()

    if not folder_list:
        # Create a new folder if it doesn't exist
        folder = drive.CreateFile({'title': login_name, 'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        st.success(f"Folder '{login_name}' created successfully.")
    else:
        folder = folder_list[0]
        st.success(f"Using existing folder '{login_name}'.")

    # File uploader widget
    uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save file temporarily
            temp_path = f'./{uploaded_file.name}'
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Upload the file to the specific user's folder
            file_drive = drive.CreateFile({'title': uploaded_file.name, 'parents': [{'id': folder['id']}]})
            file_drive.SetContentFile(temp_path)
            file_drive.Upload()


            st.success(f'File {uploaded_file.name} uploaded successfully to Google Drive in folder {login_name}.')


            # Clean up the temporary file
            os.remove(temp_path)
else:
    st.info("Please enter your login name to create or access your folder.")
 