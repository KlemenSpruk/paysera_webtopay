import OpenSSL
import base64


class Ss2SignChecker:
    def __init__(self, public_key: bytes):
        self._public_key = public_key

    def check_sign(self, data_dict: dict):
        if not all(key in data_dict for key in
                   ('data', 'ss2')):
            raise ValueError('Not enough parameters in callback. Possible version mismatch.')
        pub_key_object = OpenSSL.crypto.load_publickey(OpenSSL.crypto.FILETYPE_PEM, self._public_key)
        check = OpenSSL.crypto.verify(pub_key_object,
                                      base64.b64decode(data_dict['ss2']), data_dict['data'], "sha1")

        return check
