# chats/middleware.py
from datetime import datetime
import logging
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time
        current_hour = datetime.now().hour

        # Allow only between 9 AM (09:00) and 6 PM (18:00)
        if current_hour < 9 or current_hour >= 18:
            return HttpResponseForbidden(
                "Access to the chat is restricted to between 9 AM and 6 PM."
            )

        return self.get_response(request)