import unittest
from hashlib import md5

from paysera_webtopay.ss1_sign_checker import Ss1SignChecker


class Ss1SignCheckerTest(unittest.TestCase):
    def test_check_sign_ss1(self):
        data = {
            'data': 'encodedData',
            'ss1': md5(('encodedData' + 'secret').encode()).hexdigest(),
            'ss2': 'bad-ss2'
        }
        self.assertTrue(Ss1SignChecker('secret').check_sign(data))


if __name__ == "main":
    unittest.main()
