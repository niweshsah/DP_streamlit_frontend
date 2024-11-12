import streamlit as st
from pymongo import MongoClient
from PIL import Image
import io
import base64
import atexit
from datetime import datetime

# Get the current UTC time in ISO 8601 format with milliseconds

# MongoDB connection
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://sahniwesh:Cg1pipueVvULDzdk@testing.4soqq.mongodb.net/")
    atexit.register(client.close)  # Ensure client disconnects on exit
    db = client['attendance_tracker']
    return db['mentors']  # Replace with your actual collection name

# Convert image to base64
def image_to_base64(image, format="PNG"):
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode()

# Initialize MongoDB collection
mentors_collection = connect_to_mongodb()

def mentor():
    st.title("Add Mentor Information")
    
    # Input fields for mentor information
    name = st.text_input("Mentor Name")
    profession = st.text_input("Profession")
    uploaded_file = st.file_uploader("Upload Mentor Photo", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        img_base64 = image_to_base64(image, format=uploaded_file.type.split('/')[1].upper())
    else:
        img_base64 = None

    current_time = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

    # Button to add mentor to the database
    if st.button("Add Mentor"):
        if name and profession and img_base64:
            mentor_data = {
                'name': name,
                'photo': img_base64,
                'profession': profession,
                'lastModified': current_time
            }
            try:
                mentors_collection.insert_one(mentor_data)
                st.success("Mentor added successfully!")
            except Exception as e:
                st.error(f"Failed to add mentor: {str(e)}")
        else:
            st.error("Please fill in all fields and upload a photo.")

    # Display all mentors in the database with delete option
    st.header("Mentor List")
    mentors = list(mentors_collection.find())

    for mentor in mentors:
        st.subheader(f"Name: {mentor['name']}")
        st.write(f"Profession: {mentor['profession']}")
        st.image(Image.open(io.BytesIO(base64.b64decode(mentor['photo']))), caption=mentor['name'], width=150)
        
        # Button to delete mentor
        if st.button(f"Delete {mentor['name']}", key=mentor['_id']):
            try:
                mentors_collection.delete_one({'_id': mentor['_id']})
                st.success(f"{mentor['name']} deleted successfully!")
                st.rerun()  # Refresh the page to reflect the deletion
            except Exception as e:
                st.error(f"Failed to delete {mentor['name']}: {str(e)}")

        st.write("---")

# Run the app
# if __name__ == "__main__":
#     main()
