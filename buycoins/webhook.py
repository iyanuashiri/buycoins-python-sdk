import hashlib
import hmac


def verify_payload(body, webhook_token, header_signature):
    """

    :param body:
    :param webhook_token:
    :param header_signature:
    :return:
    """
    signing_key = webhook_token.encode("utf-8")
    if not isinstance(body, bytes):
        body = bytes(body)

    hashed = hmac.new(signing_key, body, hashlib.sha1)
    return hashed.hexdigest() == header_signature
