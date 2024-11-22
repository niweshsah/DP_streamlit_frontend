


import streamlit as st
import pandas as pd
import requests
from typing import List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def post_selected_attendees(url: str, selected_attendees: List[Dict]) -> bool:
    """Post selected attendees to the API"""
    try:
        payload = {"attendees": selected_attendees}
        print("payload: ", payload)
        response = requests.post(url, json=payload)
        print("response: ", response.json())
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        st.error(f"Error posting attendees: {str(e)}")
        return False

def send_email_to_attendees(attendees: List[Dict]):
    """Send confirmation emails to attendees"""
    # Email configuration
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
    smtp_port = 587
    # sender_email = "gatherhubiitmandi@gmail.com"  # Replace with your email
    sender_email = "sahniwesh@gmail.com"  # Replace with your email
    # sender_password = "armf odpa unrp vkjz"  # Replace with your email password
    sender_password = "poqo fznf wprs kmru"  # Replace with your email password

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        for attendee in attendees:
            recipient_email = attendee["email"]
            subject = "🎉 Registration Confirmation"
            body = f"Hello {attendee['name']},\n\nHare Krishna!\n\nBest regards,\nGatherHub Team"

            # Compose the email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Send the email
            server.sendmail(sender_email, recipient_email, msg.as_string())

        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending emails: {str(e)}")
        return False

def main_attendee_csv():
    st.title("🎉 Conference Attendee Management 🎉")
    st.markdown("""
        <style>
        .css-1d391kg {background-color: #f0f8ff;} 
        .css-1v3fvcr {background-color: #87CEFA; border: none;}
        </style>
    """, unsafe_allow_html=True)

    conference_code = st.session_state.get('current_user', 'Guest')
    st.markdown(f"**Logged in as:** `{conference_code}`")

    post_url = f"http://gatherhub-r7yr.onrender.com/user/conference/{conference_code}/eventCard/sendInvitation"

    # Step 1: File uploader
    st.header("📂 Upload CSV File with Attendee Data")
    uploaded_file = st.file_uploader(
        "Upload your attendee CSV file here", 
        type=["csv"], 
        help="The file should contain columns: name, email."
    )

    if uploaded_file:
        # Step 2: Load the CSV file
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File successfully uploaded and processed!")
            
            # Check for required columns
            required_columns = ["name", "email"]
            if not all(column in df.columns for column in required_columns):
                st.error(f"❌ CSV file must contain columns: {', '.join(required_columns)}")
                return
            
            # Check for missing or empty values in required columns
            missing_values = df[required_columns].isnull() | (df[required_columns] == '')
            if missing_values.any().any():
                st.error(f"❌ CSV contains empty or missing values in required columns: {', '.join(required_columns)}")
                return

            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Failed to process the file: {e}")
            return

        # Step 3: Allow selection of attendees
        st.header("🔘 Select Attendees to Register")
        select_all = st.checkbox("Select All Attendees", help="Select all attendees from the uploaded CSV file.")
        
        if select_all:
            selected_indices = list(range(len(df)))
        else:
            selected_indices = st.multiselect(
                "Select attendees to register",
                range(len(df)),
                format_func=lambda x: f"{df.iloc[x]['name']} ({df.iloc[x]['email']})",
                help="Select attendees from the list"
            )

        # Step 4: Display selected attendees
        if selected_indices:
            st.subheader("📑 Selected Attendees")
            selected_df = df.iloc[selected_indices][['name', 'email']]
            st.dataframe(selected_df, use_container_width=True)

            # Step 5: Submit selected attendees and send emails
            if st.button("✅ Submit and Notify Attendees"):
                # Convert selected rows to a dictionary and add username field as email
                selected_attendees = df.iloc[selected_indices].to_dict('records')

                # Add 'username' field with the value of 'email'
                for attendee in selected_attendees:
                    attendee['username'] = attendee['email']  # Set username as email

                with st.spinner("Submitting selected attendees..."):
                    if post_selected_attendees(post_url, selected_attendees):
                        st.success(f"✅ Successfully submitted {len(selected_attendees)} attendees!")
                        
                        # Send emails
                        with st.spinner("Sending confirmation emails..."):
                            if send_email_to_attendees(selected_attendees):
                                st.success(f"✅ Confirmation emails sent to {len(selected_attendees)} attendees!")
                            else:
                                st.error("❌ Failed to send confirmation emails.")

                        st.write("Submitted attendees:")
                        for attendee in selected_attendees:
                            st.write(f"✓ {attendee['name']} ({attendee['email']})")
                    else:
                        st.error("❌ Failed to submit attendees")
        else:
            st.info("❓ No attendees selected yet. Use the multiselect above or check 'Select All'.")

    else:
        st.info("📥 Please upload a CSV file to proceed.")

if __name__ == "__main__":
    main_attendee_csv()
