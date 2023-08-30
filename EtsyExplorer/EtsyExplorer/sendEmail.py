# from scrapy.mail import MailSender 
import os
import logging
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def sendEmail(recipient=None, message=None):
  # mailer = MailSender()
  userEmail = os.environ["SCRAPY_USEREMAIL"]
  userPass = os.environ["SCRAPY_USERPASS"]
  
  if not recipient:
    recipient = os.environ["SCRAPY_DEFAULT_RECIPIENT"]

  msg = MIMEMultipart()
  msg["From"] = userEmail
  msg["To"] = recipient
  msg["Subject"] = "Scrapy Report"
  if not message:
    message = f"""
    Da lay du lieu xong luc {datetime.now().strftime("%H:%m %d-%m-%Y")}.
  """
  
  msg.attach(MIMEText(message))
  img = MIMEImage(open("EtsyExplorer/img/meme.jpg", "rb").read())
  img.add_header("Content-Disposition", "attachment; filename='image.jpg'")
  msg.attach(img)
  logger.info("Sending Email.")
  with smtplib.SMTP("smtp.gmail.com", 587) as mailServer:
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.login(userEmail, userPass)
    mailServer.sendmail(userEmail, recipient, msg.as_string())
  logger.info("Email sent.")

# sendEmail("nguyenthuy221210@gmail.com")
# print(os.getcwd())