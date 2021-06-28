from fastapi import FastAPI
from app import schemas, models, database, oauth2
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List

conf = ConnectionConfig(
    MAIL_FROM="qhyzrlws2s@email.edu.pl",
    MAIL_USERNAME="bd3cbc38de74c15b2fad0dd9fbda6297",
    MAIL_PASSWORD="ff571f17834ef95ceabc98be3c6f3719",
    MAIL_PORT=587,
    MAIL_SERVER="in-v3.mailjet.com",
    MAIL_TLS=True,
    MAIL_SSL=False
)


async def product_changed_mail(emails, id):
   template = f"""
		<html>
		<body>
      <p>Hello admin
		<br>The product price with {id} has been changed!!!</p>
		</body>
		</html>
		"""

   message = MessageSchema(
      subject="Fastapi-Mail module",
      # List of recipients, as many as you can pass
      recipients=emails,
      body=template,
      subtype="html"
   )

   fm = FastMail(conf)
   await fm.send_message(message)

   return True
