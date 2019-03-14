class WebToPay:

    def __init__(self):
        pass

    def build_request(self, data: dict) -> object:
        from .request_builder import RequestBuilder
        if not all(key in data for key in
                   ('sign_password', 'projectid')):
            raise ValueError('Data sign_password or projectid missing.')
        data['environment'] = data['environment'] if 'environment' in data.keys() else 'production'
        return RequestBuilder().build_request(data)

    def get_payment_method_list(self, project_id: int, currency: str, environment: str = 'production') -> object:
        from .payment_method_list_provider import PaymentMethodListProvider
        return PaymentMethodListProvider().get_payment_method_list(project_id, currency, environment)

    def check_response(self):
        pass

    # debugging
    def check_sign(self, data: dict) -> bool:
        from hashlib import md5
        data_1 = {
            'data': 'encodedData',
            'ss1': md5(('encodedData' + 'secret').encode()).hexdigest(),
            'ss2': 'bad-ss2'
        }
        import OpenSSL
        import base64
        with open('tests/private.key', 'r') as cert_file_priv:
            cert_text_priv = cert_file_priv.read()
        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, cert_text_priv.encode())
        sign = OpenSSL.crypto.sign(private_key, 'encodedData', "sha1")
        data_2 = {
            'data': 'encodedData',
            'ss1': 'bad-ss1',
            'ss2': base64.b64encode(sign),
        }
        from .ss1_sign_checker import Ss1SignChecker
        from .ss2_sign_checker import Ss2SignChecker
        print(Ss1SignChecker('secret').check_sign(data_1))
        with open('tests/public.key', 'r') as cert_file_pub:
            cert_text_pub = cert_file_pub.read().encode()
        print(Ss2SignChecker(cert_text_pub).check_sign(data_2))
