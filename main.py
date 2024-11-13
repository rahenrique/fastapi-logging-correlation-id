import logging
from logging.config import dictConfig

from aiohttp import ClientSession
from fastapi import FastAPI, Depends, Request
from uplink import Consumer

from utils.clients import CorrelationIDAwareAioHttpClientSession, CorrelationIDAwareUplinkConsumer
from utils.logger_configuration import LOGGING_CONFIG
from utils.middleware import CorrelationIdMiddleware

app = FastAPI()


@app.on_event("startup")
async def startup():
    """FastAPI startup

    Configure logger; and
    Initialize HTTP Client sessions
    """
    dictConfig(LOGGING_CONFIG)
    setattr(app.state, "aiohttp_http_client", CorrelationIDAwareAioHttpClientSession(raise_for_status=False))
    setattr(app.state, "uplink_http_client", CorrelationIDAwareUplinkConsumer())


@app.on_event("shutdown")
async def shutdown():
    """FastAPI shutdown
    Closes HTTP Client sessions
    """
    await app.state.aiohttp_http_client.close()
    # await asyncio.wait((app.state.aiohttp_http_client.close()), timeout=5.0)


def get_aiohttp_http_client(request: Request) -> ClientSession:
    """Get an instance of an aiohttp ClientSession"""
    return request.app.state.aiohttp_http_client


def get_uplink_http_client(request: Request) -> Consumer:
    """Get an instance of an uplink Consumer"""
    return request.app.state.uplink_http_client


app.add_middleware(CorrelationIdMiddleware)


@app.get("/route_one")
async def route_one(aiohttp_http_client: ClientSession = Depends(get_aiohttp_http_client)):
    logging.info("Logging from route_one()")
    logging.info("Using an aiohttp ClientSession")

    async with await aiohttp_http_client.get(
            url="http://127.0.0.1:8000/route_two",
            headers={"X-Custom": "123"},
    ) as r:
        response = await r.json()

    return {"data": response}


@app.get("/route_two")
async def route_two(aiohttp_http_client: ClientSession = Depends(get_aiohttp_http_client)):
    logging.info("Logging from route_two()")
    logging.info("Using an aiohttp ClientSession")

    async with await aiohttp_http_client.get(
            url="http://127.0.0.1:8000/route_three",
            headers={"X-Custom": "456"},
    ) as r:
        response = await r.json()

    return {"data": response}


@app.get("/route_three")
async def route_three(uplink_http_client: Consumer = Depends(get_uplink_http_client)):
    logging.info("Logging from route_three()")
    logging.info("Using an uplink Consumer")

    response = uplink_http_client.get_external_data()
    return {"data": response}
