import logging
from aiohttp import ClientSession
from utils.middleware import CORRELATION_ID_HEADER_KEY, correlation_id_context

class CorrelationIDAwareClientSession(ClientSession):
    """CorrelationIDAwareClientSession

    This is a custom ClientSession with integrated CorrelationID control.
    """

    async def _request(self, method, url, **kwargs):
        headers = kwargs.get("headers", {})
        
        if CORRELATION_ID_HEADER_KEY not in headers:
            correlation_id = correlation_id_context.get()
            headers.update({CORRELATION_ID_HEADER_KEY: correlation_id})
            kwargs.update({"headers": headers})
        
        logging.debug(f"Request called with headers: {kwargs.get('headers', {})}")
        return await super()._request(method, url, **kwargs)
