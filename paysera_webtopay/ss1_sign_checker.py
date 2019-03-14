from hashlib import md5

class Ss1SignChecker:
    def __init__(self, sign_password: str):
        self._project_password = sign_password

    def check_sign(self, data_dict: dict):
        if not all(key in data_dict for key in
                   ('data', 'ss1')):
            raise ValueError('Not enough parameters in callback. Possible version mismatch.')
        return md5((data_dict['data'] + self._project_password).encode()).hexdigest() == data_dict['ss1']
