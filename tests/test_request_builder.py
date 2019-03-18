import unittest
from paysera_webtopay.request_builder import RequestBuilder


class RequestBuilderTest(unittest.TestCase):
    def test_build_request(self):
        request_data = {
            'orderid': 123,
            'accepturl': 'http://local.test/',
            'cancelurl': 'http://local.test/',
            'callbackurl': 'http://local.test/',
            'amount': 100,
            'some-other-parameter': 'abc',
            'lang': 'ENG',
            'currency': '',
            'payment': '',
            'country': '',
            'paytext': '',
            'p_firstname': '',
            'p_lastname': '',
            'p_email': '',
            'p_street': '',
            'p_city': '',
            'p_state': '',
            'p_zip': '',
            'p_countrycode': '',
            'test': '',
            'time_limit': '',
            'sign_password': 'encodedsecret',
            'projectid': 686
        }

        self.assertEqual({
            'data': 'b3JkZXJpZD0xMjMmYWNjZXB0dXJsPWh0dHAlM0ElMkYlMkZsb2NhbC50ZXN0JTJGJmNhbmNlbHVybD1odHRwJTNBJTJGJTJGbG9jYWwudGVzdCUyRiZjYWxsYmFja3VybD1odHRwJTNBJTJGJTJGbG9jYWwudGVzdCUyRiZhbW91bnQ9MTAwJnNvbWUtb3RoZXItcGFyYW1ldGVyPWFiYyZsYW5nPUVORyZjdXJyZW5jeT0mcGF5bWVudD0mY291bnRyeT0mcGF5dGV4dD0mcF9maXJzdG5hbWU9JnBfbGFzdG5hbWU9JnBfZW1haWw9JnBfc3RyZWV0PSZwX2NpdHk9JnBfc3RhdGU9JnBfemlwPSZwX2NvdW50cnljb2RlPSZ0ZXN0PSZ0aW1lX2xpbWl0PSZzaWduX3Bhc3N3b3JkPWVuY29kZWRzZWNyZXQmcHJvamVjdGlkPTY4Ng==',
            'sign': '3c846d70cf23bffff8cf2cb742b77d3b'}, RequestBuilder().build_request(request_data))
