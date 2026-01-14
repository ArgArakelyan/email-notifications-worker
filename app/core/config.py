from pydantic import Field
from pydantic_settings import BaseSettings


class EmailConfig(BaseSettings):
    smtp_host: str = ""
    smtp_port: str = ""
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = ""
    from_name: str = ""

    model_config = {"env_prefix": "EMAIL_", "extra": "ignore"}


class RabbitConfig(BaseSettings):
    host: str = "rabbitmq"
    port: int = 5672
    user: str = "guest"
    password: str = "guest"
    vhost: str = ""

    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"
        )

    model_config = {"env_prefix": "RABBITMQ_", "extra": "ignore"}


class QueuesConfig(BaseSettings):
    reset_password: str = "email.reset_password"
    account_verification: str = "email.account_verification"

    model_config = {"env_prefix": "QUEUE_", "extra": "ignore"}


class Config(BaseSettings):
    email: EmailConfig = Field(default_factory=EmailConfig)
    rabbitmq: RabbitConfig = Field(default_factory=RabbitConfig)
    queues: QueuesConfig = Field(default_factory=QueuesConfig)


config = Config()
