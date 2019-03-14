class WebToPay:

    def __init__(self):
        pass

    def build_request(self, data: dict) -> object:
        from .request_builder import RequestBuilder
        import collections
        data = collections.OrderedDict([
            ('sign_password', 'c7431195329e44d39065263cf14ae642'),
            ('projectid', 1573),
            ('orderid', 2438),
            ('accepturl', ''),
            ('cancelurl', ''),
            ('callbackurl', ''),
            ('lang', ''),
            ('amount', 1),
            ('currency', 'EUR'),
            ('payment', 'paysera'),
            ('country', 'SI'),
            ('paytext', ''),
            ('p_firstname', 'Klemen'),
            ('p_lastname', 'Špruk'),
            ('p_email', 'spruk.klemen@gmail.com'),
            ('p_street', ''),
            ('p_city', ''),
            ('p_state', ''),
            ('p_zip', ''),
            ('p_countrycode', ''),
            ('test', ''),
            ('time_limit', '')])

        if not all(key in data for key in
                   ('sign_password', 'projectid')):
            raise ValueError('Data sign_password or projectid missing.')
        data['environment'] = data['environment'] if 'environment' in data.keys() else 'production'
        return RequestBuilder().build_request(data)

    def get_payment_method_list(self, project_id: int, currency: str, environment: str = 'production') -> object:
        from .payment_method_list_provider import PaymentMethodListProvider
        return PaymentMethodListProvider().get_payment_method_list(project_id, currency, environment)
