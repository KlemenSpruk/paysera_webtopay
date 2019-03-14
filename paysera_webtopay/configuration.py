configuration = {
    'routes': {
        'production': {
            'public_key': 'http://www.paysera.com/download/public.key',
            'payment': 'https://bank.paysera.com/pay/',
            'payment_method_list': 'https://www.paysera.com/new/api/paymentMethods/',
            'sms_answer': 'https://bank.paysera.com/psms/respond/',
        },
        'sandbox': {
            'public_key': 'http://sandbox.paysera.com/download/public.key',
            'payment': 'https://sandbox.paysera.com/pay/',
            'payment_method_list': 'https://sandbox.paysera.com/new/api/paymentMethods/',
            'sms_answer': 'https://sandbox.paysera.com/psms/respond/',
        }
    }
}
