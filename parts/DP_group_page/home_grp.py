# app.py
import streamlit as st
import requests
import base64


def image_to_base64(image):
    """Convert uploaded image to base64 string."""
    if image is not None:
        # Read the image file
        img_bytes = image.read()
        # Encode to base64
        return base64.b64encode(img_bytes).decode('utf-8')
    return None




def main():
    st.title("Group Details Submission")

    # Group Number input
    # group_no = st.text_input("Group Number")
    # group_no = st.text_input("Group Number")
    group_no = st.text_input("Group Number").strip()


    # Group Description
    Project_name = st.text_input("Project Name")
    description = st.text_area("Project Description")


    # Faculty input (now supporting multiple faculty members)
    st.subheader("Faculty Members")
    num_faculty = st.number_input("Number of Faculty", min_value=1, max_value=5, value=1)
    
    faculty_members = []
    for i in range(num_faculty):
        faculty_name = st.text_input(f"Faculty Member {i+1} Name")
        if faculty_name:
            faculty_members.append(faculty_name)


    # Image upload
    uploaded_images = st.file_uploader("Upload Group Images", 
                                       type=['png', 'jpg', 'jpeg'], 
                                       accept_multiple_files=True)



    # Member details
    st.subheader("Group Members")
    num_members = st.number_input("Number of Members", min_value=1, max_value=8, value=1)

    members = []
    for i in range(num_members):
        st.write(f"Member {i+1}")
        name = st.text_input(f"Member {i+1} Name")
        roll_no = st.text_input(f"Member {i+1} Roll Number")
        contribution = st.text_area(f"Member {i+1} Contribution")
      
        
        members.append({
            "name": name,
            "roll_no": roll_no,
            "contribution": contribution
        })


    # Submission button
    if st.button("Submit Group Details"):
        # Validate inputs
        if not group_no or not description or not faculty_members or not members:
            st.error("Please fill in all required fields")
            return


        # Prepare image data
        image_data = []
        if uploaded_images:
            for img in uploaded_images:
                base64_img = image_to_base64(img)
                if base64_img:
                    image_data.append(base64_img)




        # Prepare payload to match the mongoose schema
        payload = {
            group_no: [
                {
                    "Description": description,
                    "Faculty": faculty_members,
                    "image": image_data,
                    "members": members
                }
            ]
        }

        # TODO: Replace with your actual backend URL
        backend_url = "http://your-backend-url.com/submit-group"

        try:
            # Send POST request
            response = requests.post(backend_url, json=payload)
            
            if response.status_code == 200:
                st.success("Group details submitted successfully!")
                # Optional: Clear form after successful submission
                st.rerun()
            else:
                st.error(f"Submission failed. Status code: {response.status_code}")
                st.error(f"Response: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error submitting group details: {e}")


if __name__ == "__main__":
    main()
    
    
