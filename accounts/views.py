from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse

import qrcode
import qrcode.image.svg
import pyotp

from accounts.forms import LoginForm,CustomUserCreationForm
from accounts.models import UserAuth


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,email = email,password = password)
            if user:
                if user.userauth.has_two:
                    otp = form.cleaned_data['otp']
                    if not pyotp.TOTP(user.userauth.secret_key).verify(otp):
                        messages.error(request, 'Your Two Factor is ON')
                        messages.error(request, 'Please Enter Valid TOTP')
                        return render(request,"accounts/login.html")
                login(request,user)
                return redirect("accounts:profile")
        messages.error(request, 'Invalid Email/Password.')
    return render(request,"accounts/login.html")


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = form.save()
            UserAuth.objects.create(secret_key = pyotp.random_base32(),user = user)
            send_mail('Account Created Successfully','Your Account Has Been Created.','lukasgarden05@gmail.com',[email])
            return redirect('accounts:created')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def qrcode_view(request):
    url = pyotp.totp.TOTP(request.user.userauth.secret_key).provisioning_uri(name=request.user.email, issuer_name='Secure App')
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgImage)
    response = HttpResponse(content_type='image/svg+xml')
    img.save(response)
    return response


@login_required
def profile(request):
    auth = request.user.userauth
    if request.method == 'POST':
        auth.has_two = True if request.POST.get("has_two") else False
        auth.save()
        return redirect("accounts:profile")
    return render(request,"accounts/profile.html",{'has_two':auth.has_two})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


def created(request):
    return render(request,"accounts/created.html")
