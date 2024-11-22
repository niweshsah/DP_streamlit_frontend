



# import streamlit as st
# import requests
# import qrcode
# from io import BytesIO
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from dotenv import load_dotenv
# import os

# # Function to send QR code email (moved to the top)
# def send_qr_code_email(name, email, mobile, designation, organization, location, linkedin, about,conference_code):
#     # Create QR Code Data
#     qr_data = f"https://niweshvistingcard.streamlit.app/?email={email}&confcode={conference_code}"  
    
#     # Generate QR Code
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(qr_data.strip())
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")
    
#     # Save QR Code to memory
#     buf = BytesIO()
#     img.save(buf)
#     buf.seek(0)
    
#     # Send the email with the QR code
#     subject = "Your Digital Business Card with QR Code"
#     body = f"Dear {name},\n\nThank you for submitting your business card. Please find your QR code attached.\n\nBest regards,\nConference Team"
    
#     msg = MIMEMultipart()
#     sender_email = "gatherhubiitmandi@gmail.com"
#     sender_password = "armf odpa unrp vkjz"
#     msg['From'] = sender_email
#     msg['To'] = email
#     print("email: ", email)
#     msg['Subject'] = subject
    
#     msg.attach(MIMEText(body, 'plain'))
    
#     # Attach the QR code image
#     image = MIMEImage(buf.read())
#     msg.attach(image)
    
#     try:
#         # SMTP server configuration (for Gmail)
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(msg['From'], msg['To'], msg.as_string())
#         server.quit()
#         st.success("✅ A QR Code has been sent to your email!")
#     except Exception as e:
#         st.error(f"❌ Error sending email: {e}")

# # Load environment variables from a .env file
# load_dotenv()

# # Page configuration
# st.set_page_config(
#     page_title="Digital Business Card Creator",
#     page_icon="💼",
#     layout="centered"
# )

# # Extract email and conference code from the URL
# query_params = st.query_params
# email = query_params.get('email', '')  # Default to an empty string if not provided
# print("email: ", email)
# conference_code = query_params.get('conference_code', 'DP2024')  # Default to 'DP2024'
# print("conference_code: ", conference_code)
# # Header section
# st.title("💼 Digital Business Card Creator")
# st.markdown("""
#     <div class="custom-container">
#     Create your professional digital business card in minutes. Fill in your details below and submit your business card for the conference.
#     </div>
# """, unsafe_allow_html=True)

# # Personal Information Section
# st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)

# col1, col2 = st.columns(2)

# with col1:
#     name = st.text_input("👤 Full Name", placeholder="John Doe")
#     mobile = st.text_input("📱 Mobile Number", placeholder="+1 (234) 567-8900")
#     designation = st.text_input("🎯 Designation", placeholder="Senior Developer")

# with col2:
#     organization = st.text_input("🏢 Organization", placeholder="Tech Corp")
#     location = st.text_input("📍 Location", placeholder="New York, USA")
#     linkedin = st.text_input("💼 LinkedIn URL", placeholder="linkedin.com/in/johndoe")

# about = st.text_area("📝 About Me", placeholder="Write a brief introduction about yourself and your professional journey...")

# # Form Submission Section
# st.markdown('<div class="section-header">Submit Your Business Card</div>', unsafe_allow_html=True)

# post_url = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/acceptedInvitation"  # Replace with the actual endpoint

# if st.button("Submit"):
#     if email:  # Ensure email is provided in the URL
#         data = {
#             "name": name,
#             "email": email,
#             "mobile": mobile,
#             "designation": designation,
#             "organization": organization,
#             "location": location,
#             "linkedIn": linkedin,
#             "about": about,
#         }
#         try:
#             print()
#             print("data: ", data)
#             st.write("email: ", email)
#             st.write("conference code: ", conference_code)
#             response = requests.post(post_url, json=data)
#             st.write(f"Response status code: {response.status_code}")  # Log the status code
#             st.write(f"Response content: {response.text}")  # Log the raw response content
#             if response.status_code == 200:
#                 st.success("✅ Your information was successfully submitted!")
#                 send_qr_code_email(name, email, mobile, designation, organization, location, linkedin, about,conference_code)
#             else:
#                 st.error(f"❌ Failed to submit. Status code: {response.status_code}")
#                 st.error(response.json())
#         except Exception as e:
#             st.error(f"❌ Error: {e}")
#     else:
#         st.error("❌ Email is missing. Please provide a valid email in the URL.")



































































# import streamlit as st
# import requests
# import qrcode
# from io import BytesIO
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from dotenv import load_dotenv
# import os
# import json
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def send_qr_code_email(name, email, mobile, designation, organization, location, linkedin, about, conference_code):
#     try:
#         # Create QR Code Data
#         qr_data = f"https://niweshvistingcard.streamlit.app/?email={email}&confcode={conference_code}"
        
#         # Generate QR Code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(qr_data.strip())
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
        
#         # Save QR Code to memory
#         buf = BytesIO()
#         img.save(buf)
#         buf.seek(0)
        
#         # Email configuration
#         sender_email = "gatherhubiitmandi@gmail.com"
#         sender_password = "armf odpa unrp vkjz"
#         subject = "Your Digital Business Card with QR Code"
#         body = f"""Dear {name},

# Thank you for submitting your business card. Please find your QR code attached.

# Best regards,
# Conference Team"""
        
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))
        
#         # Attach QR code
#         image = MIMEImage(buf.read())
#         msg.attach(image)
        
#         # Send email
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.send_message(msg)
            
#         return True, "QR Code has been sent to your email!"
#     except Exception as e:
#         logger.error(f"Email sending failed: {str(e)}")
#         return False, f"Failed to send email: {str(e)}"

# def validate_input_fields(data):
#     required_fields = ['name', 'email', 'mobile', 'designation', 'organization']
#     missing_fields = [field for field in required_fields if not data.get(field)]
    
#     if missing_fields:
#         return False, f"Please fill in the following required fields: {', '.join(missing_fields)}"
#     return True, "Validation successful"

# def submit_data(data, conference_code):
#     post_url = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/acceptedInvitation"
    
#     try:
#         # Log the request data
#         logger.info(f"Submitting data to {post_url}")
#         logger.info(f"Request payload: {json.dumps(data, indent=2)}")
        
#         response = requests.post(post_url, json=data, timeout=10)
        
#         # Log the response
#         logger.info(f"Response status code: {response.status_code}")
#         logger.info(f"Response content: {response.text}")
        
#         return response
#     except requests.exceptions.Timeout:
#         raise Exception("Request timed out. Please try again.")
#     except requests.exceptions.RequestException as e:
#         raise Exception(f"Network error: {str(e)}")
#     except Exception as e:
#         raise Exception(f"Unexpected error: {str(e)}")

# # Main app
# def main():
#     st.set_page_config(
#         page_title="Digital Business Card Creator",
#         page_icon="💼",
#         layout="centered"
#     )

#     st.title("💼 Digital Business Card Creator")
#     st.markdown("""
#         Create your professional digital business card in minutes. 
#         Fill in your details below and submit your business card for the conference.
#     """)

#     # Get URL parameters
#     query_params = st.query_params
#     email = query_params.get('email', '')
#     conference_code = query_params.get('conference_code', 'DP2024')

#     # Display debug information in development
#     if st.secrets.get('ENVIRONMENT') == 'development':
#         st.sidebar.write("Debug Information:")
#         st.sidebar.write(f"Email from URL: {email}")
#         st.sidebar.write(f"Conference Code: {conference_code}")

#     # Form inputs
#     with st.form("business_card_form"):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             name = st.text_input("👤 Full Name*", placeholder="John Doe")
#             mobile = st.text_input("📱 Mobile Number*", placeholder="+1 (234) 567-8900")
#             designation = st.text_input("🎯 Designation*", placeholder="Senior Developer")
        
#         with col2:
#             organization = st.text_input("🏢 Organization*", placeholder="Tech Corp")
#             location = st.text_input("📍 Location", placeholder="New York, USA")
#             linkedin = st.text_input("💼 LinkedIn URL", placeholder="linkedin.com/in/johndoe")
        
#         about = st.text_area("📝 About Me", placeholder="Write a brief introduction about yourself...")
        
#         submit_button = st.form_submit_button("Submit")

#         if submit_button:
#             if not email:
#                 st.error("❌ Email is missing. Please provide a valid email in the URL.")
#                 return

#             # Prepare data
#             data = {
#                 "name": name,
#                 "email": email,
#                 "mobile": mobile,
#                 "designation": designation,
#                 "organization": organization,
#                 "location": location,
#                 "linkedIn": linkedin,
#                 "about": about,
#             }

#             # Validate input
#             is_valid, validation_message = validate_input_fields(data)
#             if not is_valid:
#                 st.error(validation_message)
#                 return

#             try:
#                 with st.spinner("Submitting your information..."):
#                     # Submit data
#                     response = submit_data(data, conference_code)
                    
#                     if response.status_code == 200:
#                         st.success("✅ Information submitted successfully!")
                        
#                         # Send QR code email
#                         with st.spinner("Sending QR code to your email..."):
#                             success, message = send_qr_code_email(
#                                 name, email, mobile, designation, 
#                                 organization, location, linkedin, 
#                                 about, conference_code
#                             )
#                             if success:
#                                 st.success(message)
#                             else:
#                                 st.warning(message)
#                     else:
#                         st.error(f"❌ Submission failed: {response.text}")
                        
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")
#                 logger.error(f"Submission error: {str(e)}", exc_info=True)

# if __name__ == "__main__":
#     main()



















































import streamlit as st
import requests
import qrcode
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_qr_code_email(name, email, mobile, designation, organization, location, linkedin, about, conference_code):
    try:
        # Create QR Code Data
        qr_data = f"https://niweshvistingcard.streamlit.app/?email={email}&confcode={conference_code}"
        
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data.strip())
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf)
        buf.seek(0)
        
        sender_email = "gatherhubiitmandi@gmail.com"
        sender_password = "armf odpa unrp vkjz"
        subject = "Your Digital Business Card with QR Code"
        body = f"""Dear {name},

Thank you for submitting your business card. Please find your QR code attached.

Best regards,
Conference Team"""
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        image = MIMEImage(buf.read())
        msg.attach(image)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        return True, "QR Code has been sent to your email!"
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")
        return False, f"Failed to send email: {str(e)}"

def submit_data(data, conference_code):
    post_url = f"https://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/acceptedInvitation"
    
    try:
        logger.info(f"Submitting data to {post_url}")
        logger.info(f"Request payload: {json.dumps(data, indent=2)}")
        
        # Add headers and increase timeout
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(
            post_url, 
            json=data, 
            headers=headers,
            timeout=15
        )
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.text}")
        
        return response
    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

# Main app
def main():
    st.set_page_config(
        page_title="Digital Business Card Creator",
        page_icon="💼",
        layout="wide",  # Changed to wide layout for better mobile display
        initial_sidebar_state="collapsed"  # Hide sidebar on mobile
    )

    # Custom CSS for mobile optimization
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .stTextInput>div>div>input {
            padding: 15px 10px;
        }
        @media (max-width: 640px) {
            .main .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("💼 Digital Business Card Creator")
    st.markdown("Create your professional digital business card in minutes.")

    # Get URL parameters
    email = st.query_params.get('email', '')
    conference_code = st.query_params.get('conference_code', 'DP2024')

    # Show debug info in development
    if st.secrets.get('ENVIRONMENT') == 'development':
        st.sidebar.write(f"Email from URL: {email}")
        st.sidebar.write(f"Conference Code: {conference_code}")

    # Form inputs - Single column layout for mobile
    with st.form("business_card_form", clear_on_submit=False):
        name = st.text_input("👤 Full Name*", key="name")
        mobile = st.text_input("📱 Mobile Number*", key="mobile")
        designation = st.text_input("🎯 Designation*", key="designation")
        organization = st.text_input("🏢 Organization*", key="organization")
        location = st.text_input("📍 Location", key="location")
        linkedin = st.text_input("💼 LinkedIn URL", key="linkedin")
        about = st.text_area("📝 About Me", key="about", height=100)
        
        # Large, mobile-friendly submit button
        submit_button = st.form_submit_button("Submit Business Card", use_container_width=True)

        if submit_button:
            if not email:
                st.error("❌ Email is missing from the URL. Please use the correct link.")
                return

            # Validate required fields
            required_fields = {
                'Name': name,
                'Mobile': mobile,
                'Designation': designation,
                'Organization': organization
            }
            
            missing_fields = [field for field, value in required_fields.items() if not value.strip()]
            
            if missing_fields:
                st.error(f"❌ Please fill in these required fields: {', '.join(missing_fields)}")
                return

            # Prepare data
            data = {
                "name": name,
                "email": email,
                "mobile": mobile,
                "designation": designation,
                "organization": organization,
                "location": location,
                "linkedIn": linkedin,
                "about": about,
            }

            try:
                with st.spinner("📤 Submitting your information..."):
                    response = submit_data(data, conference_code)
                    
                    if response.status_code == 200:
                        st.success("✅ Information submitted successfully!")
                        
                        with st.spinner("📧 Sending QR code to your email..."):
                            success, message = send_qr_code_email(
                                name, email, mobile, designation, 
                                organization, location, linkedin, 
                                about, conference_code
                            )
                            if success:
                                st.success(message)
                                # Clear form or show next steps
                                st.balloons()
                            else:
                                st.warning(message)
                    else:
                        st.error(f"❌ Submission failed. Please try again. Error: {response.text}")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                logger.error(f"Submission error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()