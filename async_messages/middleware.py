from django.contrib import messages
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from async_messages import get_messages


class AsyncMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        """
        Check for messages for this user and, if it exists,
        call the messages API with it
        """
        if hasattr(request, "session") and hasattr(request, "user") and request.user.is_authenticated():
            msgs = get_messages(request.user)
            if msgs:
                for msg, level in msgs:
                    messages.add_message(request, level, msg)
        return response
