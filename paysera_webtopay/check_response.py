from .callback_validator import CallbackValidator


class CheckResponse:
    @staticmethod
    def check_response(request_data_dict: dict, projectid: int, sign_password: str):
        data = CallbackValidator(password=sign_password).validate_and_parse_data(request_data_dict, projectid)
        if data['type'] == 'macro' and int(data['status'][0]) != 1:
            raise ValueError('Expected status code 1. Deprecated usage error code {}'.format(11))
        return data
