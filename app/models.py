from pydantic import BaseModel


class ResetPasswordMessage(BaseModel):
    user_id: int
    email: str
    reset_code: str
