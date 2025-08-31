import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.core.log import logger

SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587


def send_email(  # noqa: PLR0913, PLR0917
    sender_email: str,
    password_email: str,
    recipient_emails: list[str],
    subject: str,
    body: str,
    smtp_server: str = SMTP_SERVER,
    smtp_port: int = SMTP_PORT,
):
    """Envio de email

    Args:
        sender_email (str): email do remetente
        password_email (str): senha do remetente
        recipient_emails (list[str]): emails do destinatários
        subject (str): assunto
        body (str): corpo do email
        smtp_server (str, optional): servidor SMTP. Defaults to SMTP_SERVER.
        smtp_port (int, optional): porta SMTP. Defaults to SMTP_PORT.

    Raises:
        err (Exception): retorna a exceção
    """

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
