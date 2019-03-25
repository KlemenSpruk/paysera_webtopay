from .configuration import configuration
from .web_client import WebClient
from hashlib import md5


class SmsAnswerSender:
    def __init__(self, sign_password: str, environment: str = 'production'):
        self._password = sign_password
        self._environment = environment

    def send_answer(self, sms_id: int, text:str):
        content: str = WebClient().get(configuration['routes'][self._environment]['sms_answer'], {
            'id': sms_id,
            'msg': text,
            'transaction': md5((self._password + '|' + str(sms_id)).encode())
        }).decode()

        if not content.startswith('OK'):
            raise Exception('Error {}'.format(content))

