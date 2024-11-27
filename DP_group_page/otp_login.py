# import streamlit as st
# import requests
# import qrcode
# from io import BytesIO
# from PIL import Image
# import random
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime, timedelta
# import os

# # Page configuration
# st.set_page_config(
#     page_title="Digital Business Card Creator",
#     page_icon="💼",
#     layout="centered"
# )

# # Custom CSS for theme-aware styling
# st.markdown("""
#     <style>
#     .main {
#         padding: 2rem;
#     }
#     .stButton button {
#         width: 100%;
#         border-radius: 5px;
#         height: 3em;
#     }
#     .stTextInput > div > div > input,
#     .stTextArea > div > div > textarea {
#         border-radius: 5px;
#     }
#     /* Theme-aware custom containers */
#     .custom-container {
#         padding: 1rem;
#         border-radius: 5px;
#         margin-bottom: 2rem;
#         background-color: var(--background-color);
#         border: 1px solid var(--border-color);
#     }
#     /* Dark mode */
#     [data-theme="dark"] {
#         --background-color: #2e2e2e;
#         --border-color: #404040;
#         --text-color: #ffffff;
#     }
#     /* Light mode */
#     [data-theme="light"] {
#         --background-color: #f0f2f6;
#         --border-color: #e0e0e0;
#         --text-color: #31333F;
#     }
#     /* Verification status indicators */
#     .verification-pending {
#         color: #ffa500;
#         padding: 0.2rem 0.5rem;
#         border-radius: 3px;
#         font-size: 0.9em;
#     }
#     .verification-success {
#         color: #00cc00;
#         padding: 0.2rem 0.5rem;
#         border-radius: 3px;
#         font-size: 0.9em;
#     }
#     /* Section headers */
#     .section-header {
#         color: var(--text-color);
#         padding: 0.5rem 0;
#         margin: 1rem 0;
#         border-bottom: 2px solid var(--border-color);
#     }
#     /* Input labels */
#     .input-label {
#         color: var(--text-color);
#         font-weight: 500;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize session state for OTP management
# if 'otp_storage' not in st.session_state:
#     st.session_state.otp_storage = {}

# def generate_otp():
#     """Generate a 6-digit OTP"""
#     return random.randint(100000, 999999)
# def send_email(recipient_email, otp):
#     """Send OTP via email with improved error handling"""
#     try:
#         # sender_email = os.getenv("EMAIL")
#         sender_email = "b23277@students.iitmandi.ac.in"
#         # sender_password = os.getenv("EMAIL_PASSWORD")
#         sender_password = "xeqz fkph iypn ondb"
        
#         # Validate environment variables
#         if not sender_email or not sender_password:
#             st.error("Email configuration is missing. Please set EMAIL and EMAIL_PASSWORD environment variables.")
#             return False
        
#         message = MIMEMultipart()
#         message['From'] = sender_email
#         message['To'] = recipient_email
#         message['Subject'] = "Your Digital Business Card OTP"
        
#         body = f"""
#         Hello!
        
#         Your OTP for Digital Business Card submission is: {otp}
        
#         This OTP is valid for 5 minutes.
        
#         Best regards,
#         Digital Business Card Team
#         """
        
#         message.attach(MIMEText(body, 'plain'))
        
#         # More verbose SMTP connection with explicit error handling
#         try:
#             with smtplib.SMTP('smtp.gmail.com', 587) as server:
#                 server.set_debuglevel(1)  # Enable debug output
#                 server.starttls()
#                 server.login(sender_email, sender_password)
#                 server.sendmail(sender_email, recipient_email, message.as_string())
#                 st.info("Email sent successfully!")
#         except smtplib.SMTPAuthenticationError as auth_error:
#             st.error(f"SMTP Authentication Error: {auth_error}")
#             st.error("Please check your email and app password configuration.")
#             return False
#         except smtplib.SMTPException as smtp_error:
#             st.error(f"SMTP Error: {smtp_error}")
#             return False
        
#         return True
#     except Exception as e:
#         st.error(f"Unexpected error sending email: {e}")
#         return False

# # Header section with theme-aware container
# st.title("💼 Digital Business Card Creator")
# st.markdown("""
#     <div class="custom-container">
#     Create your professional digital business card in minutes. Fill in your details below, verify your email, 
#     and get a QR code to share your contact information instantly.
#     </div>
#     """, unsafe_allow_html=True)

# # Personal Information Section
# st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)

# col1, col2 = st.columns(2)

# with col1:
#     name = st.text_input("👤 Full Name", placeholder="John Doe")
#     email = st.text_input("📧 Email Address", placeholder="john@example.com")
#     mobile = st.text_input("📱 Mobile Number", placeholder="+1 (234) 567-8900")
#     designation = st.text_input("🎯 Designation", placeholder="Senior Developer")

# with col2:
#     organization = st.text_input("🏢 Organization", placeholder="Tech Corp")
#     location = st.text_input("📍 Location", placeholder="New York, USA")
#     linkedin = st.text_input("💼 LinkedIn URL", placeholder="linkedin.com/in/johndoe")

# about = st.text_area("📝 About Me", placeholder="Write a brief introduction about yourself and your professional journey...")

# # Email Verification Section
# st.markdown('<div class="section-header">Email Verification</div>', unsafe_allow_html=True)

# # Calculate time remaining for OTP resend
# can_resend = True
# time_remaining = 0

# if email in st.session_state.otp_storage and "last_sent" in st.session_state.otp_storage[email]:
#     elapsed = (datetime.now() - st.session_state.otp_storage[email]["last_sent"]).total_seconds()
#     time_remaining = max(0, 60 - elapsed)  # 60 seconds cooldown
#     can_resend = time_remaining <= 0

# # OTP verification layout
# otp_col1, otp_col2 = st.columns([2, 1])

# with otp_col1:
#     user_otp = st.text_input("🔐 Enter OTP", placeholder="Enter 6-digit OTP")

# with otp_col2:
#     if st.button("📤 Send OTP", disabled=not can_resend, type="secondary"):
#         if not email:
#             st.error("Please enter your email address.")
#         else:
#             otp = generate_otp()
#             if send_email(email, otp):
#                 st.session_state.otp_storage[email] = {
#                     "otp": otp,
#                     "expires": datetime.now() + timedelta(minutes=5),
#                     "last_sent": datetime.now(),
#                     "verified": False
#                 }
#                 st.success("OTP sent! Please check your email.")
#             else:
#                 st.error("Failed to send OTP. Please try again.")

#     if time_remaining > 0:
#         st.caption(f"⏳ Resend available in {int(time_remaining)}s")

# # Verify OTP status
# if email in st.session_state.otp_storage and st.session_state.otp_storage[email].get("verified"):
#     st.markdown('<p class="verification-success">✅ Email Verified</p>', unsafe_allow_html=True)
# else:
#     st.markdown('<p class="verification-pending">⏳ Verification Pending</p>', unsafe_allow_html=True)

# # Verify OTP button
# if st.button("✅ Verify OTP", type="secondary"):
#     if email not in st.session_state.otp_storage:
#         st.error("Please request an OTP first.")
#     elif datetime.now() > st.session_state.otp_storage[email]["expires"]:
#         st.error("OTP has expired. Please request a new one.")
#     elif user_otp == st.session_state.otp_storage[email]["otp"]:
#         st.session_state.otp_storage[email]["verified"] = True
#         st.success("✅ Email verified successfully!")
#     else:
#         st.error("Invalid OTP. Please try again.")

# # Submit section
# st.markdown('<div class="section-header">Create Business Card</div>', unsafe_allow_html=True)

# if st.button("🎉 Create Business Card", type="primary"):
#     if not all([name, email, mobile]):
#         st.error("Please fill in all required fields (Name, Email, and Mobile).")
#     elif email not in st.session_state.otp_storage or not st.session_state.otp_storage.get(email, {}).get("verified"):
#         st.error("Please verify your email before submitting.")
#     else:
#         try:
#             payload = {
#                 "name": name,
#                 "email": email,
#                 "mobile": mobile,
#                 "designation": designation,
#                 "organization": organization,
#                 "about": about,
#                 "linkedIn": linkedin,
#                 "location": location
#             }

#             response = requests.post(
#                 "https://gatherhub-r7yr.onrender.com/user/businessCard/posting",
#                 json=payload
#             )

#             if response.status_code == 201:
#                 response_json = response.json()
#                 id = response_json.get("_id")
                
#                 # Generate QR code
#                 qr = qrcode.QRCode(
#                     version=1,
#                     error_correction=qrcode.constants.ERROR_CORRECT_L,
#                     box_size=10,
#                     border=4,
#                 )
#                 qr.add_data(f"https://niweshvistingcard.streamlit.app/?userId={id}")
#                 qr.make(fit=True)

#                 # Create QR code with proper background color
#                 is_dark_mode = st.get_theme()['base'] == 'dark'
#                 qr_image = qr.make_image(
#                     fill="white" if is_dark_mode else "black",
#                     back_color="black" if is_dark_mode else "white"
#                 )
                
#                 buffer = BytesIO()
#                 qr_image.save(buffer, format="PNG")
#                 buffer.seek(0)

#                 # Success message and QR code display
#                 st.success("🎉 Business card created successfully!")
                
#                 # Display QR code with theme-aware container
#                 st.markdown("""
#                     <div class="custom-container" style="text-align: center;">
#                         <h3 style="color: var(--text-color);">Your Business Card QR Code</h3>
#                     </div>
#                     """, unsafe_allow_html=True)
                
#                 st.image(buffer, caption="Scan this QR code to view your digital business card", use_column_width=True)
                
#                 # Download button for QR code
#                 st.download_button(
#                     label="⬇️ Download QR Code",
#                     data=buffer,
#                     file_name="business_card_qr.png",
#                     mime="image/png"
#                 )
#             else:
#                 st.error(f"Submission failed: {response.text}")
#         except Exception as e:
#             st.error(f"An error occurred: {e}")

# # Footer with theme awareness
# st.markdown("""
#     <div class="custom-container" style="text-align: center; margin-top: 2rem;">
#         <p style="color: var(--text-color);">Made with ❤️ by the Digital Business Card Team</p>
#     </div>
#     """, unsafe_allow_html=True)
































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
import time
import os

# Page configuration
st.set_page_config(
    page_title="Digital Business Card Creator",
    page_icon="💼",
    layout="centered"
)

# Custom CSS for theme-aware styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 5px;
    }
    .custom-container {
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 2rem;
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
    }
    [data-theme="dark"] {
        --background-color: #2e2e2e;
        --border-color: #404040;
        --text-color: #ffffff;
    }
    [data-theme="light"] {
        --background-color: #f0f2f6;
        --border-color: #e0e0e0;
        --text-color: #31333F;
    }
    .verification-pending {
        color: #ffa500;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        font-size: 0.9em;
    }
    .verification-success {
        color: #00cc00;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        font-size: 0.9em;
    }
    .section-header {
        color: var(--text-color);
        padding: 0.5rem 0;
        margin: 1rem 0;
        border-bottom: 2px solid var(--border-color);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for OTP management
if 'otp_storage' not in st.session_state:
    st.session_state.otp_storage = {}

def generate_otp():
    """Generate a 6-digit OTP"""
    return random.randint(100000, 999999)

def send_email(recipient_email, otp):
    """Send OTP via email with improved error handling"""
    try:
        # sender_email = "your-email@gmail.com"  # Replace with your email
        # sender_password = "your-app-password"  # Replace with your app password
        # sender_email = os.getenv("EMAIL")
        sender_email = "b23277@students.iitmandi.ac.in"
        # sender_password = os.getenv("EMAIL_PASSWORD")
        sender_password = "xeqz fkph iypn ondb"
        
        
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = "Your Digital Business Card OTP"
        
        body = f"""
        Hello!
        
        Your OTP for Digital Business Card submission is: {otp}
        
        This OTP is valid for 5 minutes.
        
        Best regards,
        Digital Business Card Team
        """
        
        message.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Header section
st.title("💼 Digital Business Card Creator")
st.markdown("""
    <div class="custom-container">
    Create your professional digital business card in minutes. Fill in your details below, verify your email, 
    and get a QR code to share your contact information instantly.
    </div>
    """, unsafe_allow_html=True)

# Personal Information Section
st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Full Name", placeholder="John Doe")
    email = st.text_input("📧 Email Address", placeholder="john@example.com")
    mobile = st.text_input("📱 Mobile Number", placeholder="+1 (234) 567-8900")
    designation = st.text_input("🎯 Designation", placeholder="Senior Developer")

with col2:
    organization = st.text_input("🏢 Organization", placeholder="Tech Corp")
    location = st.text_input("📍 Location", placeholder="New York, USA")
    linkedin = st.text_input("💼 LinkedIn URL", placeholder="linkedin.com/in/johndoe")

about = st.text_area("📝 About Me", placeholder="Write a brief introduction about yourself and your professional journey...")

# Email Verification Section
st.markdown('<div class="section-header">Email Verification</div>', unsafe_allow_html=True)

# OTP Resend Timer
if email in st.session_state.otp_storage and "last_sent" in st.session_state.otp_storage[email]:
    elapsed = (datetime.now() - st.session_state.otp_storage[email]["last_sent"]).total_seconds()
    time_remaining = max(0, 30 - elapsed)  # 30 seconds cooldown
    can_resend = time_remaining <= 0
else:
    time_remaining = 0
    can_resend = True

if time_remaining > 0:
    st.info(f"⏳ You can resend the OTP in {int(time_remaining)} seconds.")
    time.sleep(1)
    st.rerun()

otp_col1, otp_col2 = st.columns([2, 1])

with otp_col1:
    user_otp = st.text_input("🔐 Enter OTP", placeholder="Enter 6-digit OTP")

with otp_col2:
    if st.button("📤 Send OTP", disabled=not can_resend, type="secondary"):
        if not email:
            st.error("Please enter your email address.")
        else:
            otp = generate_otp()
            if send_email(email, otp):
                st.session_state.otp_storage[email] = {
                    "otp": otp,
                    "expires": datetime.now() + timedelta(minutes=5),
                    "last_sent": datetime.now(),
                    "verified": False
                }
                st.success("OTP sent! Please check your email.")
            else:
                st.error("Failed to send OTP. Please try again.")

# Verify OTP status
if email in st.session_state.otp_storage and st.session_state.otp_storage[email].get("verified"):
    st.markdown('<p class="verification-success">✅ Email Verified</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="verification-pending">⏳ Verification Pending</p>', unsafe_allow_html=True)

if st.button("✅ Verify OTP", type="secondary"):
    if email not in st.session_state.otp_storage:
        st.error("Please request an OTP first.")
    elif datetime.now() > st.session_state.otp_storage[email]["expires"]:
        st.error("OTP has expired. Please request a new one.")
    elif user_otp == str(st.session_state.otp_storage[email]["otp"]):
        st.session_state.otp_storage[email]["verified"] = True
        st.success("✅ Email verified successfully!")
    else:
        st.error("Invalid OTP. Please try again.")


# Submit section
st.markdown('<div class="section-header">Create Business Card</div>', unsafe_allow_html=True)

if st.button("🎉 Create Business Card", type="primary"):
    if not all([name, email, mobile]):
        st.error("Please fill in all required fields (Name, Email, and Mobile).")
    elif email not in st.session_state.otp_storage or not st.session_state.otp_storage[email].get("verified"):
        st.error("Please verify your email before submitting.")
    else:
        try:
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

            response = requests.post(
                "https://gatherhub-r7yr.onrender.com/user/businessCard/posting",
                json=payload
            )

            if response.status_code == 201:
                response_json = response.json()
                id = response_json.get("_id")
                
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(f"https://niweshvistingcard.streamlit.app/?userId={id}")
                qr.make(fit=True)

                qr_image = qr.make_image(fill="black", back_color="white")
                
                buffer = BytesIO()
                qr_image.save(buffer, format="PNG")
                buffer.seek(0)

                st.success("🎉 Business card created successfully!")
                st.image(buffer, caption="Scan this QR code to view your digital business card", use_column_width=True)
                
                st.download_button(
                    label="⬇️ Download QR Code",
                    data=buffer,
                    file_name="business_card_qr.png",
                    mime="image/png"
                )
            else:
                st.error(f"Submission failed: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("""
    <div class="custom-container">
    <small>© 2024 Digital Business Card Creator. All rights reserved.</small>
    </div>
    """, unsafe_allow_html=True)
