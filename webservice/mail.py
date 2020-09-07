from config import PASSWORD
import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(type, title, sender, sender_url, event_url, body):
    email_address = 'mezgoodle@gmail.com'
    # receiver_email = 'proksima.maxim@gmail.com'

    message = MIMEMultipart('alternative')
    message['Subject'] = 'GitHub Alerts'
    message['From'] = email_address
    message['To'] = email_address

    # Plain Template
    text = f'''\
	Hi,
	How are you?
	New {type.capitalize()}, {title}, has been created.
	Link: {event_url}
	'''

    # HTML Template
    html = f'''\
	<html>
	<body>
		<h3>Hi, there are news from GitHub🥳</h3>
		<ul>
		<li>New {type.capitalize()}, <a href='{event_url}'>{title}</a>, has been created.</li>
		<li>Author: <a href='{sender_url}'>{sender}</a></li>
		<li>Body: {body}</li>
		</ul>
	</body>
	</html>
	'''

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(email_address, PASSWORD)
        server.sendmail(
            email_address, email_address, message.as_string()
        )
