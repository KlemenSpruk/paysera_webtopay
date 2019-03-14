from hashlib import md5
from urllib.parse import urlencode
import base64


class RequestBuilder:

    def __init__(self):
        self._required_request_properties = (
            'orderid',
            'accepturl',
            'cancelurl',
            'callbackurl',
            'lang',
            'amount',
            'currency',
            'payment',
            'country',
            'paytext',
            'p_firstname',
            'p_lastname',
            'p_email',
            'p_street',
            'p_city',
            'p_state',
            'p_zip',
            'p_countrycode',
            'test',
            'time_limit',
            'sign_password',
            'projectid'
        )

    def build_request(self, data: dict):
        self.validate_request(data)
        return self.create_request(data)

    def validate_request(self, request_data: dict) -> None:
        request_properties = request_data.keys()
        for key in self._required_request_properties:
            if key not in request_properties:
                raise ValueError("{} must be present in request data".format(key))

    def create_request(self, request_data: dict) -> dict:
        query_string = urlencode(request_data)
        encoded_bytes = base64.b64encode(query_string.encode())
        string = encoded_bytes.decode().replace('+', '-').replace('/', '_')
        return {
            'data': string,
            'sign': md5((string + request_data['sign_password']).encode()).hexdigest()
        }
