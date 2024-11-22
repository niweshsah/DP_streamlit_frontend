

# import streamlit as st
# import requests
# import qrcode
# from io import BytesIO
# from PIL import Image

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
                
#                 # Generate the QR code
#                 # qr_data = f"https://gatherhub-r7yr.onrender.com/user/businessCard/getInfo/{id}"
#                 qr_data = f"https://niweshvistingcard.streamlit.app/?userId={id}"
#                 qr = qrcode.QRCode(
#                     version=1,
#                     error_correction=qrcode.constants.ERROR_CORRECT_L,
#                     box_size=10,
#                     border=4,
#                 )
#                 qr.add_data(qr_data)
#                 qr.make(fit=True)

#                 # Save QR code to a BytesIO object
#                 qr_image = qr.make_image(fill="black", back_color="white")
#                 buffer = BytesIO()
#                 qr_image.save(buffer, format="PNG")
#                 buffer.seek(0)

#                 # Display QR code
#                 st.image(buffer, caption="Scan this QR code to view your business card info.", use_column_width=True)
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
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

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

# OTP storage
otp_storage = {}

# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

# Function to send email
def send_email(recipient_email, otp):
    sender_email = "gatherhubiitmandi@gmail.com"  # Replace with your email
    sender_password = os.getenv("EMAIL_PASSWORD")  # Replace with your email password

    subject = "Your OTP for Business Card Submission"
    body = f"Your OTP is {otp}. It is valid for 5 minutes."

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Resend OTP logic
resend_cooldown = 60  # Cooldown in seconds

# Check last sent time
last_sent_time = otp_storage.get(email, {}).get("last_sent", None)
time_remaining = None

if last_sent_time:
    time_remaining = max(0, resend_cooldown - (datetime.now() - last_sent_time).total_seconds())

# OTP Request
if st.button("Send OTP"):
    if not email:
        st.error("Please enter your email address.")
    elif time_remaining and time_remaining > 0:
        st.error(f"Please wait {int(time_remaining)} seconds before resending the OTP.")
    else:
        otp = generate_otp()
        expiration = datetime.now() + timedelta(minutes=5)  # OTP valid for 5 minutes
        otp_storage[email] = {"otp": otp, "expires": expiration, "last_sent": datetime.now()}

        if send_email(email, otp):
            st.success("OTP has been sent to your email. Please check your inbox.")
        else:
            st.error("Failed to send OTP. Please try again.")

# Verify OTP
user_otp = st.text_input("Enter OTP", placeholder="Enter the OTP sent to your email")

if st.button("Verify OTP"):
    if email in otp_storage:
        stored_otp = otp_storage[email]['otp']
        expiration = otp_storage[email]['expires']

        if datetime.now() > expiration:
            st.error("OTP has expired. Please request a new one.")
        elif user_otp == stored_otp:
            st.success("OTP verified successfully! You can now submit your business card.")
            del otp_storage[email]  # Remove OTP after successful verification
        else:
            st.error("Invalid OTP. Please try again.")
    else:
        st.error("No OTP found for this email. Please request a new one.")

# Submission URL
submit_url = "https://gatherhub-r7yr.onrender.com/user/businessCard/posting"

# Submit business card information
if st.button("Submit"):
    if not name or not email or not mobile:
        st.error("Please fill in all required fields (Name, Email, and Mobile).")
    elif email not in otp_storage:
        st.error("Please verify your email using the OTP.")
    else:
        try:
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
            }

            # Send POST request
            response = requests.post(submit_url, json=payload)
            if response.status_code == 201:
                response_json = response.json()
                id = response_json.get("_id")
                st.success("🎉 Your information has been submitted successfully!")
                
                # Generate the QR code
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
                # st.error(f"Failed to submit. Server responded with status: {response.status_code}")
                st.error(f"{response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
