from django.utils.deprecation import MiddlewareMixin

from core.settings.base import DEBUG


class DisableCSRFMiddleware(MiddlewareMixin):
    def disable(self, request):
        if DEBUG:
            setattr(request, '_dont_enforce_csrf_checks', True)