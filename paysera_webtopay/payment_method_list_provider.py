import xmltodict
from .util import get_configuration
from .web_client import WebClient
from .payment_method import PaymentMethod


class PaymentMethodListProvider:

    def get_payment_method_list(self, projectid: int, currency: str, amount_in_cents: int, desired_language: str,
                                environment: str) -> dict:
        result_dict = {
            'project_id': projectid,
            'currency': currency,
            'amount_in_cents': amount_in_cents,
            'language': desired_language
        }
        url = "{}{}/currency:{}/amount:{}/language:{}".format(get_configuration(environment).get('payment_method_list'),
                                                              projectid, currency, amount_in_cents, desired_language)

        xml_string = WebClient().get(url).decode()
        xml_dict_object = xmltodict.parse(xml_string)
        for country in xml_dict_object['payment_types_document']['country']:
            result_dict[country['@code']] = {
                'country_code': country['@code'],
                'title': country['title']['#text'] if '#text' in country['title'].keys() else None,
                'payments': self._process_payments(country['payment_group'], desired_language),
            }
        return result_dict

    def _process_payments(self, data: dict, language: str) -> list:
        result = []

        for payment in data:
            if isinstance(payment['payment_type'], list):
                for nested_payment in payment['payment_type']:
                    result.append(self._create_payment_method(nested_payment, language,
                                                              payment['title']['#text'] if (
                                                                      'title' in payment and '#text' in
                                                                      payment['title']) else None))
            else:
                result.append(self._create_payment_method(payment['payment_type'], language,
                                                          payment['title']['#text'] if (
                                                                  'title' in payment and '#text' in
                                                                  payment['title']) else None))

        return result

    @staticmethod
    def _create_payment_method(payment: dict, language: str, group: str) -> dict:
        min_amount = payment['min']['@amount'] if 'min' in payment else None
        currency = payment['min']['@currency'] if 'min' in payment else None
        max_amount = payment['max']['@amount'] if 'max' in payment else None
        if currency is None:
            currency = payment['max']['@currency'] if 'max' in payment else None

        return PaymentMethod(
            key=payment['@key'] if '@key' in payment else None,
            min_amount_in_cents=min_amount,
            max_amount_in_cents=max_amount,
            currency=currency,
            logo_list={language: payment['logo_url']['#text']} if 'logo_url' in payment else None,
            title_translations={language: payment['title']['#text']} if 'title' in payment else None,
            default_language='',
            is_iban=bool(
                payment['is_iban'] if 'is_iban' in payment else None),
            base_currency=payment['base_currency'] if 'base_currency' in payment else None,
            group=group
        ).to_dictionary(language)
