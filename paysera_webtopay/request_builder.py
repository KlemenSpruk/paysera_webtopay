from hashlib import md5
from urllib.parse import urlencode


class RequestBuilder:

    def __init__(self):
        self._required_request_properties = (
            'orderid',
            'accepturl',
            'cancelurl',
            'callbackurl',
            'amount',
            'currency',
            'paytext',
            'p_firstname',
            'p_lastname',
            'p_email',
            'p_street',
            'p_city',
            'p_state',
            'p_zip',
            'time_limit',
            'sign_password',
            'projectid'
        )

    def build_request(self, data: dict) -> dict:
        self.validate_request(data)
        return self.create_request(data)

    def validate_request(self, request_data: dict) -> None:
        request_properties = request_data.keys()
        for key in self._required_request_properties:
            if key not in request_properties:
                raise ValueError("{} must be present in request data".format(key))

    def create_request(self, request_data: dict) -> dict:
        query_string = urlencode(request_data)
        from .util import encode_safe_url_base64
        string = encode_safe_url_base64(query_string)
        return {
            'data': string,
            'sign': md5(string.encode() + request_data['sign_password'].encode()).hexdigest()
        }
