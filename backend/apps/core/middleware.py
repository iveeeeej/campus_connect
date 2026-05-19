from django.conf import settings
from django.http import HttpResponse


class LocalDevelopmentCorsMiddleware:
    """Allow local static frontend files to call the API during development."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.is_enabled() and request.method == "OPTIONS":
            response = HttpResponse()
        else:
            response = self.get_response(request)

        if self.is_enabled() and self.is_allowed_origin(request.headers.get("Origin")):
            origin = request.headers.get("Origin")
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Vary"] = "Origin"

        return response

    def is_enabled(self):
        return bool(getattr(settings, "DEBUG", False) or getattr(settings, "ENABLE_DEV_CORS", False))

    def is_allowed_origin(self, origin):
        if not origin:
            return False
        return (
            origin == "null"
            or origin.startswith("http://localhost:")
            or origin.startswith("http://127.0.0.1:")
        )
