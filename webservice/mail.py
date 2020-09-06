from .config import PASSWORD
import yagmail

def send_mail(type):
	receiver = "mezgoodle@gmail.com"
	body = f'''\
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

	yag = yagmail.SMTP("mezgoodle@gmail.com", PASSWORD)
	yag.send(
		to=receiver,
		subject="Yagmail test with attachment",
		contents=body, 
	)
