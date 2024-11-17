import streamlit as st
from pymongo import MongoClient
import atexit
from datetime import datetime

# MongoDB connection
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://sahniwesh:Cg1pipueVvULDzdk@testing.4soqq.mongodb.net/")
    atexit.register(client.close)  # Ensure client disconnects on exit
    db = client['attendance_tracker']
    return db['about']  # Replace with your actual collection name

# Initialize MongoDB collection
posts_collection = connect_to_mongodb()

def post_content():
    st.title("Add Post")

    # Input fields for post information
    title = st.text_input("Post Title")
    content = st.text_area("Post Content")
    
    current_time = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

    # Button to add post to the database
    if st.button("Add Post"):
        if title and content:
            post_data = {
                'title': title,
                'content': content,
                'lastModified': current_time
            }
            try:
                posts_collection.insert_one(post_data)
                st.success("Post added successfully!")
            except Exception as e:
                st.error(f"Failed to add post: {str(e)}")
        else:
            st.error("Please fill in both the title and content.")

    # Display all posts in the database with delete option
    st.header("Posts List")
    posts = list(posts_collection.find())

    for post in posts:
        st.subheader(f"Title: {post['title']}")
        st.write(post['content'])
        
        # Button to delete post
        if st.button(f"Delete {post['title']}", key=post['_id']):
            try:
                posts_collection.delete_one({'_id': post['_id']})
                st.success(f"{post['title']} deleted successfully!")
                st.rerun()  # Refresh the page to reflect the deletion
            except Exception as e:
                st.error(f"Failed to delete {post['title']}: {str(e)}")

        st.write("---")