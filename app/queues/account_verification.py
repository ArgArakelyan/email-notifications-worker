from app.core.broker import broker
from app.core.config import config
from app.models import AccountVerificationMessage
from app.service import (EmailNotificationService,
                         get_email_notification_service)

email_notification_service: EmailNotificationService = get_email_notification_service()

import logging

logger = logging.getLogger(__name__)


@broker.subscriber(config.queues.account_verification)
async def handle_reset_password(msg: AccountVerificationMessage):
    result = await email_notification_service.send_account_verification_code(
        msg.email, msg.code
    )

    if not result:
        raise ValueError("Email sending failed")

    return result
