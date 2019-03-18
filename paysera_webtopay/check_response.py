from .callback_validator import CallbackValidator


class CheckResponse:
    @staticmethod
    def check_response(request_data_dict: dict, user_data: dict):
        data = CallbackValidator().validate_and_parse_data({**request_data_dict, **user_data})
        if data['type'] == 'macro' and data['status'] != 1:
            raise ValueError('Expected status code 1. Deprecated usage error code {}'.format(11))
        return data
