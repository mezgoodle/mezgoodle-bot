from .config import PASSWORD
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(type):
	sender_email = 'mezgoodle@gmail.com'
	# receiver_email = 'proksima.maxim@gmail.com'
	password = PASSWORD

	message = MIMEMultipart('alternative')
	message['Subject'] = 'GitHub Alerts'
	message['From'] = sender_email
	message['To'] = sender_email

	# HTML-Template
	text = '''\
	Hi,
	How are you?
	Real Python has many great tutorials:
	www.realpython.com'''
	html = f'''\
	<html>
	<body>
		<h3>Hi, there are news from GitHub🥳</h3>
		<ul>
		<li>New {type}, <a href='http://www.github.com'>GitHub</a>, has been created.</li>
		<li>Author: <a href='http://www.github.com'>GitHub</a> </li>
		<li>{type.capitalize()}: <a href='http://www.github.com'>GitHub</a> </li>
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
		server.login(sender_email, password)
		server.sendmail(
			sender_email, sender_email, message.as_string()
		)