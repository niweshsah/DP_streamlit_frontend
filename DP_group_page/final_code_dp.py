 
    
    
import streamlit as st
import requests
import base64
import random
import time
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO
from datetime import datetime, timedelta
import re

# Backend Base URL
BASE_URL = "http://gatherhub-r7yr.onrender.com/user/conference/DP2024"

class GroupSubmissionApp:
    def __init__(self):
        # Initialize session state
        if 'otp_storage' not in st.session_state:
            st.session_state.otp_storage = {}
        if 'submission_completed' not in st.session_state:
            st.session_state.submission_completed = False

    def apply_custom_css(self):
        """Apply custom CSS to enhance the app's appearance with dark and light mode support"""
        st.markdown("""
        <style>
        /* Dark and Light Mode Color Variables */
        :root {
            /* Light Mode Colors */
            --bg-primary: #f0f2f6;
            --bg-secondary: #ffffff;
            --text-primary: #2c3e50;
            --text-secondary: #7f8c8d;
            --input-border: #a1c5e8;
            --input-focus: #3498db;
            --button-primary: #3498db;
            --button-hover: #2980b9;
            --success-bg: #e6f3e6;
            --error-bg: #f9e6e6;
            --warning-bg: #fff4e6;
        }

        /* Dark Mode Color Overrides */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-primary: #121212;
                --bg-secondary: #1e1e1e;
                --text-primary: #e0e0e0;
                --text-secondary: #a0a0a0;
                --input-border: #4a4a4a;
                --input-focus: #5294e0;
                --button-primary: #5294e0;
                --button-hover: #6aa0e5;
                --success-bg: #2c3e2c;
                --error-bg: #3e2c2c;
                --warning-bg: #3e352c;
            }
        }

        /* Base App Styling */
        .stApp {
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }

        /* Header Styling */
        h1, h2, h3 {
            color: var(--text-primary);
            font-weight: 600;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Input and Text Area Styling */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1.5px solid var(--input-border);
            border-radius: 8px;
            padding: 10px;
            transition: border-color 0.3s ease;
        }

        .stTextInput > div > div > input:focus, 
        .stTextArea > div > div > textarea:focus {
            border-color: var(--input-focus);
            box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
        }

        /* Button Styling */
        .stButton > button {
            background-color: var(--button-primary);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            transition: background-color 0.3s ease, transform 0.2s;
        }

        .stButton > button:hover {
            background-color: var(--button-hover);
            transform: scale(1.05);
        }

        /* Status Message Styling */
        .stSuccess {
            background-color: var(--success-bg);
            color: var(--text-primary);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }

        .stError {
            background-color: var(--error-bg);
            color: var(--text-primary);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }

        .stWarning {
            background-color: var(--warning-bg);
            color: var(--text-primary);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        </style>
        """, unsafe_allow_html=True)

    def validate_email(self, email):
        # """Validate email format"""
        # email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # """Validate email format and restrict to iitmandi.ac.in domain."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@students.iitmandi\.ac\.in$'
        
        return re.match(email_regex, email) is not None

    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return random.randint(100000, 999999)

    def send_email(self, recipient_email, otp):
        """Send OTP via email with improved error handling"""
        try:
            sender_email = "b23277@students.iitmandi.ac.in"
            sender_password = "xeqz fkph iypn ondb"
            
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = "DP Project OTP"
            
            body = f"""
            Hello!
            
            Your OTP for DP project submission is: {otp}
            
            This OTP is valid for 5 minutes.
            
            Best regards,
            Gatherhub Team
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

    def image_to_base64(self, image, max_width=300, max_height=300, quality=60):
        """Convert an image to Base64 string with optional resizing and compression."""
        if image is not None:
            img = Image.open(image)
            
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            img.thumbnail((max_width, max_height))
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=quality)
            buffer.seek(0)
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
        return None

    def verify_otp(self, email, user_otp):
        """Verify OTP with comprehensive validation"""
        if not email or not user_otp:
            st.error("Email and OTP are required.")
            return False
        
        if email not in st.session_state.otp_storage:
            st.error("Please request an OTP first.")
            return False
        
        stored_otp_info = st.session_state.otp_storage[email]
        
        if datetime.now() > stored_otp_info["expires"]:
            st.error("OTP has expired. Please request a new one.")
            return False
        
        if user_otp != str(stored_otp_info["otp"]):
            st.error("Invalid OTP. Please try again.")
            return False
        
        # Mark as verified
        st.session_state.otp_storage[email]["verified"] = True
        return True

    def check_group_exists(self, group_number):
        """Check if a group already exists"""
        try:
            response = requests.get(f"{BASE_URL}/groups/{group_number}")
            
            if response.status_code == 200:
                st.error(f"Group {group_number} already exists!")
                return True
            elif response.status_code == 404:
                return False
            else:
                st.error(f"Unexpected error checking group existence. Status code: {response.status_code}")
                return True
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error checking group existence: {e}")
            return True

    def render_group_form(self):
        """Render the group submission form"""
        # Apply custom styling
        self.apply_custom_css()

        st.title("📋 GatherHub DP Project Management")
        st.markdown("""
        <div style="text-align: center; color: #7f8c8d; margin-bottom: 20px;">
            Submit your project details with ease and security
        </div>
        """, unsafe_allow_html=True)
        
        # Reset submission status if needed
        if st.session_state.get('submission_completed', False):
            reset = st.checkbox("Reset for Another Submission", key="reset_submission")
            if reset:
                st.session_state.submission_completed = False
                st.rerun()
        
        # Prevent multiple submissions
        if st.session_state.get('submission_completed', False):
            st.warning("🎉 You have already completed a submission. Reset to submit another group.")
            return

        # Group Details
        st.subheader("🔢 Group Details")
        group_no = st.text_input("Group Number", help="Enter a unique group number")
        project_name = st.text_input("Project Name", help="Enter your project's title")
        description = st.text_area("Project Description", help="Briefly describe your project")
        
        # Faculty Members
        st.subheader("👥 Faculty Members")
        num_faculty = st.number_input("Number of Faculty", min_value=1, max_value=5, value=1, help="Select number of faculty members")
        faculty_members = [st.text_input(f"Faculty {i+1} Name", help=f"Name of faculty member {i+1}") for i in range(num_faculty)]
        
        # Group Members
        st.subheader("👥 Group Members")
        num_members = st.number_input("Number of Members", min_value=1, max_value=8, value=1, help="Select number of group members")
        members = [
            {
                "name": st.text_input(f"Member {i+1} Name", help=f"Name of member {i+1}"),
                "roll_no": st.text_input(f"Member {i+1} Roll Number", help=f"Roll number of member {i+1}"),
                "contribution": st.text_area(f"Member {i+1} Contribution", help=f"Describe member {i+1}'s project contribution")
            }
            for i in range(num_members)
        ]
        
        # Image Upload
        st.subheader("🖼️ Project Images")
        uploaded_images = st.file_uploader(
            "Upload Group Images (It is recommended to compress them before uploading)",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload project-related images (Optional)"
        )

        image_data = []
        if uploaded_images:
            for img in uploaded_images:
                if img.size > 1 * 1024 * 1024:  # Check if file size exceeds 1 MB
                    st.error(f"❌ {img.name} is larger than 1 MB. Please compress and upload again.")
                else:
                    base64_img = self.image_to_base64(img)
                    if base64_img:
                        image_data.append(base64_img)
                
        # Email Verification Section
        st.subheader("🔒 Email Verification")
        email = st.text_input("Enter Your Email for Verification", help="Enter your email to receive OTP")
        
        if email and not self.validate_email(email):
            st.error("Only email addresses ending with '@students.iitmandi.ac.in' are allowed.")
        # OTP Sending Cooldown
        if email in st.session_state.otp_storage and "last_sent" in st.session_state.otp_storage[email]:
            elapsed = (datetime.now() - st.session_state.otp_storage[email]["last_sent"]).total_seconds()
            time_remaining = max(0, 30 - elapsed)
            can_resend = time_remaining <= 0
        else:
            time_remaining = 0
            can_resend = True

        if time_remaining > 0:
            st.info(f"⏳ You can resend the OTP in {int(time_remaining)} seconds.")

        otp_col1, otp_col2 = st.columns([2, 1])

        with otp_col1:
            user_otp = st.text_input("🔐 Enter OTP", placeholder="Enter 6-digit OTP", help="Enter the OTP sent to your email")

        with otp_col2:
            # Send OTP Button
            if st.button("📤 Send OTP", disabled=not can_resend, type="secondary"):
                if not email:
                    st.error("Please enter your email address.")
                elif not self.validate_email(email):
                    st.error("Please enter a valid email address.")
                else:
                    otp = self.generate_otp()
                    if self.send_email(email, otp):
                        st.session_state.otp_storage[email] = {
                            "otp": str(otp),
                            "expires": datetime.now() + timedelta(minutes=5),
                            "last_sent": datetime.now(),
                            "verified": False
                        }
                        st.success("OTP sent! Please check your email.")
                    else:
                        st.error("Failed to send OTP. Please try again.")

        # OTP Verification Button
        if st.button("✅ Verify OTP", type="secondary"):
            if self.verify_otp(email, user_otp):
                st.success("✅ Email verified successfully!")

        # Display Verification Status
        if email in st.session_state.otp_storage:
            if st.session_state.otp_storage[email].get("verified", False):
                st.markdown('<p style="color:green; text-align:center;">✅ Email Verified</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:orange; text-align:center;">⏳ Verification Pending</p>', unsafe_allow_html=True)

        # Submit Group Details
        st.markdown("---")  # Add a divider
        if st.button("🚀 Submit Group Details", type="primary"):
            # Validate email verification
            if not email or email not in st.session_state.otp_storage or not st.session_state.otp_storage[email].get("verified", False):
                st.error("Please verify your email before submitting!")
                return

            # Validate email format
            if not self.validate_email(email):
                st.error("Please enter a valid email address.")
                return

            # Validate required fields
            if not group_no or not project_name:
                st.error("Group Number and Project Name are required!")
                return

            # Check if group already exists
            if self.check_group_exists(group_no):
                return

            # Prepare payload
            payload = {
                "Group_number": int(group_no),
                "project_name": project_name,
                "Description": description,
                "Faculty": [f for f in faculty_members if f],
                "members": [m for m in members if m["name"]],
                "image": image_data,
                "emailUsed": email
            }

            try:
                    response = requests.post(f"{BASE_URL}/groups", json=payload)
                    if response.status_code in [200, 201]:
                        st.balloons()  # Add a fun celebration effect
                        st.success("🎉 Group added successfully!")
                        st.session_state.submission_completed = True
                        st.rerun()
                    else:
                        st.error(f"Failed to add group: {response.text}")
            except requests.exceptions.RequestException as e:
                    st.error(f"Error submitting group: {e}")

def main():
    st.set_page_config(
        page_title="GatherHub DP Project Management", 
        page_icon="📋", 
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    app = GroupSubmissionApp()
    app.render_group_form()

if __name__ == "__main__":
    main()
    
    