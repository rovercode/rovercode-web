"""Users utils."""
from rest_framework_jwt.utils import jwt_payload_handler as \
    base_jwt_payload_handler


def jwt_payload_handler(user):
    """Populate JWT with user data."""
    payload = base_jwt_payload_handler(user)
    payload['show_guide'] = user.show_guide

    return payload
