import logging
import uuid

from aiohttp import ClientSession
from fastapi import FastAPI, Request

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)-9s %(message)s',
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    original_request_id = request.headers.get("X-Request-Id")
    logging.info(f"DEBUG The original_request_id is {original_request_id}")
    request_id = uuid.uuid4() if original_request_id is None else original_request_id

    if original_request_id is None:
        # request.headers["X-Request-Id"] = request_id
        request.headers.__dict__["_list"].append(
            (
                "x-request-id".encode(),
                str(request_id).encode()
            )
        )

    logging.info(f"DEBUG The request_id is now {request.headers.get('X-Request-Id')}")

    try:
        logging.info(f"[{request_id}] Start request path={request.url.path}")
        response = await call_next(request)
        return response

    except Exception as e:
        logging.error(f"[{request_id}] Unhandled Exception during request: {type(e)} {e}")


@app.get("/route_one")
async def route_one(request: Request):
    logging.info("Logging from route_one()")

    http_client = ClientSession(raise_for_status=False)

    async with await http_client.get(
            url="http://127.0.0.1:8000/route_two",
            headers={"X-Request-Id": f"{request.headers.get('X-Request-Id')}"}
    ) as r:
        response = await r.json()

    await http_client.close()

    return {"status": f"{response}"}


@app.get("/route_two")
def route_two():
    logging.info("Logging from route_two()")
    return True
