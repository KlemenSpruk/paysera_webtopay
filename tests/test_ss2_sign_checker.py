import unittest
import base64
import OpenSSL
from paysera_webtopay.ss2_sign_checker import Ss2SignChecker


class Ss2SignCheckerTest(unittest.TestCase):
    def test_check_sign_ss2(self):
        with open('private.key', 'r') as cert_priv:
            cert_text_priv = cert_priv.read()
        cert_priv.close()

        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, cert_text_priv.encode())
        sign = OpenSSL.crypto.sign(private_key, 'encodedData', "sha1")
        data = {
            'data': 'encodedData',
            'ss1': 'bad-ss1',
            'ss2': base64.b64encode(sign),
        }
        with open('public.key', 'r') as cert_pub:
            cert_text_pub = cert_pub.read()
        cert_pub.close()
        self.assertTrue(Ss2SignChecker(cert_text_pub).check_sign(data))


if __name__ == "main":
    unittest.main()
