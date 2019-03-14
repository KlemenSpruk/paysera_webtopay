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

    def get_payment_method_list(self, project_id: int, currency: str, environment: str = 'production') -> object:
        from .payment_method_list_provider import PaymentMethodListProvider
        return PaymentMethodListProvider().get_payment_method_list(project_id, currency, environment)

    def check_response(self):
        pass
