import asyncio

from faststream import FastStream

import app.queues.reset_password as reset_password # noqa
import app.queues.account_verification as account_verification # noqa
from app.core.broker import broker
from app.core.log import setup_logging

app = FastStream(broker)


setup_logging()


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
