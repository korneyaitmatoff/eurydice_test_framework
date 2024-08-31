from typing import Any
from requests import Response, request
from loguru import logger


class BaseApi:
    """Base class for api"""
    url: str
    service_name = str

    def request(self, method: str, params: Any = None, headers: dict[str, Any] = None, path: str = "/") -> Response:
        """Method-layer for send request"""
        logger.debug(f"Send {method} request to {self.url}/{path} with params {str(params)}")

        response = request(
            method=method,
            url=f"{self.url}/{path}",
            headers=headers,
            params=params
        )

        logger.debug((
            f"Receive response from {self.url}/{path}\n"
            f"Status code: {response.status_code}\n"
            f"Headers: {response.headers}\n"
            f"Text: {response.text}\n"
        ))

        return response
