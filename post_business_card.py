# import streamlit as st
# import requests

# # Page configuration
# st.set_page_config(
#     page_title="Digital Business Card Submission",
#     page_icon="🖋️",
#     layout="centered"
# )

# # Title and description
# st.title("🖋️ Submit Your Digital Business Card Info")
# st.markdown(
#     """
#     Fill in the details below to create your digital business card. 
#     Once submitted, the information will be saved securely.
#     """
# )

# # User input fields
# name = st.text_input("Full Name", placeholder="Enter your full name")
# email = st.text_input("Email", placeholder="Enter your email address")
# mobile = st.text_input("Mobile Number", placeholder="Enter your mobile number")
# designation = st.text_input("Designation", placeholder="Enter your designation")
# organization = st.text_input("Organization", placeholder="Enter your organization name")
# location = st.text_input("Location", placeholder="Enter your location (e.g., City, Country)")
# linkedin = st.text_input("LinkedIn Profile URL", placeholder="Enter your LinkedIn profile URL")
# about = st.text_area("About Me", placeholder="Write a short description about yourself")
# # avatar_url = st.text_input("Avatar URL (optional)", placeholder="Enter a URL for your profile picture")

# # Submission URL
# submit_url = "https://gatherhub-r7yr.onrender.com/user/businessCard/posting"

# # Submit button
# if st.button("Submit"):
#     # Prepare the payload
#     payload = {
#         "name": name,
#         "email": email,
#         "mobile": mobile,
#         "designation": designation,
#         "organization": organization,
#         "about": about,
#         "linkedIn": linkedin,
#         "location": location
#         # "avatar_url": avatar_url
#     }


#     # Validate inputs
#     if not name or not email or not mobile:
#         st.error("Please fill in all required fields (Name, Email, and Mobile).")
#     else:
#         try:
#             # Send POST request
#             response = requests.post(submit_url, json=payload)
#             if response.status_code == 201:
#                 response_json = response.json()
#                 id = response_json.get("_id")
#                 st.success("🎉 Your information has been submitted successfully!")
                
                
                
#             else:
#                 st.error(f"Failed to submit. Server responded with status: {response.status_code}")
#                 st.error(f"Response: {response.text}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"An error occurred: {e}")





























import streamlit as st
import requests
import qrcode
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Digital Business Card Submission",
    page_icon="🖋️",
    layout="centered"
)

# Title and description
st.title("🖋️ Submit Your Digital Business Card Info")
st.markdown(
    """
    Fill in the details below to create your digital business card. 
    Once submitted, the information will be saved securely.
    """
)

# User input fields
name = st.text_input("Full Name", placeholder="Enter your full name")
email = st.text_input("Email", placeholder="Enter your email address")
mobile = st.text_input("Mobile Number", placeholder="Enter your mobile number")
designation = st.text_input("Designation", placeholder="Enter your designation")
organization = st.text_input("Organization", placeholder="Enter your organization name")
location = st.text_input("Location", placeholder="Enter your location (e.g., City, Country)")
linkedin = st.text_input("LinkedIn Profile URL", placeholder="Enter your LinkedIn profile URL")
about = st.text_area("About Me", placeholder="Write a short description about yourself")
# avatar_url = st.text_input("Avatar URL (optional)", placeholder="Enter a URL for your profile picture")

# Submission URL
submit_url = "https://gatherhub-r7yr.onrender.com/user/businessCard/posting"

# Submit button
if st.button("Submit"):
    # Prepare the payload
    payload = {
        "name": name,
        "email": email,
        "mobile": mobile,
        "designation": designation,
        "organization": organization,
        "about": about,
        "linkedIn": linkedin,
        "location": location
        # "avatar_url": avatar_url
    }

    # Validate inputs
    if not name or not email or not mobile:
        st.error("Please fill in all required fields (Name, Email, and Mobile).")
    else:
        try:
            # Send POST request
            response = requests.post(submit_url, json=payload)
            if response.status_code == 201:
                response_json = response.json()
                id = response_json.get("_id")
                st.success("🎉 Your information has been submitted successfully!")
                
                # Generate the QR code
                # qr_data = f"https://gatherhub-r7yr.onrender.com/user/businessCard/getInfo/{id}"
                qr_data = f"https://niweshvistingcard.streamlit.app/?userId={id}"
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_data)
                qr.make(fit=True)

                # Save QR code to a BytesIO object
                qr_image = qr.make_image(fill="black", back_color="white")
                buffer = BytesIO()
                qr_image.save(buffer, format="PNG")
                buffer.seek(0)

                # Display QR code
                st.image(buffer, caption="Scan this QR code to view your business card info.", use_column_width=True)
            else:
                st.error(f"Failed to submit. Server responded with status: {response.status_code}")
                st.error(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

