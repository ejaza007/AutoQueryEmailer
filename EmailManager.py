import os
import smtplib
import threading
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import Encryption
import RecipientManager
import LogManager

#send a single email
def send_email(sender_email, sender_password, recipient_email, subject, message, file_path, image_path):
    LogManager.Log("SENDING EMAIL '" + subject + "' TO '" + recipient_email + "'")

    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'  # Change this if using a different email provider
    smtp_port = 587  # Change this if using a different email provider

    # Create a message object and set the recipient, subject, and message body
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    # Attach the file
    if not file_path.__eq__(''):
        attachment = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=file_path)
        msg.attach(part)

    # Attach the image
    if not image_path.__eq__(''):
        img_data = open(image_path, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(image_path))
        msg.attach(image)

    try:
        # Log in to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)

        # Clean up the connection
        server.quit()

        LogManager.Log("EMAIL "+ subject +" SUCCESSFULLY SENT TO " + recipient_email)
    except Exception as e:
        LogManager.Log("ERROR SENDING " + subject + " EMAIL TO " + recipient_email, str(e))

#send email to all emails in the recipient list
def Send_Routine_Emails():
    sender_cred = Encryption.read_sender_credentials()
    sender_email = sender_cred[0]
    sender_password = sender_cred[1]
    recipient_emails = RecipientManager.get_emails()

    for recipient_email in recipient_emails:
        send_email(sender_email, sender_password, recipient_email, subject, message, file_path, image_path)

#send email to all emails in the list provided (in the context of this program, the provided list will be a subset of the recipient list)
def Send_Emails(recipient_emails):
    sender_cred = Encryption.read_sender_credentials()
    sender_email = sender_cred[0]
    sender_password = sender_cred[1]

    threads = []
    for recipient_email in recipient_emails:
        thread = threading.Thread(target=send_email, args=(sender_email, sender_password, recipient_email, subject, message, file_path, image_path))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    LogManager.Log("ALL EMAILS SENT")

#variables and setters to set email content
subject = 'Test Email'
message = 'This is a test email.'
file_path = ''  # Replace with the path to your file attachment (optional)
image_path = ''  # Replace with the path to your image attachment (optional)

def set_Subject(subject_text):
    subject = subject_text

def set_Message(message_text):
    message = message_text

def set_file_path(path):
    file_path = path

def set_image_path(path):
    image_path = path