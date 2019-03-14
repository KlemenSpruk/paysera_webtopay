import base64


def decode_safe_url_base64(encoded_text: str) -> str:
    return base64.b64decode(encoded_text.encode()).decode().replace('-', '+').replace('_', '/')


def encode_safe_url_base64(text: str) -> str:
    return base64.b64encode(text.encode()).decode().replace('+', '-').replace('/', '_')
