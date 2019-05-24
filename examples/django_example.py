import datetime
import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from models import Messages
from models import Payment

from paysera_webtopay import WebToPay
from paysera_webtopay.callback_validator import CallbackValidator

project_id = 123
sign_password = 'abc'
test_payment = 1


def paysera_build_request(request: HttpRequest) -> JsonResponse:
    """
    Build request for paysera payment API
    parameters: https://developers.paysera.com/en/payments/current#integration-via-library
    """

    def handle_urls(request: HttpRequest):
        protocol = 'https' if request.is_secure() else 'http'
        uri = protocol + '://' + request.get_host() + '/'
        data_dict = request.GET.dict()
        data_dict['accepturl'] = uri + 'paysera-payment-accept'
        data_dict['cancelurl'] = uri + 'paysera-payment-cancel'
        data_dict['callbackurl'] = uri + 'paysera-payment-check-response'
        return data_dict

    data = handle_urls(request)
    data['sign_password'] = sign_password
    data['projectid'] = project_id
    data['time_limit'] = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime(
        '%Y-%m-%d %H:%M:%S')
    data['frame'] = 1
    data['test'] = test_payment

    payment = Payment(amount_in_cents=data['amount'],
                      currency=data['currency'])
    payment.save()
    data['orderid'] = payment.order_id
    web_to_pay = WebToPay()
    pay_request: dict = web_to_pay.build_request(data)
    return JsonResponse(
        {'url': web_to_pay.get_public_pay_url() + '?data=' + pay_request.get(
            'data') + '&sign=' + pay_request.get(
            'sign')})


def paysera_check_response(request: HttpRequest) -> HttpResponse:
    """
    paysera-payment-check-response route handler
    """
    response = WebToPay().check_response(request.GET, project_id, sign_password)
    if not response.get('orderid', None):
        raise KeyError('Order id not set in response')
    response_order_id = int(response['orderid'][0])
    db_order = Payment.objects.filter(pk=response_order_id).first()
    if not db_order:
        raise LookupError('Order with order id {} not found'.format(response_order_id))
    db_order.response = json.dumps(response)
    db_order.save()
    if int(response['status'][0]) == 1:
        if db_order.status == 'done':
            return HttpResponse('OK')
        else:
            if int(response['amount'][0]) != db_order.amount_in_cents or \
                    str(response['currency'][0]) != db_order.currency or \
                    int(response['test'][0]) != test_payment:
                raise ValueError('Some values are not as expected')
            handle_successful_payment(request, response_order_id)
            return HttpResponse('OK')
    elif int(response['status'][0]) == 3:
        db_order.additional_data = json.dumps(response)
        db_order.save()


def paysera_accept(request: HttpRequest):
    """
    paysera-payment-accept route handler
    """
    response = CallbackValidator(password=sign_password).validate_and_parse_data(request.GET,
                                                                                 project_id)
    if int(response['status'][0]) == 0 or int(response['status'][0]) == 2:
        Messages.info(request.user,
                      'Your payment has been got successfuly, it will be confirmed shortly.')
        return redirect('/')
    elif int(response['status'][0]) == 1:
        if not response.get('orderid', None):
            raise KeyError('Order id not set in response')
        response_order_id = int(response['orderid'][0])
        payment = Payment.objects.get(pk=response_order_id)
        if payment.status == 'done':
            Messages.info(request.user, 'Your payment was processed. Thank you for buying.')
            return redirect('/')
        return handle_successful_payment(request, response_order_id)


def paysera_cancel(request: HttpRequest):
    """
    paysera-payment-cancel route handler
    """
    Messages.info(request.user, 'Payment cancelled or rejected.')
    return redirect('/')


def handle_successful_payment(request: HttpRequest, paysera_order_id: int) -> HttpResponse:
    """Handles successul payment in app"""
    Payment.objects.filter(order_id=paysera_order_id).update(status='done')

    Messages.info(request.user, 'Your payment was processed. Thank you for buying.')
    return redirect('/')
