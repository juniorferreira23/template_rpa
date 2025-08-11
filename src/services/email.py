import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.core.log import logger

SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587


def send_email(  # noqa: PLR0913, PLR0917
    subject: str,
    body: str,
    sender_email: str,
    password_email: str,
    recipient_emails: list[str],
    smtp_server: str = SMTP_SERVER,
    smtp_port: int = SMTP_PORT,
):
    
    recipients = ', '.join(recipient_emails)
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipients
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.sendmail(sender_email, recipients, message.as_string())
        logger.info('Email sent to all recipients!')

    except Exception as err:
        logger.error(f'Error sending email: {err}')
        raise err
