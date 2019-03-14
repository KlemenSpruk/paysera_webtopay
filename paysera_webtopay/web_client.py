from urllib.parse import urlencode
import requests


class WebClient:

    @staticmethod
    def get(uri: str, query_data=None) -> str:
        if query_data is None:
            query_data = {}
        uri += urlencode(query_data)
        response = requests.get(uri)
        return response.content
