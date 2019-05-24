import unittest
from unittest.mock import Mock
from paysera_webtopay.ss1_sign_checker import Ss1SignChecker
from paysera_webtopay.ss2_sign_checker import Ss2SignChecker
from paysera_webtopay.callback_validator import CallbackValidator

projectid = 123

parsed = {
    'projectid': projectid,
    'someparam': 'qwerty123',
    'type': 'micro'
}


class CallBackValidatorTest(unittest.TestCase):
    Ss1SignChecker.check_sign = Mock(return_value=True)
    Ss2SignChecker.check_sign = Mock(return_Value=True)
    CallbackValidator._generate_request = Mock(return_value=parsed)

    def test_validate_and_parse_data(self):
        request = {
            'data': 'abcdef',
            'sign': 'qwerty'
        }

        self.assertEqual(
            parsed,
            CallbackValidator(password='qwerty').validate_and_parse_data({**request, **parsed},
                                                                         projectid)
        )


if __name__ == "main":
    unittest.main()
