


# import streamlit as st
# import pandas as pd
# import requests
# from typing import List, Dict
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def post_selected_attendees(url: str, selected_attendees: List[Dict]) -> bool:
#     """Post selected attendees to the API"""
#     try:
#         payload = {"attendees": selected_attendees}
#         print("payload: ", payload)
#         response = requests.post(url, json=payload)
#         print("response: ", response.json())
#         response.raise_for_status()
#         return True
#     except requests.RequestException as e:
#         st.error(f"Error posting attendees: {str(e)}")
#         return False

# def send_email_to_attendees(attendees: List[Dict]):
#     """Send confirmation emails to attendees"""
#     # Email configuration
#     smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
#     smtp_port = 587
#     # sender_email = "gatherhubiitmandi@gmail.com"  # Replace with your email
#     sender_email = "sahniwesh@gmail.com"  # Replace with your email
#     # sender_password = "armf odpa unrp vkjz"  # Replace with your email password
#     sender_password = "poqo fznf wprs kmru"  # Replace with your email password

#     try:
#         # Connect to SMTP server
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(sender_email, sender_password)

#         for attendee in attendees:
#             recipient_email = attendee["email"]
#             subject = "🎉 Registration Confirmation"
#             body = f"Hello {attendee['name']},\n\nHare Krishna!\n\nBest regards,\nGatherHub Team"

#             # Compose the email
#             msg = MIMEMultipart()
#             msg["From"] = sender_email
#             msg["To"] = recipient_email
#             msg["Subject"] = subject
#             msg.attach(MIMEText(body, "plain"))

#             # Send the email
#             server.sendmail(sender_email, recipient_email, msg.as_string())

#         server.quit()
#         return True
#     except Exception as e:
#         st.error(f"Error sending emails: {str(e)}")
#         return False

# def main_attendee_csv():
#     st.title("🎉 Conference Attendee Management 🎉")
#     st.markdown("""
#         <style>
#         .css-1d391kg {background-color: #f0f8ff;} 
#         .css-1v3fvcr {background-color: #87CEFA; border: none;}
#         </style>
#     """, unsafe_allow_html=True)

#     conference_code = st.session_state.get('current_user', 'Guest')
#     st.markdown(f"**Logged in as:** `{conference_code}`")

#     post_url = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/sendInvitation"

#     # Step 1: File uploader
#     st.header("📂 Upload CSV File with Attendee Data")
#     uploaded_file = st.file_uploader(
#         "Upload your attendee CSV file here", 
#         type=["csv"], 
#         help="The file should contain columns: name, email."
#     )

#     if uploaded_file:
#         # Step 2: Load the CSV file
#         try:
#             df = pd.read_csv(uploaded_file)
#             st.success("✅ File successfully uploaded and processed!")
            
#             # Check for required columns
#             required_columns = ["name", "email"]
#             if not all(column in df.columns for column in required_columns):
#                 st.error(f"❌ CSV file must contain columns: {', '.join(required_columns)}")
#                 return
            
#             # Check for missing or empty values in required columns
#             missing_values = df[required_columns].isnull() | (df[required_columns] == '')
#             if missing_values.any().any():
#                 st.error(f"❌ CSV contains empty or missing values in required columns: {', '.join(required_columns)}")
#                 return

#             st.dataframe(df, use_container_width=True)
#         except Exception as e:
#             st.error(f"❌ Failed to process the file: {e}")
#             return

#         # Step 3: Allow selection of attendees
#         st.header("🔘 Select Attendees to Register")
#         select_all = st.checkbox("Select All Attendees", help="Select all attendees from the uploaded CSV file.")
        
#         if select_all:
#             selected_indices = list(range(len(df)))
#         else:
#             selected_indices = st.multiselect(
#                 "Select attendees to register",
#                 range(len(df)),
#                 format_func=lambda x: f"{df.iloc[x]['name']} ({df.iloc[x]['email']})",
#                 help="Select attendees from the list"
#             )

#         # Step 4: Display selected attendees
#         if selected_indices:
#             st.subheader("📑 Selected Attendees")
#             selected_df = df.iloc[selected_indices][['name', 'email']]
#             st.dataframe(selected_df, use_container_width=True)

#             # Step 5: Submit selected attendees and send emails
#             if st.button("✅ Submit and Notify Attendees"):
#                 # Convert selected rows to a dictionary and add username field as email
#                 selected_attendees = df.iloc[selected_indices].to_dict('records')

#                 # Add 'username' field with the value of 'email'
#                 for attendee in selected_attendees:
#                     attendee['username'] = attendee['email']  # Set username as email

#                 with st.spinner("Submitting selected attendees..."):
#                     if post_selected_attendees(post_url, selected_attendees):
#                         st.success(f"✅ Successfully submitted {len(selected_attendees)} attendees!")
                        
#                         # Send emails
#                         with st.spinner("Sending confirmation emails..."):
#                             if send_email_to_attendees(selected_attendees):
#                                 st.success(f"✅ Confirmation emails sent to {len(selected_attendees)} attendees!")
#                             else:
#                                 st.error("❌ Failed to send confirmation emails.")

#                         st.write("Submitted attendees:")
#                         for attendee in selected_attendees:
#                             st.write(f"✓ {attendee['name']} ({attendee['email']})")
#                     else:
#                         st.error("❌ Failed to submit attendees")
#         else:
#             st.info("❓ No attendees selected yet. Use the multiselect above or check 'Select All'.")

#     else:
#         st.info("📥 Please upload a CSV file to proceed.")

# if __name__ == "__main__":
#     main_attendee_csv()
























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

Thank you for registering for the IC-202P Conference! This email is part of our Conference Management System project.

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










# def send_email_to_attendees(attendees: List[Dict], smtp_config: Dict) -> Tuple[bool, str, List[str]]:
#     """
#     Send beautifully formatted confirmation emails to attendees with comprehensive error handling.
    
#     Args:
#         attendees: List of attendee dictionaries
#         smtp_config: SMTP server configuration
        
#     Returns:
#         Tuple[bool, str, List[str]]: (Success status, Error message, List of failed email addresses)
#     """
#     failed_emails = []
#     server = None
    
#     html_template = """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <meta charset="utf-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Conference Registration Confirmation</title>
#         <style>
#             body {
#                 font-family: Arial, sans-serif;
#                 line-height: 1.6;
#                 color: #333333;
#                 max-width: 600px;
#                 margin: 0 auto;
#                 padding: 20px;
#             }
#             .header {
#                 background-color: #4A90E2;
#                 color: white;
#                 padding: 30px;
#                 text-align: center;
#                 border-radius: 8px 8px 0 0;
#             }
#             .content {
#                 background-color: #ffffff;
#                 padding: 30px;
#                 border: 1px solid #e1e1e1;
#                 border-radius: 0 0 8px 8px;
#             }
#             .button {
#                 display: inline-block;
#                 padding: 12px 24px;
#                 background-color: #4CAF50;
#                 color: white;
#                 text-decoration: none;
#                 border-radius: 4px;
#                 margin: 20px 0;
#             }
#             .contact-info {
#                 background-color: #f9f9f9;
#                 padding: 20px;
#                 border-radius: 4px;
#                 margin-top: 20px;
#             }
#             .footer {
#                 text-align: center;
#                 margin-top: 30px;
#                 color: #666666;
#                 font-size: 14px;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="header">
#             <h1>🎉 Welcome to the Conference!</h1>
#         </div>
#         <div class="content">
#             <p>Dear {name},</p>
            
#             <p>Thank you for registering for the IC-202P Conference! This email is part of Group 0's Conference Management System project.</p>
            
#             <p><strong>Important:</strong> Your attendance will be marked based on this registration. Please ensure you complete the following steps:</p>
            
#             <p style="text-align: center;">
#                 <a href="https://niweshvistingcardposting.streamlit.app/?email={email}&conference_code=DP2024" class="button">
#                     Complete Your Registration Details
#                 </a>
#             </p>
            
#             <div class="contact-info">
#                 <h3>Need Assistance?</h3>
#                 <p>Please don't hesitate to contact our team lead:</p>
#                 <ul style="list-style-type: none; padding-left: 0;">
#                     <li><strong>Name:</strong> Niwesh Sah</li>
#                     <li><strong>Mobile:</strong> 9451864348</li>
#                     <li><strong>Roll No.:</strong> B23277</li>
#                 </ul>
#             </div>
            
#             <div class="footer">
#                 <p>Best regards,<br><strong>GatherHub Team</strong></p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
    
#     try:
#         # Connect to SMTP server
#         server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
#         server.starttls()
#         server.login(smtp_config['email'], smtp_config['password'])
        
#         for attendee in attendees:
#             try:
#                 recipient_email = attendee["email"]
#                 subject = "🎉 Conference Registration Confirmation"
                
#                 # Create message container
#                 msg = MIMEMultipart('alternative')
#                 msg["From"] = smtp_config['email']
#                 msg["To"] = recipient_email
#                 msg["Subject"] = subject
                
#                 # Create both plain-text and HTML versions of the message
#                 text_content = f"""
# Hello {attendee['name']},

# Thank you for registering for the IC-202P Conference! This email is part of our Conference Management System project.

# Please complete your registration details at:
# https://niweshvistingcardposting.streamlit.app/?email={recipient_email}&conference_code=DP2024

# Need help? Contact Niwesh Sah (Roll No. B23277) at 9451864348.

# Best regards,
# GatherHub Team
#                 """
                
#                 # Substitute attendee details into HTML template
#                 html_content = html_template.format(
#                     name=attendee['name'],
#                     email=recipient_email
#                 )
                
#                 # Attach both versions
#                 part1 = MIMEText(text_content, 'plain')
#                 part2 = MIMEText(html_content, 'html')
#                 msg.attach(part1)
#                 msg.attach(part2)
                
#                 server.sendmail(smtp_config['email'], recipient_email, msg.as_string())
#                 logger.info(f"Successfully sent email to {recipient_email}")
                
#             except Exception as e:
#                 logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
#                 failed_emails.append(recipient_email)
                
#     except Exception as e:
#         error_msg = f"Email sending error: {str(e)}"
#         logger.error(error_msg)
#         return False, error_msg, failed_emails
        
#     finally:
#         if server:
#             server.quit()
            
#     if failed_emails:
#         return False, f"Failed to send emails to {len(failed_emails)} recipients", failed_emails
    
#     return True, "", []

def main_attendee_csv():
    st.title("🎉 Conference Attendee Management 🎉")
    
    # Custom styling
    st.markdown("""
        <style>
        .css-1d391kg {background-color: #f0f8ff;} 
        .css-1v3fvcr {background-color: #87CEFA; border: none;}
        </style>
    """, unsafe_allow_html=True)

    # Session state management
    conference_code = st.session_state.get('current_user', 'Guest')
    st.markdown(f"**Logged in as:** `{conference_code}`")

    post_url = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/sendInvitation"


    # SMTP Configuration
    smtp_config = {
        'server': "smtp.gmail.com",
        'port': 587,
        'email': "sahniwesh@gmail.com",
        'password': "poqo fznf wprs kmru"
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