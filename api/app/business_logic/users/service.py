import smtplib
from email.mime.text import MIMEText
from app.config import get_smtp_server, get_smtp_port, get_smtp_username, get_smtp_password
from jinja2 import Environment, FileSystemLoader


async def send_password_reset_email(email_to: str, reset_link: str) -> None:
    smtp_server = get_smtp_server()
    smtp_port = get_smtp_port()
    smtp_username = get_smtp_username()
    smtp_password = get_smtp_password()
    sender_email = smtp_username

    subject = 'Запрос на сброс пароля'

    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('reset_password_email_template.html')

    body = template.render(reset_link=reset_link)

    message = MIMEText(body, 'html', 'utf-8')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = email_to
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, email_to, message.as_string())

