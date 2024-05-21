import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_background(email: str):
    corpo_email = """\
    Clique no link para redefinir sua senha: <link>
    <p>Parágrafo1</p>
    <p>Parágrafo2</p>
    """

    sender_email = os.environ["EMAIL_USER"]
    sender_password = os.environ["EMAIL_PASS"]
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Redefinição de senha"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Clique no link para redefinir sua senha: <link>
    """
    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("smtp.ethereal.email", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
