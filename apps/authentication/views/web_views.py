from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from apps.authentication.services.auth_service import AuthService
from core.errors import AppError
from core.middleware import auth_limiter, otp_limiter


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('admin.v1.dashboard.index')
        return render(request, 'be/default/auth/login.html', {})

    def post(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown')).split(',')[0].strip()
        if not auth_limiter.check(ip):
            messages.error(request, 'Too many attempts. Please try again later.')
            return render(request, 'be/default/auth/login.html', {})
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        try:
            result = AuthService().login(email, password)
            user = result['user']
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'Login Success.')
            return redirect('admin.v1.dashboard.index')
        except AppError as e:
            messages.error(request, 'Wrong email or password.')
            return render(request, 'be/default/auth/login.html', {'email': email})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Logout Success.')
        return redirect('web.auth.login')


class RegisterView(View):
    def get(self, request):
        return render(request, 'be/default/auth/register.html', {})

    def post(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown')).split(',')[0].strip()
        if not auth_limiter.check(ip):
            messages.error(request, 'Too many attempts. Please try again later.')
            return render(request, 'be/default/auth/register.html', {})
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        # Strip roles from body (security — never accept roles from register form)
        data = {'email': email, 'password': password, 'name': name}
        try:
            AuthService().register(data)
            messages.success(request, 'Register Success.')
            return redirect('web.auth.login')
        except AppError as e:
            messages.error(request, e.message)
            return render(request, 'be/default/auth/register.html', {'email': email, 'name': name})


class ResetRequestView(View):
    def get(self, request):
        return render(request, 'be/default/auth/reset_request.html', {})

    def post(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown')).split(',')[0].strip()
        if not auth_limiter.check(ip):
            messages.error(request, 'Too many attempts. Please try again later.')
            return render(request, 'be/default/auth/reset_request.html', {})
        email = request.POST.get('email', '').strip()
        try:
            AuthService().request_reset(email)
            messages.success(request, 'OTP Send Success.')
            return redirect('web.auth.reset.process')
        except AppError as e:
            messages.error(request, e.message)
            return render(request, 'be/default/auth/reset_request.html', {'email': email})


class ResetProcessView(View):
    def get(self, request):
        return render(request, 'be/default/auth/reset_process.html', {})

    def post(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown')).split(',')[0].strip()
        if not otp_limiter.check(ip):
            messages.error(request, 'Too many attempts. Please try again later.')
            return render(request, 'be/default/auth/reset_process.html', {})
        email = request.POST.get('email', '').strip()
        otp = request.POST.get('otp', '').strip()
        new_password = request.POST.get('new_password', '')
        try:
            AuthService().process_reset(email, otp, new_password)
            messages.success(request, 'Reset Password Success.')
            return redirect('web.auth.login')
        except AppError as e:
            messages.error(request, e.message)
            return render(request, 'be/default/auth/reset_process.html', {'email': email, 'otp': otp})
