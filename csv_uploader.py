
# MongoDB connection
# def connect_to_mongodb():
#     client = MongoClient("mongodb+srv://sahniwesh:Cg1pipueVvULDzdk@testing.4soqq.mongodb.net/")
#     atexit.register(client.close)  # Ensure client disconnects on exit
#     db = client['attendance_tracker']
#     return db['about']  # Replace with your actual collection name


import streamlit as st
import pandas as pd
from pymongo import MongoClient
import json
from datetime import datetime

# Initialize MongoDB connection
def init_mongo_client():
    try:
        # Replace with your MongoDB connection string
        client = MongoClient("mongodb+srv://sahniwesh:Cg1pipueVvULDzdk@testing.4soqq.mongodb.net/")
        atexit.register(client.close)  # Ensure client disconnects on exit
        db = client['attendance_tracker']
        return db['about']  # Replace with your actual collection name
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

def process_file(uploaded_file, collection):
    try:
        # Get file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Read file based on extension
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload CSV or Excel files only.")
            return False
        
        # Convert DataFrame to list of dictionaries
        records = json.loads(df.to_json(orient='records'))
        
        # Add metadata to each record
        for record in records:
            record['upload_timestamp'] = datetime.now()
            record['source_file'] = uploaded_file.name
        
        # Insert records into MongoDB
        result = collection.insert_many(records)
        
        return len(result.inserted_ids)
    
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return False

def main():
    st.title("MongoDB File Uploader")
    
    # Initialize MongoDB connection
    collection = init_mongo_client()
    if collection is None:  # Changed from 'if not collection'
        st.error("Failed to connect to MongoDB. Please check your connection string.")
        return
    
    # File upload widget
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=['csv', 'xlsx', 'xls']
    )
    
    if uploaded_file:
        # Display file details
        st.write("File Details:")
        st.write(f"- Filename: {uploaded_file.name}")
        st.write(f"- File size: {uploaded_file.size} bytes")
        
        # Preview data
        if uploaded_file.name.endswith('csv'):
            df_preview = pd.read_csv(uploaded_file)
        else:
            df_preview = pd.read_excel(uploaded_file)
        
        st.write("Data Preview:")
        st.dataframe(df_preview.head())
        
        # Upload button
        if st.button("Upload to MongoDB"):
            with st.spinner("Uploading data to MongoDB..."):
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                
                # Process and upload file
                inserted_count = process_file(uploaded_file, collection)
                
                if inserted_count:
                    st.success(f"Successfully uploaded {inserted_count} records to MongoDB!")
                    
                    # Display collection stats
                    total_documents = collection.count_documents({})
                    st.write(f"Total documents in collection: {total_documents}")
                else:
                    st.error("Failed to upload data to MongoDB.")

if __name__ == "__main__":
    main()