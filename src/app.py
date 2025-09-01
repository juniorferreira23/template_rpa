import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI

from src.api.schemas import (
    ExampleBotSchema,
    HelloBotSchema,
    Message,
    MessageBot,
)
from src.tasks import hello, run_bot_example

if sys.platform == 'win32':  # pragma: no cover
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Api rodando'}


@app.post('/hello_bot', status_code=HTTPStatus.OK, response_model=MessageBot)
async def run_hello_bot(name: HelloBotSchema):
    message = hello.delay(name)  # type: ignore
    return {
        'task_id': message.id,
        'message': 'Requisição processada com sucesso!',
    }


@app.post('/example_bot', status_code=HTTPStatus.OK, response_model=MessageBot)
async def run_example_bot(headless: ExampleBotSchema):
    message = run_bot_example.delay(headless)  # type: ignore
    return {
        'task_id': message.id,
        'message': 'Requisição processada com sucesso!',
    }
