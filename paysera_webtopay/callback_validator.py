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
    def _generate_request(data: str):
        return parse_http_query(decode_safe_url_base64(data).decode())

    def validate_and_parse_data(self, request_data_dict: dict, projectid: int) -> dict:
        signer = self.get_signer()
        if not signer.check_sign(request_data_dict):
            raise Exception('Invalid sign parameters, check $_GET length limit')
        request_keys = request_data_dict.keys()
        request = self._generate_request(request_data_dict['data'])
        if projectid is None or type(projectid) is not int:
            raise ValueError('Project ID not provided in callback')
        # @todo: check what request really returns
        if int(request['projectid'][0] if isinstance(request['projectid'], list) else request[
            'projectid']) != projectid:
            raise ValueError(
                'Bad projectid: {}, should be: {}'.format(
                    request['projectid'][0] if isinstance(request['projectid'], list) else request[
                        'projectid'], projectid))
        if 'type' not in request_keys or request['type'][0] not in ('micro', 'macro'):
            micro = True if 'to' in request_keys and 'from' in request_keys and 'sms' in request_keys else False
            request['type'] = 'micro' if micro else 'macro'
        return request

    def get_signer(self):
        def check_and_get_public_ssl_key(url: str):
            response = requests.get(url)
            return response.content if response.status_code == 200 else None

        public_ssl_key_url = get_configuration(self._environment)['public_key']

        ssl_public_key_check = check_and_get_public_ssl_key(public_ssl_key_url)
        if ssl_public_key_check is None:
            return Ss1SignChecker(self._password)
        ssl_public_key = self.get_public_key(ssl_public_key_check)
        return Ss2SignChecker(ssl_public_key)

    @staticmethod
    def get_public_key(cert_or_key_text: bytes) -> bytes:
        if 'key' in cert_or_key_text.lower().decode():
            return cert_or_key_text
        import OpenSSL
        certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_or_key_text)
        pub_key_object = certificate.get_pubkey()
        return OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, pub_key_object)
