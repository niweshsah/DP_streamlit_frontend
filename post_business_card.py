
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

load_dotenv()


rest_api_url =  'https://gatherhub-r7yr.onrender.com'

visiting_card_url = 'https://niweshvistingcard.streamlit.app'

# i am hardcodding for DP, please don't do anything
sender_email = 'b23277@students.iitmandi.ac.in'
sender_password = 'jmpi kksi mbss grgo'


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_qr_code_email(name, email, mobile, designation, organization, location, linkedin, about, conference_code):
    try:
        # Create QR Code Data
        qr_data = f"{visiting_card_url}/?email={email}&confcode={conference_code}"
        
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
        
        subject = "Your Personalized  QR Code"
        body = f"""Dear {name},

Thank you for submitting your business card. Please find your QR code attached.

Best regards,
GatherHub Team"""
        

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
    
    post_url = f"{rest_api_url}/user/conference/{conference_code}/eventCard/acceptedInvitation"
    
    
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

    st.title("💼 GatherHub Business Card Creator")
    st.markdown("Create your personalized QR code in minutes!")

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
                        st.error(f"❌ Submission failed. Error: {response.text}")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                logger.error(f"Submission error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()