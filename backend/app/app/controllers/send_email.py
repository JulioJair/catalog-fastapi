from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List

conf = ConnectionConfig(
    MAIL_FROM="",
    MAIL_USERNAME="",
    MAIL_PASSWORD="",
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
