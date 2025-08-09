# chats/middleware.py
from datetime import datetime
import logging
from django.http import HttpResponseForbidden
from django.http import JsonResponse



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
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store message timestamps per IP
        self.ip_message_log = {}
        self.limit = 5  # max messages allowed
        self.time_window = 60  # seconds (1 minute)

    def __call__(self, request):
        # Only track POST requests to the chat message endpoint
        if request.method == 'POST' and '/messages' in request.path.lower():
            ip_address = self.get_client_ip(request)
            now = time.time()

            # Initialize IP log if not present
            if ip_address not in self.ip_message_log:
                self.ip_message_log[ip_address] = []

            # Remove timestamps older than the time window
            self.ip_message_log[ip_address] = [
                ts for ts in self.ip_message_log[ip_address]
                if now - ts < self.time_window
            ]

            # Check if limit exceeded
            if len(self.ip_message_log[ip_address]) >= self.limit:
                return JsonResponse(
                    {"error": "Message limit exceeded. Please wait before sending more."},
                    status=429
                )

            # Log the current message timestamp
            self.ip_message_log[ip_address].append(now)

        # Continue normal processing
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get the client's IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip