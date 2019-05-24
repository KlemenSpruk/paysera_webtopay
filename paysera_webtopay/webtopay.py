class WebToPay:

    @staticmethod
    def build_request(data: dict) -> dict:
        from .request_builder import RequestBuilder
        if not all(key in data for key in
                   ('sign_password', 'projectid')):
            raise KeyError('Data sign_password or projectid missing.')
        data['environment'] = data['environment'] if 'environment' in data.keys() else 'production'
        return RequestBuilder().build_request(data)

    @staticmethod
    def get_payment_method_list(project_id: int, amount_in_cents: int, currency: str = 'EUR',
                                desired_language: str = 'en', environment: str = 'production') -> dict:
        from .payment_method_list_provider import PaymentMethodListProvider
        return PaymentMethodListProvider().get_payment_method_list(project_id, currency, amount_in_cents,
                                                                   desired_language, environment)

    @staticmethod
    def check_response(get_request_data: dict, projectid: int, sign_password: str) -> dict:
        from .check_response import CheckResponse
        response = CheckResponse().check_response(get_request_data, projectid, sign_password)
        return response

    @staticmethod
    def sms_answer(data: dict) -> None:
        if not all(key in data for key in ('id', 'msg', 'sign_password')):
            raise KeyError('id, msg and sign_password are required')
        from .sms_answer_sender import SmsAnswerSender
        SmsAnswerSender(str(data.get('sign_password'))).send_answer(int(data.get('id')), str(data.get('msg')))

    @staticmethod
    def get_public_pay_url(environment: str = 'production') -> str:
        from .configuration import configuration
        return configuration['routes'][environment]['payment']
