from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
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


async def send_email_async(subject: str, emails_to: list, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=emails_to,
        body=body,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


def send_email_background(background_tasks: BackgroundTasks, subject: str, emails_to: list, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=emails_to,
        body=body,
        subtype='html',
    )
    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message, message, template_name='email.html')
