import time
from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def limit_rate(num_requests, period):
    def decorator(view_func):
        request_history = []

        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            current_time = time.time()

            request_history[:] = [timestamp for timestamp in request_history if timestamp > current_time - period]

            if len(request_history) >= num_requests:
                responce_len_ratelimit = {
                    "message": "Отдохните, и попробуйте оставить ваш отзыв через час",
                }
                return Response(responce_len_ratelimit, status=status.HTTP_429_TOO_MANY_REQUESTS)

            request_history.append(current_time)
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator
