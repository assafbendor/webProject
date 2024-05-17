import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_addr, sub, text):
    from_email = "bookforyousystem@gmail.com"

    # Email content
    subject = sub
    body = text

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = "bookforyousystem@gmail.com"
    message['To'] = to_addr
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, 'plain'))

    # Gmail SMTP server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # For starttls

    try:
        # Setup the SMTP server connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, "siec ourx ceih tpvs")  # Login to the sender's email account

        # Send the email
        text = message.as_string()
        server.sendmail(from_email, to_addr, text)

        # Close the SMTP server connection
        server.quit()

        return True
    except Exception as e:
        return f"Failed to send email: {e}"

# send_email("asaf.bendor2@gmail.com", "change password", "12345")
