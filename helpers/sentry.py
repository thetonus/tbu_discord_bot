""" Sentry Client """
import sentry_sdk
from settings import SENTRY_CLIENT_KEY

client = sentry_sdk.init(SENTRY_CLIENT_KEY)