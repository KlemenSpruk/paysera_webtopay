import unittest
import paysera_webtopay.util


class UtilTest(unittest.TestCase):

    def test_encode(self):
        self.assertEqual('amRmb2dqdWRoZ29kamdvaWRmamd1aGZkZ18va2RnZg==',
                         paysera_webtopay.util.encode_safe_url_base64(
                             "jdfogjudhgodjgoidfjguhfdg_/kdgf"))

        # self.assertEqual("MwABAgMEBZL_qgABAgMEBZL-qu4=", paysera_webtopay.util.encode_safe_url_base64(
        #     "\x33\0\1\2\3\4\5\x92\xFF\xAA\0\1\2\3\4\5\x92\xFE\xAA\xEE"))

    def test_decode(self):
        self.assertEqual(
            paysera_webtopay.util.decode_safe_url_base64('amRmb2dqdWRoZ29kamdvaWRmamd1aGZkZ18va2RnZg==').decode(),
            "jdfogjudhgodjgoidfjguhfdg_/kdgf")
        # self.assertEqual("\x33\0\1\2\3\4\5\x92\xFF\xAA\0\1\2\3\4\5\x92\xFE\xAA\xEE",
        #                  paysera_webtopay.util.decode_safe_url_base64('MwABAgMEBZL_qgABAgMEBZL-qu4='))
        # self.assertEqual("\x33\0\1\2\3\4\5\x92\xFF\xAA\0\1\2\3\4\5\x92\xFE\xAA\xEE",
        #                  paysera_webtopay.util.decode_safe_url_base64('MwABAgMEBZL/qgABAgMEBZL+qu4='))

    def test_encode_decode(self):
        strings = (
            'Some long string with UTF-8 ąččėę проверка',
            "Some binary symbols \0\1\3\xFF\xE0\xD0\xC0\xB0\xA0\x90\x10\x0A ",
            'Some other symbols %=?/-_)22Wq')
        for s in strings:
            self.assertEqual(s,
                             paysera_webtopay.util.decode_safe_url_base64(
                                 paysera_webtopay.util.encode_safe_url_base64(s)).decode()
                             )

    def test_parse_http_query(self):
        self.assertEqual({
            'param1': ['some string'],
            'param2': ['special symbols !!%(@_-+/='],
            'param3': ['slashes \\\'"'],
        }, paysera_webtopay.util.parse_http_query(
            'param1=some+string&param2=special+symbols+%21%21%25%28%40_-%2B%2F%3D&param3=slashes+%5C%27%22'))


if __name__ == "main":
    unittest.main()
