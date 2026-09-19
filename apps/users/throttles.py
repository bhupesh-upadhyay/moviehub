from rest_framework.throttling import AnonRateThrottle


class AuthAnonRateThrottle(AnonRateThrottle):
    """Stricter limit for password reset / abuse-prone anonymous endpoints."""

    scope = "auth"
