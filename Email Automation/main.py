import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import time


# Function to send an automatic email response
def send_auto_reply(sender_email, sender_password, recipient_email, subject, body):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Compose the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Attach the body with the email
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to the server and login
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)

        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        print(f"Automatic response sent to {recipient_email}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server.quit()


# Function to check and respond to new emails
def check_inbox_and_respond(sender_email, sender_password):
    # Set up the IMAP server to read incoming emails
    imap_server = "imap.gmail.com"
    imap_port = 993

    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(sender_email, sender_password)
        mail.select("inbox")

        # Search for all emails (unseen emails)
        status, messages = mail.search(None, '(UNSEEN)')
        if status == "OK":
            for num in messages[0].split():
                # Fetch the email
                status, msg_data = mail.fetch(num, "(RFC822)")
                if status == "OK":
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = response_part[1]
                            # Decode email subject
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")

                            # From email address
                            from_ = msg.get("From")
                            if isinstance(from_, bytes):
                                from_ = from_.decode(encoding if encoding else "utf-8")

                            print(f"New email from {from_} with subject: {subject}")

                            # Prepare automatic response body
                            auto_reply_body = """Hello,

Thank you for reaching out. I am currently out of the office and will respond to your email as soon as possible.

Best regards,
Your Name"""

                            # Send the response email
                            send_auto_reply(sender_email, sender_password, from_, "Thank you for your email",
                                            auto_reply_body)

        # Logout from the server
        mail.logout()

    except Exception as e:
        print(f"Error checking inbox: {e}")


# Replace with your credentials
sender_email = "ingeniumprakashraj@gmail.com"  # Your email address
sender_password = "Prakashraj@EKA2024"  # Your email password or app-specific password

# Run the check every minute
while True:
    check_inbox_and_respond(sender_email, sender_password)
    time.sleep(60)  # Wait 60 seconds before checking again
