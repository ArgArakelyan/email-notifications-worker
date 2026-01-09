import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import config
from app.templates.reset_password import reset_template

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

    async def send_reset_password(self, to_email: str, reset_code: str):
        try:
            subject = f"Сброс пароля • Код: {reset_code}"

            html_body = self.reset_template.render(reset_code=reset_code)

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


def get_email_notification_service() -> EmailNotificationService:
    return EmailNotificationService()
