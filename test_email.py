import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "gatherhubiitmandi@gmail.com"
sender_password = "armf odpa unrp vkjz"  # Replace with your App Password
recipient_email = "sahniwesh@gmail.com"

try:
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = "Test Email"

    body = "This is a test email."
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
