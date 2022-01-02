from google.api_core.exceptions import PermissionDenied
from google.cloud import secretmanager


def get_secret(name: str, fallback, client=None):
    if not client:
        client = secretmanager.SecretManagerServiceClient()
    try:
        return client.access_secret_version(name=name)
    except PermissionDenied as error:
        return fallback()
