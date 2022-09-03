import requests
from loguru import logger
from exceptions import RequestError


class HttpRequestMaker:
    @staticmethod
    def send_get_request(url) -> requests.Response:
        request = requests.get(url)
        if request.status_code == 200:
            return request
        else:
            logger.warning(f'Error {request.status_code=}')
            raise RequestError(request.status_code)
