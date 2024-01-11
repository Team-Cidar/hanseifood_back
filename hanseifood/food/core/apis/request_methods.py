import requests
from requests import Response


class APIRequests:
    @staticmethod
    def get(url: str, headers: dict = None) -> Response:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response

    @staticmethod
    def post(url: str, headers: dict = None, body: dict = None) -> Response:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        return response
