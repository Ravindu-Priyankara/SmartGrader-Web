import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
import configparser

# Read the HTML template file
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        template = Template(file.read())
    return template

def mail(mail_address, subject, template_name):
    # Read configurations from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Email configurations
    sender_email = config['EMAIL']['sender_email']
    receiver_email = mail_address
    password = config['EMAIL']['password']

    # Create message container
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Read the HTML template
    template = read_template(template_name)

    # Fill in the template with dynamic content
    email_body = template.substitute(name="name")

    # Attach HTML content to the email
    message.attach(MIMEText(email_body, 'html'))

    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Log in to your Gmail account
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Quit the server
    server.quit()

    print("Email sent successfully!")
