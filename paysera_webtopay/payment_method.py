class PaymentMethod:
    def __init__(self, key: str, min_amount_in_cents: int, max_amount_in_cents: int, currency: str, logo_list=None,
                 title_translations=None,
                 default_language: str = 'en', is_iban: bool = False, base_currency: str = None, group: str = None):
        if title_translations is None:
            title_translations = {}
        if logo_list is None:
            logo_list = {}
        if group is None:
            group = ''
        self.group = group
        self._key = key
        self._logo_list = logo_list
        self._title_translations = title_translations
        self._default_language = default_language
        self._is_iban = is_iban
        self._base_currency = base_currency
        self.min_amount = min_amount_in_cents
        self.max_amount = max_amount_in_cents
        self.currency = currency

    def to_dictionary(self, language: str):
        return {
            'logo_url': self.get_logo(language),
            'title': self.get_title(language),
            'key': self.get_key(),
            'min_amount': self.get_min_amount_as_string(),
            'max_amount': self.get_max_amount_as_string(),
            'is_iban': self.is_iban,
            'group': self.group
        }

    @property
    def default_language(self):
        return self._default_language

    @default_language.setter
    def default_language(self, language: str):
        self._default_language = language

    def get_key(self):
        return self._key

    def get_logo(self, language_code=None):
        return self._logo_list[language_code] if language_code in self._logo_list else (
            self._logo_list[self._default_language] if self._default_language in self._logo_list else None)

    def get_title(self, language_code=None):
        return self._title_translations[language_code] if language_code in self._title_translations else (
            self._title_translations[
                self._default_language] if self._default_language in self._title_translations else None)

    def is_available_for_amount(self, amount_in_cents, currency):
        if self.currency != currency:
            raise Exception(
                'Currencies does not match. You have to get payment types for the currency you are checking. Given '
                'currency: {} , available currency: {}'.format(
                    currency, self.currency))
        return (self.min_amount is None or amount_in_cents >= self.min_amount) and (
                self.max_amount is None or amount_in_cents <= self.max_amount)

    def get_min_amount_as_string(self):
        return '' if self.min_amount is None else "{} {}".format(int(self.min_amount) / 100, self.currency)

    def get_max_amount_as_string(self):
        return '' if self.max_amount is None else "{} {}".format(int(self.max_amount) / 100, self.currency)

    @property
    def is_iban(self):
        return self._is_iban

    @is_iban.setter
    def is_iban(self, is_iban):
        self._is_iban = is_iban

    @property
    def base_currency(self):
        return self._base_currency

    @base_currency.setter
    def base_currency(self, base_currency):
        self._base_currency = base_currency
