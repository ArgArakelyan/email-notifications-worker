from faststream.rabbit import RabbitBroker

from app.core.config import config

broker = RabbitBroker(config.rabbitmq.rabbitmq_url)
