import OpenSSL
from paysera_webtopay.util import decode_safe_url_base64


class Ss2SignChecker:
    def __init__(self, public_key: str):
        self._public_key = public_key

    def check_sign(self, data_dict: dict):
        if not all(key in data_dict for key in
                   ('data', 'ss2')):
            raise ValueError('Not enough parameters in callback. Possible version mismatch.')
        pub_key_object = OpenSSL.crypto.load_publickey(OpenSSL.crypto.FILETYPE_PEM, self._public_key)
        x509 = OpenSSL.crypto.X509()
        x509.set_pubkey(pub_key_object)

        check = OpenSSL.crypto.verify(x509,
                                      decode_safe_url_base64(data_dict['ss2']), data_dict['data'], "sha1")
        return check is None
