import json
import xmltodict
from .util import get_configuration
from .web_client import WebClient
from .payment_method import PaymentMethod


class PaymentMethodListProvider:

    def get_payment_method_list(self, projectid: int, currency: str, amount_in_cents: int, desired_language: str,
                                environment: str) -> str:
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
                'payments': self._process_payments(country['payment_group']),
            }
        file = open('tmp.txt', 'w')
        file.write(json.dumps(result_dict))
        file.close()
        return json.dumps(result_dict)

    @staticmethod
    def _process_payments(data: dict) -> list:
        result = []
        for payment in data:
            min_amount = payment['payment_type']['min']['@amount'] if 'min' in payment['payment_type'] else None
            currency = payment['payment_type']['min']['@currency'] if 'min' in payment['payment_type'] else None
            max_amount = payment['payment_type']['max']['@amount'] if 'max' in payment['payment_type'] else None
            if currency is None:
                currency = payment['payment_type']['max']['@currency'] if 'max' in payment[
                    'payment_type'] else None

            result.append(PaymentMethod(
                key=payment['payment_type']['@key'] if '@key' in payment['payment_type'] else None,
                min_amount=min_amount,
                max_amount=max_amount,
                currency=currency,
                logo_list=[payment['payment_type']['logo_url']['#text']] if 'logo_url' in payment[
                    'payment_type'] else None,
                title_translations=[payment['payment_type']['title']['#text']] if 'title' in payment[
                    'payment_type'] else None,
                default_language='',
                is_iban=bool(
                    payment['payment_type']['is_iban'] if 'is_iban' in payment['payment_type'] else None),
                base_currency=payment['payment_type']['base_currency'] if 'base_currency' in payment[
                    'payment_type'] else None
            ).to_dictionary())

        return result
