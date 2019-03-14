import json
import xmltodict
from .configuration import configuration
from .web_client import WebClient


class PaymentMethodListProvider:

    def get_payment_method_list(self, projectid: int, currency: str, environment: str) -> str:
        uri = "{}{}/currency:{}".format(configuration.get('routes').get(environment).get('payment_method_list'),
                                        projectid, currency)
        xml_string = WebClient().get(uri).decode()
        xml_dict_object = xmltodict.parse(xml_string)
        return json.dumps(xml_dict_object)
