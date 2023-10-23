from itsdangerous import TimedSerializer

from itsdangerous import URLSafeTimedSerializer

from meidou_mall.settings import SECRET_KEY


def encode_token(token):
    serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    return serializer.dumps(token)


def decode_token(token_encoded):
    serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    return serializer.loads(token_encoded)