
import os
import streamlit as st
import pandas as pd
import requests
from typing import List, Dict, Tuple, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime
import re
from dotenv import load_dotenv

rest_api_url = os.getenv("REST_API_URL")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailValidationError(Exception):
    """Custom exception for email validation errors"""
    pass

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

def validate_email(email: str) -> bool:
    """
    Validate email format using regex pattern.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_csv_data(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate the CSV data for required columns and data quality.
    
    Args:
        df: Pandas DataFrame containing the CSV data
        
    Returns:
        Tuple[bool, str]: (Success status, Error message if any)
    """
    try:
        # Check for required columns
        required_columns = ["name", "email"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"

        # Check for empty values
        empty_values = df[required_columns].isnull().any() | (df[required_columns] == '').any()
        if empty_values.any():
            return False, "CSV contains empty or missing values in required columns"

        # Validate email formats
        invalid_emails = []
        for idx, row in df.iterrows():
            if not validate_email(row['email']):
                invalid_emails.append(f"Row {idx + 1}: {row['email']}")
        
        if invalid_emails:
            return False, f"Invalid email formats found:\n{chr(10).join(invalid_emails)}"

        return True, ""
    except Exception as e:
        logger.error(f"Error validating CSV data: {str(e)}")
        return False, f"Error validating CSV data: {str(e)}"


def post_selected_attendees(url: str, selected_attendees: List[Dict]) -> Tuple[bool, str]:
    """
    Post selected attendees to the API with proper error handling.
    
    Args:
        url: API endpoint URL
        selected_attendees: List of attendee dictionaries
        
    Returns:
        Tuple[bool, str]: (Success status, Error message if any)
    """
    try:
        payload = {"attendees": selected_attendees}
        logger.info(f"Sending payload to {url}")
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info("Successfully posted attendees to API")
            return True, ""
        else:
            error_msg = f"API error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return False, error_msg
            
    except requests.Timeout:
        error_msg = "API request timed out. Please try again."
        logger.error(error_msg)
        return False, error_msg
    except requests.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error posting attendees: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def send_email_to_attendees(attendees: List[Dict], smtp_config: Dict) -> Tuple[bool, str, List[str]]:
    """
    Send confirmation emails to attendees with comprehensive error handling.
    
    Args:
        attendees: List of attendee dictionaries
        smtp_config: SMTP server configuration
        
    Returns:
        Tuple[bool, str, List[str]]: (Success status, Error message, List of failed email addresses)
    """
    failed_emails = []
    server = None
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
        server.starttls()
        server.login(smtp_config['email'], smtp_config['password'])
        
        for attendee in attendees:
            try:
                recipient_email = attendee["email"]
                subject = "🎉 Registration Confirmation"
                body = f"""
Hello {attendee['name']},

This email is part of our Conference Management System project, group-0 DP project. We are trying to demonstrate the working of our system by trying to mark your attendance based on this registration. You are kindly requested to complete your registration details by clicking on the link below.

Please complete your registration details at:
https://niweshvistingcardposting.streamlit.app/?email={recipient_email}&conference_code=DP2024

Need help? Contact Niwesh Sah (Roll No. B23277) at 9451864348.

Best regards,
GatherHub Team
                """

                msg = MIMEMultipart()
                msg["From"] = smtp_config['email']
                msg["To"] = recipient_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                server.sendmail(smtp_config['email'], recipient_email, msg.as_string())
                logger.info(f"Successfully sent email to {recipient_email}")
                
            except Exception as e:
                logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
                failed_emails.append(recipient_email)

    except smtplib.SMTPAuthenticationError:
        return False, "SMTP authentication failed. Please check your credentials.", failed_emails
    except smtplib.SMTPException as e:
        return False, f"SMTP error occurred: {str(e)}", failed_emails
    except Exception as e:
        return False, f"Unexpected error sending emails: {str(e)}", failed_emails
    finally:
        if server:
            try:
                server.quit()
            except Exception as e:
                logger.error(f"Error closing SMTP connection: {str(e)}")

    if failed_emails:
        return False, f"Failed to send emails to {len(failed_emails)} recipients", failed_emails
    return True, "", []


def main_attendee_csv():
    st.title("🎉 Conference Attendee Management 🎉")
    
    # Custom styling
    st.markdown("""
        <style>
        .css-1d391kg {background-color: #f0f8ff;} 
        .css-1v3fvcr {background-color: #87CEFA; border: none;}
        </style>
    """, unsafe_allow_html=True)
    
    # "gatherhubniwesh@gmail.com"
    # Session state management
    conference_code = st.session_state.get('current_user', 'Guest')
    st.markdown(f"**Logged in as:** `{conference_code}`")

    post_url = f"{rest_api_url}/user/conference/{conference_code}/eventCard/sendInvitation"


    # SMTP Configuration
    smtp_config = {
        'server': "smtp.gmail.com",
        'port': 587,
        # 'email': "sahniwesh@gmail.com",
        'email': os.getenv("EMAIL"),
        'password': os.getenv("EMAIL_PASSWORD")
    }

    # File upload section
    st.header("📂 Upload CSV File with Attendee Data")
    uploaded_file = st.file_uploader(
        "Upload your attendee CSV file here", 
        type=["csv"], 
        help="The file should contain columns: name, email."
    )

    if uploaded_file:
        try:
            # Load and validate CSV
            df = pd.read_csv(uploaded_file)
            validation_success, validation_message = validate_csv_data(df)
            
            if not validation_success:
                st.error(f"❌ {validation_message}")
                return
            
            st.success("✅ File successfully uploaded and validated!")
            st.dataframe(df, use_container_width=True)

            # Attendee selection
            st.header("🔘 Select Attendees to Register")
            select_all = st.checkbox("Select All Attendees")
            
            selected_indices = (
                list(range(len(df))) if select_all
                else st.multiselect(
                    "Select attendees to register",
                    range(len(df)),
                    format_func=lambda x: f"{df.iloc[x]['name']} ({df.iloc[x]['email']})"
                )
            )

            if selected_indices:
                st.subheader("📑 Selected Attendees")
                selected_df = df.iloc[selected_indices][['name', 'email']]
                st.dataframe(selected_df, use_container_width=True)

                if st.button("✅ Submit and Notify Attendees"):
                    selected_attendees = df.iloc[selected_indices].to_dict('records')
                    for attendee in selected_attendees:
                        attendee['username'] = attendee['email']

                    # Submit attendees
                    with st.spinner("Submitting selected attendees..."):
                        submit_success, submit_error = post_selected_attendees(post_url, selected_attendees)
                        
                        if submit_success:
                            st.success(f"✅ Successfully submitted {len(selected_attendees)} attendees!")
                            
                            # Send emails
                            with st.spinner("Sending confirmation emails..."):
                                email_success, email_error, failed_emails = send_email_to_attendees(
                                    selected_attendees, 
                                    smtp_config
                                )
                                
                                if email_success:
                                    st.success("✅ All confirmation emails sent successfully!")
                                else:
                                    if failed_emails:
                                        st.warning(f"⚠️ Failed to send emails to {len(failed_emails)} recipients:")
                                        for email in failed_emails:
                                            st.write(f"- {email}")
                                    else:
                                        st.error(f"❌ {email_error}")
                        else:
                            st.error(f"❌ {submit_error}")
            else:
                st.info("❓ No attendees selected yet. Use the multiselect above or check 'Select All'.")

        except pd.errors.EmptyDataError:
            st.error("❌ The uploaded CSV file is empty.")
        except pd.errors.ParserError:
            st.error("❌ Error parsing CSV file. Please ensure it's properly formatted.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    else:
        st.info("📥 Please upload a CSV file to proceed.")

if __name__ == "__main__":
    main_attendee_csv()