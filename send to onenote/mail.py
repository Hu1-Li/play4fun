#!/usr/bin/python
import smtplib, os, fnmatch
from email.mime.text import MIMEText
def sendemail(from_addr, to_addr,
		subject, content,
		login, password,
		smtpserver='smtp.163.com'):
	msg = MIMEText(content.encode('utf-8'), 'html', 'utf-8')
	msg['From'] = from_addr
	msg['To'] = to_addr
	msg['Subject'] = subject
	server = smtplib.SMTP(smtpserver)
	server.starttls()
	server.login(login, password)
	problems = server.sendmail(from_addr, to_addr, msg.as_string())
	server.quit()
	return problems

def get_html_file():
	html_file = ""
	for file in os.listdir('.'):
		if fnmatch.fnmatch(file, "*.html"):
			html_file = file
			vol, ext = os.path.splitext(html_file)
			f = open(html_file, "r").read().decode('utf-8')
			sendemail(from_addr = 'onenote_leah@163.com',
					  to_addr = 'me@onenote.com',
					  subject = vol,
					  content = f,
					  login = 'onenote_leah@163.com',
					  password = 'xxxxx')
			return 0

get_html_file()
