def decode_safe_url_base64(encoded_text: str) -> str:
    import base64
    return base64.urlsafe_b64decode(encoded_text.encode()).decode()


def encode_safe_url_base64(text: str) -> str:
    import base64
    return base64.urlsafe_b64encode(text.encode()).decode()


def get_configuration(environment: str) -> dict:
    from .configuration import configuration
    if environment in configuration['routes'].keys():
        return configuration['routes'][environment]
    raise KeyError('Configuration key error')


def parse_http_query(query: str):
    print(query)
    from urllib.parse import parse_qs
    return parse_qs(query)
