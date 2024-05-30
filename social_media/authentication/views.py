from django.shortcuts import render, redirect
from django.core import mail
from .models import CustomUser
import random
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        provided_password = request.POST.get('password').strip()

        if email:
            user = CustomUser.objects.get(email=email)
            stored_hashed_password = user.password

            if check_password(provided_password, stored_hashed_password):
                request.session['user_email'] = email
                request.session['id'] = user.id
                return redirect('home:home')

            else:
                context = {
                    'page_title': "Sign In",
                    'success': False,
                    'toast_message': "Email and password doesn't match",
                    'sub_message': "Please try again or reset password."
                }
                return render(request, "login.html", context)
        else:
            context = {
                'page_title': "Sign In",
                'success': False,
                'toast_message': "Email not found",
                'sub_message': "Please register your account."
            }
            return render(request, "login.html", context)

    context = {'page_title': "Sign In", 'success': True}
    return render(request, "login.html", context)

    # 0 = first time page
    # 1 = success
    # 400 = email not found
    # 401 = password wrong


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_code = random.randint(1000, 9999)
        username = email.split("@")[0] + str(random.randint(1000, 9999))

        try:
            # Try to get the user by email
            user = CustomUser.objects.get(email=email)

            # If user exists, update the OTP code
            context = {
                'page_title': "Sign Up",
                'success': False,
                'toast_message': 'Email already registered',
                'sub_message': 'Please use another email to create your account'
            }

            return render(request, "register.html", context)

        except CustomUser.DoesNotExist:
            # If user does not exist, create a new user
            new_user = CustomUser(email=email, otp_code=otp_code, username=username, follower_count=0, following_count=0)
            new_user.save()

        # Send email and set session
        mail.send_mail(
            "Verify Your Account with OTP Code",
            f"Your OTP Code is : {otp_code}",
            "sofietiara404@gmail.com",
            [email],
            fail_silently=False,
        )

        request.session['user_email'] = email

        # Pass a variable to the template to indicate success
        return redirect('verify_otp')

    # Pass a variable to the template to indicate failure
    context = {'page_title': "Sign Up", 'success': True}
    return render(request, "register.html", context)


def verify_otp_code(request):
    if request.method == "POST":
        input_otp_code = request.POST.get('otp_code').strip()
        email = request.session.get('user_email')
        user = CustomUser.objects.get(email=email)
        otp_code = str(user.otp_code).strip()  # Retrieve the otp_code from the user

        if input_otp_code == otp_code:
            # return redirect('home:home')
            return redirect('register_profile')
        else:
            context = {
                'page_title': "Verify",
                'success': False,
                'toast_message': 'Sorry, wrong OTP Code',
                'sub_message': 'We have sent your OTP Code via Gmail, please check the gmail for your OTP Code'
            }

            return render(request, "register_verify_otp.html", context)

    context = {'page_title': "Verify", 'success': True}
    return render(request, "register_verify_otp.html", context)


def register_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        phone_number = request.POST.get('phone_number').strip()
        password = request.POST.get('password').strip()
        email = request.session.get('user_email')

        user = CustomUser.objects.get(email=email)  # get user data

        user.name = name
        user.phone_number = phone_number
        user.password = make_password(password)

        user.save()

        return redirect('home:home')

    context = {'page_title': "Write your identity", 'success': True}
    return render(request, "register_profile.html", context)


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        
        try:
            user = CustomUser.objects.get(email=email)
            request.session['user_email'] = email
            rp_otp_code = random.randint(1000, 9999)
            user.rp_otp_code = rp_otp_code
            user.rp_verify_status = 0
            user.save()

            mail.send_mail(
                "Verify Your Account to Reset Password with OTP Code",
                f"Your OTP Code is : {rp_otp_code}",
                "sofietiara404@gmail.com",
                [email],
                fail_silently=False,
            )
            
            return redirect('rp_verify_otp_code')

        except CustomUser.DoesNotExist:
            context = {
                'page_title': "Forget Password", 
                'success': False,
                'toast_message': 'Sorry',
                'sub_message': 'Account does not exist. Please try with another email'
            }
            return render(request, "forget_password.html", context)

    # Pass a variable to the template to indicate failure
    context = {'page_title': "Forget Password", 'success': True}
    return render(request, "forget_password.html", context)


def rp_verify_otp_code(request):
    if request.method == "POST":
        input_otp_code = request.POST.get('otp_code').strip()
        email = request.session.get('user_email')
        user = CustomUser.objects.get(email=email)
        rp_otp_code = str(user.rp_otp_code).strip()  # Retrieve the otp_code from the user

        if input_otp_code == rp_otp_code:
            return redirect('reset_password')
        
        else:
            context = {
                'page_title': "Verify", 
                'success': False,
                'toast_message': 'Sorry, wrong OTP Code',
                'sub_message': 'We have sent your OTP Code via Gmail, please check the gmail for your OTP Code'
            }
            return render(request, "register_verify_otp.html", context)

    context = {'page_title': "Verify", 'success': True}
    return render(request, "register_verify_otp.html", context)


def reset_password(request):
    if request.method == "POST":
        password = request.POST.get('password').strip()
        email = request.session.get('user_email')
        user = CustomUser.objects.get(email=email)
        user.password = make_password(password)
        user.save()

        return redirect('login')


    context = {'page_title': "Reset Password", 'success': True}
    return render(request, "reset_password.html", context)



