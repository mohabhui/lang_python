
"""
python 3
Author: mohabhui
Date: 12-Mar-2024

This is configured to send gmail with attachment.

Instruction:

    • Update the "User Configuration" section of the code. For help, google "how to use gmail as smtp server"
    • Run this code
    • Open browser, go to page http://127.0.0.1:5000/sendemail/
    • Press 'send email' button on the page
"""


import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  # New line
from email.mime.base import MIMEBase  # New line
from email import encoders  # New line

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route("/sendemail/")
def sendemail():
    #================================================= User configuration ===================================================
    sender_email = "place_holder" # replace place_holder with sender email e.g. abc@gmail.com
    sender_name = "MMB-Sender"
    password = "place_holder" # replace place_holder with app password of sender email (Not the regular password) [Google "how to use gmail as smtp server"]
    receiver_emails = ["place_holder"] # replace place_holder with receiver email e.g. abc@gmail.com or emails
    receiver_names = ["MMB-Receiver"]
    email_body = "This email is sent by ....."
    filename = 'turtle.jpg'
    #============================================================ xxx ======================================================

    for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
    		print("Sending the email...")
    		# Configurating user's info
    		msg = MIMEMultipart()
    		msg['To'] = formataddr((receiver_name, receiver_email))
    		msg['From'] = formataddr((sender_name, sender_email))
    		msg['Subject'] = 'Hello, my friend ' + receiver_name

    		msg.attach(MIMEText(email_body, 'html'))

    		try:
    			# Open PDF file in binary mode
    			with open(filename, "rb") as attachment:
    							part = MIMEBase("application", "octet-stream")
    							part.set_payload(attachment.read())

    			# Encode file in ASCII characters to send by email
    			encoders.encode_base64(part)

    			# Add header as key/value pair to attachment part
    			part.add_header(
    					"Content-Disposition",
    					f"attachment; filename= {filename}",
    			)

    			msg.attach(part)
    		except Exception as e:
    				print(f'Oh no! We didn\'t found the attachment!\n{e}')
    				break

    		try:
    				# Creating a SMTP session | use 587 with TLS, 465 SSL and 25
    				server = smtplib.SMTP('smtp.gmail.com', 587)
    				# Encrypts the email
    				context = ssl.create_default_context()
    				server.starttls(context=context)
    				# We log in into our Google account
    				server.login(sender_email, password)
    				# Sending email from sender, to receiver with the email body
    				server.sendmail(sender_email, receiver_email, msg.as_string())
    				print('Email sent!')
    		except Exception as e:
    				print(f'Oh no! Something bad happened!\n{e}')
    				break
    		finally:
    				print('Closing the server...')
    				server.quit()
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)

