import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = 'mezgoodle@gmail.com'
receiver_email = 'proksima.maxim@gmail.com'
password = 'password'

message = MIMEMultipart('alternative')
message['Subject'] = 'multipart test'
message['From'] = sender_email
message['To'] = receiver_email

# HTML-Template
text = '''\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com'''
html = '''\
<html>
  <body>
    <p><h1>Hi</h1>,<br>
       How are you?<br>
       <a href='http://www.github.com'>GitHub</a> 
       has many great tutorials.
    </p>
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
        sender_email, receiver_email, message.as_string()
    )
