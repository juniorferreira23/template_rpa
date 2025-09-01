from pydantic import BaseModel


class Message(BaseModel):
    message: str


class MessageBot(Message):
    task_id: str


class HelloBotSchema(BaseModel):
    name: str


class ExampleBotSchema(BaseModel):
    headless: bool
