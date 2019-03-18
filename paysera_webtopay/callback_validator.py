import requests
from .util import get_configuration
from .ss1_sign_checker import Ss1SignChecker
from .ss2_sign_checker import Ss2SignChecker
from .util import decode_safe_url_base64, parse_http_query


class CallbackValidator:

    def __init__(self, environment: str = 'production', password: str = ''):
        self._environment = environment
        self._password = password

    @staticmethod
    def _generate_request(data:str):
        return parse_http_query(decode_safe_url_base64(data))

    def validate_and_parse_data(self, request_data_dict: dict) -> dict:
        signer = self.get_signer()
        if not signer.check_sign(request_data_dict):
            raise Exception('Invalid sign parameters, check $_GET length limit')
        request_keys = request_data_dict.keys()
        request = self._generate_request(request_data_dict['data'])
        if 'projectid' not in request_keys:
            raise ValueError('Project ID not provided in callback')
        # @todo: check what request really returns
        print(request, request_data_dict)
        if request['projectid'] != request_data_dict['projectid']:
            raise ValueError(
                'Bad projectid: {}, should be: {}'.format(request['projectid'][0], request_data_dict['projectid']))
        if 'type' not in request_keys or request['type'][0] not in ('micro', 'macro'):
            micro = True if 'to' in request_keys and 'from' in request_keys and 'sms' in request_keys else False
            request['type'] = 'micro' if micro else 'macro'
        return request

    def get_signer(self):
        def check_public_ssl_key(url: str):
            response = requests.get(url)
            return response.content if response.status_code == 200 else None

        public_ssl_key_url = get_configuration(self._environment)['public_key']
        ssl_public_key = check_public_ssl_key(public_ssl_key_url)
        return Ss2SignChecker(ssl_public_key) if ssl_public_key else Ss1SignChecker(self._password)
