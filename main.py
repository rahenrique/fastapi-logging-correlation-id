import logging
from logging.config import dictConfig

from aiohttp import ClientSession
from fastapi import FastAPI, Depends, Request

from utils.client import CorrelationIDAwareClientSession
from utils.logger_configuration import LOGGING_CONFIG
from utils.middleware import CorrelationIdMiddleware

app = FastAPI()


@app.on_event("startup")
async def startup():
    """FastAPI startup

    Initialize Async HTTP Client session
    Configure logger
    """
    dictConfig(LOGGING_CONFIG)
    setattr(app.state, "http_client", CorrelationIDAwareClientSession(raise_for_status=False))


@app.on_event("shutdown")
async def shutdown():
    """FastAPI shutdown
    Closes Async HTTP Client session
    """
    await app.state.http_client.close()
    # await asyncio.wait((app.state.http_client.close()), timeout=5.0)


def get_http_client(request: Request) -> ClientSession:
    """Get an instance of an Async HTTP Client"""
    return request.app.state.http_client


app.add_middleware(CorrelationIdMiddleware)


@app.get("/route_one")
async def route_one(http_client: ClientSession = Depends(get_http_client)):
    logging.info("Logging from route_one()")

    async with await http_client.get(
            url="http://127.0.0.1:8000/route_two",
            headers={"X-Custom": "123"},
    ) as r:
        response = await r.json()

    return {"data": f"{response}"}


@app.get("/route_two")
async def route_two(http_client: ClientSession = Depends(get_http_client)):
    logging.info("Logging from route_two()")

    async with await http_client.get(
            url="http://127.0.0.1:8000/route_three",
            headers={"X-Custom": "123"},
    ) as r:
        response = await r.json()

    return {"status": f"{response}"}


@app.get("/route_three")
def route_three():
    logging.info("Logging from route_three()")
    return True
