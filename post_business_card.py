



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

# Function to send QR code email (moved to the top)
def send_qr_code_email(name, email, mobile, designation, organization, location, linkedin, about,conference_code):
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
    
    # Save QR Code to memory
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    
    # Send the email with the QR code
    subject = "Your Digital Business Card with QR Code"
    body = f"Dear {name},\n\nThank you for submitting your business card. Please find your QR code attached.\n\nBest regards,\nConference Team"
    
    msg = MIMEMultipart()
    sender_email = "gatherhubiitmandi@gmail.com"
    sender_password = "armf odpa unrp vkjz"
    msg['From'] = sender_email
    msg['To'] = email
    print("email: ", email)
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the QR code image
    image = MIMEImage(buf.read())
    msg.attach(image)
    
    try:
        # SMTP server configuration (for Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        st.success("✅ A QR Code has been sent to your email!")
    except Exception as e:
        st.error(f"❌ Error sending email: {e}")

# Load environment variables from a .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Digital Business Card Creator",
    page_icon="💼",
    layout="centered"
)

# Extract email and conference code from the URL
query_params = st.query_params
email = query_params.get('email', '')  # Default to an empty string if not provided
print("email: ", email)
conference_code = query_params.get('conference_code', 'DP2024')  # Default to 'DP2024'
print("conference_code: ", conference_code)
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

post_url = f"http://localhost:27017/user/conference/{conference_code}/eventCard/acceptedInvitation"  # Replace with the actual endpoint

if st.button("Submit"):
    if email:  # Ensure email is provided in the URL
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
            print()
            print("data: ", data)
            response = requests.post(post_url, json=data)
            st.write(f"Response status code: {response.status_code}")  # Log the status code
            st.write(f"Response content: {response.text}")  # Log the raw response content
            if response.status_code == 200:
                st.success("✅ Your information was successfully submitted!")
                send_qr_code_email(name, email, mobile, designation, organization, location, linkedin, about,conference_code)
            else:
                st.error(f"❌ Failed to submit. Status code: {response.status_code}")
                st.error(response.json())
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.error("❌ Email is missing. Please provide a valid email in the URL.")