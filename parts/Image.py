import streamlit as st
from pymongo import MongoClient
from PIL import Image
import io
import base64
from bson.objectid import ObjectId
import atexit

# MongoDB connection
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://sahniwesh:Cg1pipueVvULDzdk@testing.4soqq.mongodb.net/")
    atexit.register(client.close)  # Ensure client disconnects on exit
    db = client['attendance_tracker']
    return db['images']

# Convert image to base64
def image_to_base64(image, format="PNG"):
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode()

# Convert base64 to image
def base64_to_image(base64_string):
    return Image.open(io.BytesIO(base64.b64decode(base64_string)))

# Initialize MongoDB collection
images_collection = connect_to_mongodb()

def main_Image():
    st.title("Image Manager")
    
    # Upload new image
    st.header("Upload New Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        if uploaded_file.type not in ['image/png', 'image/jpeg']:
            st.error("Unsupported file format. Please upload PNG or JPEG images.")
        else:
            # Open and resize image
            image = Image.open(uploaded_file)
            resized_image = image.resize((200, 200))
            
            # Convert to base64 for storage
            img_base64 = image_to_base64(resized_image, format=uploaded_file.type.split('/')[1].upper())
            
            # Get current highest order
            highest_order = images_collection.find_one(sort=[("order", -1)])
            new_order = 1 if not highest_order else highest_order['order'] + 1
            
            # Insert into MongoDB
            if st.button("Add Image"):
                try:
                    images_collection.insert_one({
                        'image': img_base64,
                        'order': new_order
                    })
                    st.success(f"Image added successfully with order {new_order}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to add image: {str(e)}")

    # Display all images
    st.header("Current Images")
    images = list(images_collection.find().sort("order"))
    
    if not images:
        st.write("No images uploaded yet")
    else:
        cols = st.columns(3)
        for idx, img_data in enumerate(images):
            with cols[idx % 3]:
                # Display image
                img = base64_to_image(img_data['image'])
                st.image(img, caption=f"Image {img_data['order']}")

                # Delete button
                if st.button(f"Delete Image {img_data['order']}", key=f"del_{img_data['_id']}"):
                    try:
                        images_collection.delete_one({'_id': img_data['_id']})
                        st.success(f"Image {img_data['order']} deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to delete image: {str(e)}")

                # Update image
                new_img = st.file_uploader(f"Update Image {img_data['order']}", key=f"update_{img_data['_id']}", type=['png', 'jpg', 'jpeg'])
                if new_img:
                    updated_image = Image.open(new_img)
                    resized_updated = updated_image.resize((200, 200))
                    updated_base64 = image_to_base64(resized_updated, format=new_img.type.split('/')[1].upper())

                    if st.button(f"Confirm Update {img_data['order']}", key=f"confirm_{img_data['_id']}"):
                        try:
                            images_collection.update_one(
                                {'_id': img_data['_id']},
                                {'$set': {'image': updated_base64}}
                            )
                            st.success(f"Image {img_data['order']} updated")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to update image: {str(e)}")

    # Reorder images
    if images:
        st.header("Reorder Images")
        col1, col2 = st.columns(2)
        with col1:
            source_order = st.selectbox("Select Image to Move", [img['order'] for img in images])
        with col2:
            target_order = st.selectbox("Move to Position", [img['order'] for img in images])
        
        if st.button("Reorder"):
            if source_order != target_order:
                try:
                    # Get the images to swap
                    source_img = images_collection.find_one({'order': source_order})
                    
                    if source_order < target_order:
                        # Move images down
                        images_collection.update_many(
                            {'order': {'$gt': source_order, '$lte': target_order}},
                            {'$inc': {'order': -1}}
                        )
                    else:
                        # Move images up
                        images_collection.update_many(
                            {'order': {'$lt': source_order, '$gte': target_order}},
                            {'$inc': {'order': 1}}
                        )
                    
                    # Update source image order
                    images_collection.update_one(
                        {'_id': source_img['_id']},
                        {'$set': {'order': target_order}}
                    )

                    st.success("Images reordered successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to reorder images: {str(e)}")

# if __name__ == "__main__":
#     main()
