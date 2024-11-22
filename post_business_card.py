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
# import time  # Import for delay in the timer

# # Page configuration
# st.set_page_config(
#     page_title="Digital Business Card Creator",
#     page_icon="💼",
#     layout="centered"
# )

# # Custom CSS for styling with adaptive theme
# st.markdown("""
#     <style>
#     :root {
#         --primary-color: #7C3AED;
#         --primary-hover: #6D28D9;
#         --background-primary: #ffffff;
#         --background-secondary: #f3f4f6;
#         --border-color: #e5e7eb;
#         --text-primary: #1F2937;
#         --text-secondary: #4B5563;
#         --success-color: #059669;
#         --warning-color: #D97706;
#         --error-color: #DC2626;
#     }

#     /* Dark mode overrides */
#     @media (prefers-color-scheme: dark) {
#         :root {
#             --background-primary: #1F2937;
#             --background-secondary: #374151;
#             --border-color: #4B5563;
#             --text-primary: #F3F4F6;
#             --text-secondary: #D1D5DB;
#         }
#     }

#     .main {
#         padding: 2rem;
#         background-color: var(--background-primary);
#         color: var(--text-primary);
#     }

#     .custom-container {
#         padding: 1.5rem;
#         border-radius: 8px;
#         margin-bottom: 2rem;
#         background-color: var(--background-secondary);
#         border: 1px solid var(--border-color);
#         box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
#     }

#     .stButton button {
#         width: 100%;
#         border-radius: 8px;
#         height: 3em;
#         background-color: var(--primary-color);
#         color: white;
#         font-weight: 500;
#         transition: all 0.2s ease;
#     }

#     .stButton button:hover {
#         background-color: var(--primary-hover);
#         transform: translateY(-1px);
#     }

#     .stTextInput > div > div > input,
#     .stTextArea > div > div > textarea {
#         border-radius: 8px;
#         border: 1px solid var(--border-color);
#         background-color: var(--background-primary);
#         color: var(--text-primary);
#     }

#     .stTextInput > div > div > input:focus,
#     .stTextArea > div > div > textarea:focus {
#         border-color: var(--primary-color);
#         box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
#     }

#     .verification-pending {
#         color: var(--warning-color);
#         padding: 0.5rem 1rem;
#         border-radius: 6px;
#         font-size: 0.9em;
#         background-color: rgba(217, 119, 6, 0.1);
#         display: inline-block;
#     }

#     .verification-success {
#         color: var(--success-color);
#         padding: 0.5rem 1rem;
#         border-radius: 6px;
#         font-size: 0.9em;
#         background-color: rgba(5, 150, 105, 0.1);
#         display: inline-block;
#     }

#     .section-header {
#         color: var(--text-primary);
#         padding: 1rem 0;
#         margin: 1.5rem 0;
#         border-bottom: 2px solid var(--border-color);
#         font-size: 1.25rem;
#         font-weight: 600;
#     }

#     .stDownloadButton button {
#         background-color: var(--background-secondary);
#         color: var(--text-primary);
#         border: 1px solid var(--border-color);
#     }

#     .stDownloadButton button:hover {
#         background-color: var(--primary-color);
#         color: white;
#     }

#     .qr-container {
#         background-color: var(--background-secondary);
#         padding: 2rem;
#         border-radius: 8px;
#         text-align: center;
#         margin: 2rem 0;
#     }

#     .otp-container {
#         display: flex;
#         align-items: center;
#         gap: 1rem;
#         margin-bottom: 1rem;
#     }

#     .timer {
#         color: var(--warning-color);
#         font-size: 0.9em;
#         white-space: nowrap;
#         padding: 0.5rem 1rem;
#         background-color: rgba(217, 119, 6, 0.1);
#         border-radius: 6px;
#         height: 38px;
#         display: flex;
#         align-items: center;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Initialize session state for OTP management
# if 'otp_storage' not in st.session_state:
#     st.session_state.otp_storage = {}

# def generate_otp():
#     """Generate a 6-digit OTP"""
#     return str(random.randint(100000, 999999))

# def send_email(recipient_email, otp):
#     """Send OTP via email"""
#     try:
#         sender_email = "gatherhubiitmandi@gmail.com"
#         sender_password = "armf odpa unrp vkjz"  # Use environment variables in production
        
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
        
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, recipient_email, message.as_string())
#         return True
#     except Exception as e:
#         st.error(f"Error sending email: {e}")
#         return False

# # Header section
# st.title("💼 Digital Business Card Creator")
# st.markdown("""
#     <div class="custom-container" style="color: var(--text-color);">
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

# # Timer placeholder
# timer_placeholder = st.empty()

# if email in st.session_state.otp_storage and "last_sent" in st.session_state.otp_storage[email]:
#     elapsed = (datetime.now() - st.session_state.otp_storage[email]["last_sent"]).total_seconds()
#     time_remaining = max(0, 60 - elapsed)
# else:
#     time_remaining = 0

# can_resend = time_remaining <= 0

# if not can_resend:
#     # Countdown timer
#     with timer_placeholder.container():
#         while time_remaining > 0:
#             timer_placeholder.markdown(
#                 f'<div class="timer">⏳ Resend in {int(time_remaining)}s</div>',
#                 unsafe_allow_html=True
#             )
#             time_remaining -= 1
#             time.sleep(1)
#         timer_placeholder.empty()

# col1, col2 = st.columns([2, 1])

# with col1:
#     otp_input = st.text_input("🔒 Enter OTP", placeholder="Enter 6-digit OTP", max_chars=6)

# with col2:
#     if can_resend:
#         if st.button("📤 Send OTP", type="secondary"):
#             if not email:
#                 st.error("Please enter your email address.")
#             else:
#                 otp = generate_otp()
#                 if send_email(email, otp):
#                     st.session_state.otp_storage[email] = {
#                         "otp": otp,
#                         "expires": datetime.now() + timedelta(minutes=5),
#                         "last_sent": datetime.now(),
#                         "verified": False
#                     }
#                     st.success("OTP sent! Please check your email.")
#                     timer_placeholder.empty()
#     else:
#         st.write("")  # Ensure alignment if no timer is shown

# if otp_input:
#     if email in st.session_state.otp_storage:
#         stored_data = st.session_state.otp_storage[email]
#         if otp_input == stored_data["otp"]:
#             if datetime.now() <= stored_data["expires"]:
#                 st.session_state.otp_storage[email]["verified"] = True
#                 st.success("✅ Email verified successfully!")
#             else:
#                 st.error("❌ OTP expired. Please request a new one.")
#         else:
#             st.error("❌ Invalid OTP. Please try again.")
#     else:
#         st.error("❌ No OTP sent to this email. Please send OTP first.")

# # QR Code Generation
# st.markdown('<div class="section-header">QR Code</div>', unsafe_allow_html=True)

# if st.button("Generate QR Code"):
#     if email in st.session_state.otp_storage and st.session_state.otp_storage[email].get("verified"):
#         qr_data = f"""
#         Name: {name}
#         Email: {email}
#         Mobile: {mobile}
#         Designation: {designation}
#         Organization: {organization}
#         Location: {location}
#         LinkedIn: {linkedin}
#         About: {about}
#         """
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(qr_data.strip())
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")

#         buf = BytesIO()
#         img.save(buf)
#         buf.seek(0)
#         st.image(img, caption="Scan this QR Code", use_column_width=True)
#         st.download_button(
#             "📥 Download QR Code",
#             buf,
#             file_name="business_card_qr.png",
#             mime="image/png"
#         )
#     else:
#         st.error("❌ Please verify your email to generate a QR code.")




























































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
# import time

# # Page configuration
# st.set_page_config(
#     page_title="Digital Business Card Creator",
#     page_icon="💼",
#     layout="centered"
# )

# # Custom CSS for styling
# st.markdown("""
#     <style>
#     :root {
#         --primary-color: #7C3AED;
#         --primary-hover: #6D28D9;
#         --background-primary: #ffffff;
#         --background-secondary: #f3f4f6;
#         --border-color: #e5e7eb;
#         --text-primary: #1F2937;
#         --text-secondary: #4B5563;
#         --success-color: #059669;
#         --warning-color: #D97706;
#         --error-color: #DC2626;
#     }

#     /* Dark mode overrides */
#     @media (prefers-color-scheme: dark) {
#         :root {
#             --background-primary: #1F2937;
#             --background-secondary: #374151;
#             --border-color: #4B5563;
#             --text-primary: #F3F4F6;
#             --text-secondary: #D1D5DB;
#         }
#     }

#     .main {
#         padding: 2rem;
#         background-color: var(--background-primary);
#         color: var(--text-primary);
#     }

#     .custom-container {
#         padding: 1.5rem;
#         border-radius: 8px;
#         margin-bottom: 2rem;
#         background-color: var(--background-secondary);
#         border: 1px solid var(--border-color);
#         box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
#     }

#     .stButton button {
#         width: 100%;
#         border-radius: 8px;
#         height: 3em;
#         background-color: var(--primary-color);
#         color: white;
#         font-weight: 500;
#         transition: all 0.2s ease;
#     }

#     .stButton button:hover {
#         background-color: var(--primary-hover);
#         transform: translateY(-1px);
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Initialize session state for OTP management
# if 'otp_storage' not in st.session_state:
#     st.session_state.otp_storage = {}

# def generate_otp():
#     """Generate a 6-digit OTP"""
#     return str(random.randint(100000, 999999))

# def send_email(recipient_email, otp):
#     """Send OTP via email"""
#     try:
#         sender_email = "gatherhubiitmandi@gmail.com"
#         sender_password = "armf odpa unrp vkjz"  # Use environment variables in production
        
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
        
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, recipient_email, message.as_string())
#         return True
#     except Exception as e:
#         st.error(f"Error sending email: {e}")
#         return False

# # Header section
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

# col1, col2 = st.columns([2, 1])

# otp_input = col1.text_input("🔒 Enter OTP", placeholder="Enter 6-digit OTP", max_chars=6)

# if col2.button("📤 Send OTP"):
#     if not email:
#         st.error("Please enter your email address.")
#     else:
#         otp = generate_otp()
#         if send_email(email, otp):
#             st.session_state.otp_storage[email] = {
#                 "otp": otp,
#                 "expires": datetime.now() + timedelta(minutes=5),
#                 "verified": False
#             }
#             st.success("OTP sent! Please check your email.")

# if otp_input:
#     if email in st.session_state.otp_storage:
#         stored_data = st.session_state.otp_storage[email]
#         if otp_input == stored_data["otp"]:
#             if datetime.now() <= stored_data["expires"]:
#                 st.session_state.otp_storage[email]["verified"] = True
#                 st.success("✅ Email verified successfully!")
#             else:
#                 st.error("❌ OTP expired. Please request a new one.")
#         else:
#             st.error("❌ Invalid OTP. Please try again.")
#     else:
#         st.error("❌ No OTP sent to this email. Please send OTP first.")

# # QR Code Generation
# st.markdown('<div class="section-header">QR Code</div>', unsafe_allow_html=True)

# if st.button("Generate QR Code"):
#     if email in st.session_state.otp_storage and st.session_state.otp_storage[email].get("verified"):
#         qr_data = f"""
#         Name: {name}
#         Email: {email}
#         Mobile: {mobile}
#         Designation: {designation}
#         Organization: {organization}
#         Location: {location}
#         LinkedIn: {linkedin}
#         About: {about}
#         """
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(qr_data.strip())
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")

#         buf = BytesIO()
#         img.save(buf)
#         buf.seek(0)
#         st.image(img, caption="Scan this QR Code", use_column_width=True)
#         st.download_button(
#             "📥 Download QR Code",
#             buf,
#             file_name="business_card_qr.png",
#             mime="image/png"
#         )
#     else:
#         st.error("❌ Please verify your email to generate a QR code.")

# # Form Submission Section
# st.markdown('<div class="section-header">Submit Your Business Card</div>', unsafe_allow_html=True)

# query_params = st.get_query_params()

# # Get the 'conference_code' parameter from the query string
# conference_code = query_params.get('conference_code', ['DP2024'])[0]  # Default to an empty string if not provided


# post_url = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/sendInvitation"  # Replace with the actual endpoint



# if st.button("Submit"):
#     if email in st.session_state.otp_storage and st.session_state.otp_storage[email].get("verified"):
#         data = {
#             "name": name,
#             "email": email,
#             "mobile": mobile,
#             "designation": designation,
#             "organization": organization,
#             "location": location,
#             "linkedin": linkedin,
#             "about": about,
#         }
#         try:
#             response = requests.post(post_url, json=data)
#             if response.status_code == 200:
#                 st.success("✅ Your information was successfully submitted!")
#             else:
#                 st.error(f"❌ Failed to submit. Status code: {response.status_code}")
#         except Exception as e:
#             st.error(f"❌ Error: {e}")
#     else:
#         st.error("❌ Please verify your email before submitting.")





















































import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Digital Business Card Creator",
    page_icon="💼",
    layout="centered"
)

# Extract email and conference code from the URL
query_params = st.get_query_params()

# Get the 'email' and 'conference_code' parameters from the query string
email = query_params.get('email', [''])[0]  # Default to an empty string if not provided
conference_code = query_params.get('conference_code', ['DP2024'])[0]  # Default to 'DP2024'

# Header section
st.title("💼 Digital Business Card Creator")
st.markdown("""
    <div class="custom-container">
    Create your professional digital business card in minutes. Fill in your details below and submit your business card for the conference.
    </div>
""", unsafe_allow_html=True)

# Personal Information Section
st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Full Name", placeholder="John Doe")
    mobile = st.text_input("📱 Mobile Number", placeholder="+1 (234) 567-8900")
    designation = st.text_input("🎯 Designation", placeholder="Senior Developer")

with col2:
    organization = st.text_input("🏢 Organization", placeholder="Tech Corp")
    location = st.text_input("📍 Location", placeholder="New York, USA")
    linkedin = st.text_input("💼 LinkedIn URL", placeholder="linkedin.com/in/johndoe")

about = st.text_area("📝 About Me", placeholder="Write a brief introduction about yourself and your professional journey...")

# Form Submission Section
st.markdown('<div class="section-header">Submit Your Business Card</div>', unsafe_allow_html=True)

post_url = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/sendInvitation"  # Replace with the actual endpoint

if st.button("Submit"):
    if email:  # Ensure email is provided in the URL
        data = {
            "name": name,
            "email": email,
            "mobile": mobile,
            "designation": designation,
            "organization": organization,
            "location": location,
            "linkedin": linkedin,
            "about": about,
        }
        try:
            response = requests.post(post_url, json=data)
            if response.status_code == 200:
                st.success("✅ Your information was successfully submitted!")
            else:
                st.error(f"❌ Failed to submit. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.error("❌ Email is missing. Please provide a valid email in the URL.")
