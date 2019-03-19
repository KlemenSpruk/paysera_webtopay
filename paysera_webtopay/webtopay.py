class WebToPay:

    def __init__(self):
        pass

    def build_request(self, data: dict) -> object:
        from .request_builder import RequestBuilder
        if not all(key in data for key in
                   ('sign_password', 'projectid')):
            raise ValueError('Data sign_password or projectid missing.')
        data['environment'] = data['environment'] if 'environment' in data.keys() else 'production'
        return RequestBuilder().build_request(data)

    @staticmethod
    def get_payment_method_list(project_id: int, amount_in_cents: int, currency: str = 'EUR',
                                desired_language: str = 'en', environment: str = 'production') -> object:
        from .payment_method_list_provider import PaymentMethodListProvider
        return PaymentMethodListProvider().get_payment_method_list(project_id, currency, amount_in_cents,
                                                                   desired_language, environment)

    def check_response(self, get_request_data: dict, user_data: dict):
        from .check_response import CheckResponse
        # user_data = {
        #     'projectid': 1573,
        #     'sign_password': 'c7431195329e44d39065263cf14ae642',
        # }
        # get_request_data = {
        #     'sign_password': 'c7431195329e44d39065263cf14ae642', 'projectid': 1573,
        #     'orderid': 11337, 'lang': 'ENG', 'payment': 'paysera', 'p_firstname': 'Klemen',
        #     'p_lastname': 'VelisCompany', 'p_email': 'spruk.klemen@gmail.com',
        #     'p_street': 'Jelovška 24', 'p_city': 'Radovlica', 'p_state': 'Slovenia',
        #     'p_zip': '4240', '__plan': '3', 'data': 'sdgsgsd', 'sign': 'c7431195329e44d39065263cf14ae642'}
        return CheckResponse().check_response(get_request_data, user_data)
