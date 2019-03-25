class WebToPay:

    @staticmethod
    def build_request(data: dict) -> object:
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
        # if int(response['test'][0]) != 0:
        #     raise Exception('Testing, real payment was not made')
        # if str(response['type'][0]) != 'macro':
        #     raise Exception('Only macro payment callbacks are accepted')
        return response

    @staticmethod
    def sms_answer(data: dict):
        if not all(key in data for key in ('id', 'msg', 'sign_password')):
            raise KeyError('id, msg and sign_password are required')
        from .sms_answer_sender import SmsAnswerSender
        SmsAnswerSender(str(data.get('sign_password'))).send_answer(int(data.get('id')), str(data.get('msg')))
