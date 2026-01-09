from app.core.broker import broker
from app.core.config import config
from app.models import ResetPasswordMessage
from app.service import (EmailNotificationService,
                         get_email_notification_service)

email_notification_service: EmailNotificationService = get_email_notification_service()

import logging

logger = logging.getLogger(__name__)


@broker.subscriber(config.queues.reset_password)
async def handle_reset_password(msg: ResetPasswordMessage):
    result = await email_notification_service.send_reset_password(
        msg.email, msg.reset_code
    )

    if not result:
        raise ValueError("Email sending failed")

    return result
