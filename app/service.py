import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import config
from app.templates.reset_password import reset_template
from app.templates.verification_code import verificaton_template

logger = logging.getLogger(__name__)


class EmailNotificationService:
    def __init__(self):
        self.smtp_host = config.email.smtp_host
        self.smtp_port = config.email.smtp_port
        self.smtp_user = config.email.smtp_user
        self.smtp_password = config.email.smtp_password
        self.from_email = config.email.from_email
        self.from_name = config.email.from_name

        # templates
        self.reset_template = reset_template
        self.account_verification_template = verificaton_template

    async def send_from_template(self, to_email, html_body, subject):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            html_part = MIMEText(html_body, "html", "utf-8")
            msg.attach(html_part)

            await aiosmtplib.send(
                msg,
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=False,
                username=self.smtp_user,
                password=self.smtp_password,
                validate_certs=True,
            )

            return True
        except Exception as e:
            logger.error("Failed to send email notification", extra={"error": str(e), "smtp_port": self.smtp_port, "to_email": to_email})
            return False

    async def send_reset_password(self, to_email: str, reset_code: str):
        html_body = self.reset_template.render(reset_code)
        subject = f"Ваш код для сброса пароля"
        return await self.send_from_template(to_email=to_email, html_body=html_body, subject=subject)

    async def send_account_verification_code(self, to_email: str, code: str):
        html_body = self.account_verification_template.render(code=code)
        subject = "Ваш код для подтверждения аккаунта"
        return await self.send_from_template(to_email=to_email, html_body=html_body, subject=subject)



def get_email_notification_service() -> EmailNotificationService:
    return EmailNotificationService()
