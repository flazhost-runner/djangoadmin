"""Core middleware: MethodOverrideMiddleware, RateLimiter, MultiSourceCsrfMiddleware."""
import time
import hmac
import threading
from django.http import HttpRequest
from django.middleware.csrf import CsrfViewMiddleware


class _RateLimiter:
    """Thread-safe in-memory rate limiter."""
    def __init__(self, max_requests: int, window_seconds: int):
        self._max = max_requests
        self._window = window_seconds
        self._store: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    _LOOPBACK = {'127.0.0.1', '::1', '0:0:0:0:0:0:0:1', 'localhost'}

    def check(self, key: str) -> bool:
        if key in self._LOOPBACK:
            return True
        now = time.time()
        with self._lock:
            timestamps = [t for t in self._store.get(key, []) if now - t < self._window]
            if len(timestamps) >= self._max:
                self._store[key] = timestamps
                return False
            timestamps.append(now)
            self._store[key] = timestamps
        return True


# authLimiter: 10 req / 15 min / IP (POST login, register, OTP request)
auth_limiter = _RateLimiter(max_requests=10, window_seconds=900)

# otpLimiter: 5 req / 15 min / IP (POST OTP process)
otp_limiter = _RateLimiter(max_requests=5, window_seconds=900)


class MethodOverrideMiddleware:
    """Convert POST + ?_method=PUT|DELETE|PATCH to the proper HTTP method.
    Mirrors NodeAdmin's method-override npm package."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.method == 'POST':
            override = (request.GET.get('_method') or '').upper()
            if override in ('PUT', 'PATCH', 'DELETE'):
                # Access request.POST while method is still 'POST' so Django parses the body.
                # Then inject the token into HTTP_X_CSRFTOKEN — the slot Django's CsrfViewMiddleware
                # reads for non-POST methods in process_view.
                csrf = (request.POST.get('csrfmiddlewaretoken', '')
                        or request.POST.get('_csrf', ''))
                if csrf:
                    request.META['HTTP_X_CSRFTOKEN'] = csrf
                request.method = override
                request.META['REQUEST_METHOD'] = override
        return self.get_response(request)


class MultiSourceCsrfMiddleware(CsrfViewMiddleware):
    """Extend Django CSRF to accept token from 3 sources:
    1. Body field `_csrf` (or Django's `csrfmiddlewaretoken`)
    2. Query param `?_csrf=`
    3. Header `x-csrf-token` (lowercase, i.e. HTTP_X_CSRF_TOKEN)
    Skips enforcement for paths starting with /api/.
    """

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Skip CSRF for /api/ routes
        if request.path.startswith('/api/'):
            return None

        # Inject token from alternate sources into META so Django's checker finds it
        token = (
            request.POST.get('_csrf')
            or request.GET.get('_csrf')
            or request.META.get('HTTP_X_CSRF_TOKEN')
        )
        if token:
            # Place it where Django's CSRF mechanism reads it
            request.META['HTTP_X_CSRFTOKEN'] = token

        return super().process_view(request, callback, callback_args, callback_kwargs)
