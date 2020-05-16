# Automation Script To Send Emails Message To Email Account
# TODO:Just Create File With NAme job_emails On Desktop Dir In Linux System
import os
import re
from os import path
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


my_cv_file = "yourCvFIle.pdf"

MY_ADDRESS  = 'enter your email account'
PASSWORD    = 'enter email password'

job_emails_file = 'enter txt file name which contain emails without extension' # like target_emails
email_subject   = "PHP Backend Developer Vacancy."
email_content   = """\
Subject: PHP Backend Developer Vacancy.

I'm a PHP Backend Developer with experience 4 years in my career.

And Here's My CV:"""

# Target Files Location
os.chdir(r'/home/yourdevice/Desktop')
file_path = os.getcwd() + '/' + job_emails_file
cv_file_path = os.getcwd() + '/' + my_cv_file

# Initialize server & Login to account
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(MY_ADDRESS, PASSWORD)


def validateEmail(target_email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,target_email)):
        return True
    else:
        return False

def attachCv(message):
    with open(cv_file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment",filename=my_cv_file)
    message.attach(part)

def getEmails():
    emails = []
    with open(file_path) as target_file:
        temp_data = target_file.readlines()
        for line in temp_data:
            if not line:
                break
            if (validateEmail(line)):
                emails.append(line)

    return emails




# Main Script
if(not path.exists(file_path)):
    print('file not found')
    sys.exit()

for target_email in getEmails():

    msg = MIMEMultipart()
    msg['From'] = MY_ADDRESS
    msg['To'] = target_email
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_content,'plain'))
    msg.add_header("Subject",email_subject)

    # attach cv
    attachCv(msg)

    try:
        server.sendmail(msg['From'],msg['To'],msg.as_string())
        del msg
        print("Email To {} Sent Successfuly".format(target_email))
    except smtplib.SMTPException:
        print("Error: Email To {} Not Sent".format(target_email))

    server.quit()



