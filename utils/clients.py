import logging

from aiohttp import ClientSession
from uplink import Consumer, get, json, returns, timeout

from utils.middleware import CORRELATION_ID_HEADER_KEY, correlation_id_context


class CorrelationIDAwareAioHttpClientSession(ClientSession):
    """CorrelationIDAwareAioHttpClientSession

    This is a custom aiohttp ClientSession with integrated CorrelationID control.
    """

    async def _request(self, method, url, **kwargs):
        headers = kwargs.get("headers", {})

        if CORRELATION_ID_HEADER_KEY not in headers:
            correlation_id = correlation_id_context.get()
            headers.update({CORRELATION_ID_HEADER_KEY: correlation_id})
            kwargs.update({"headers": headers})

        logging.debug(f"CorrelationIDAwareAioHttpClientSession request called with headers: {kwargs.get('headers', {})}")
        return await super()._request(method, url, **kwargs)


class CorrelationIDAwareUplinkConsumer(Consumer):
    """CorrelationIDAwareUplinkConsumer

    This is a custom uplink Consumer with integrated CorrelationID control.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # headers = kwargs.get("headers", {})

        if CORRELATION_ID_HEADER_KEY not in self.session.headers:
            correlation_id = correlation_id_context.get()
            self.session.headers.update({CORRELATION_ID_HEADER_KEY: correlation_id})
            logging.debug(f"CorrelationIDAwareUplinkConsumer updated with headers: {self.session.headers}")


    @json
    @timeout(5)
    @returns.json
    @get("https://jsonplaceholder.typicode.com/users")
    def get_external_data(self):
        pass  # pragma: no cover

