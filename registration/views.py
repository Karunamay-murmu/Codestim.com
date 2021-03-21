import uuid
import requests
import json

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page
from django.contrib import messages
from django.shortcuts import redirect

from .forms import Signup, Login
from .models import User

from .validate_captcha import validate_captcha

@method_decorator(compress_page, name="dispatch")
class User_signup(FormView):
    form_class = Signup
    template_name = 'authentication/signup.html'

    def dispatch(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'You are alreay logeed in',
                          extra_tags='info')

            return HttpResponseRedirect(reverse('blog:home'))

        return super(User_signup, self).dispatch(request)

    def form_valid(self, form):
        user = form.save(commit=False)
        valid_captcha = validate_captcha(self.request)

        if valid_captcha == False:
            form.add_error(None, 'Captcha invalid or empty')

            return self.form_invalid(form)

        user.save()
        messages.success(
            self.request, 'Account created successfully. Please Login!', extra_tags='success')

        return super(User_signup, self).form_valid(form)

    def get_success_url(self):
        return reverse('registration:log_in')

@method_decorator(compress_page, name="dispatch")
class User_login(FormView):
    form_class = Login
    template_name = 'authentication/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are alreay logeed in',
                          extra_tags='info')

            return HttpResponseRedirect(reverse('blog:home'))

        return super(User_login, self).dispatch(request)

    def form_valid(self, form):
        email, password = form.cleaned_data.values()
        user = authenticate(email=email, password=password)

        if user is not None:
            login(self.request, user)
            if 'next' in self.request.POST:
                return redirect(self.request.POST.get('next'))

            return HttpResponseRedirect(reverse('blog:home'))

        return super(User_login, self).form_valid(form)


@login_required
def User_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:home'))
