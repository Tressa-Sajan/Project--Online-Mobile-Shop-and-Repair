from django.shortcuts import render, redirect
from django.http import HttpResponse
from Store.forms import PasswordResetForm, PasswordResetRequestForm
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail 
from django.contrib import messages
from django.http import JsonResponse

def showIndexPage(request):
    return render(request, "index.html")

def showSigninPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)   #boss#request,email
        #my code
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'')
            return redirect('login')
    else:
            
        return render(request, "login.html")

def showSignupPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        ConfirmPassword  = request.POST['ConfirmPassword']
        if password == ConfirmPassword :
            if User.objects.filter(email=email).exists():
                messages.info(request,'email is already exist')
                return redirect('login')
            else:
                user = User.objects.create_user(username=username,email=email,userRole="customer")
                user.set_password(password)
                user.save()
                return redirect('login')
    else:
        return render(request, "signup.html")

def check_user_exists(request):
    customerMail = request.GET.get('email')  # You can also use 'email' if you're checking by email
    data = {
        'exists': User.objects.filter(email=customerMail).exists()
    }
    return JsonResponse(data)
#
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate a password reset token
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                # Send an email with a link for resetting the password
                reset_link = f"http://{request.get_host()}/reset_password/{uid}/{token}/"
                send_mail(
                    'Password Reset Request',
                    f'Click the following link to reset your password: {reset_link}',
                    'noreply@example.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'An email with instructions to reset your password has been sent to your email address.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User with this email address does not exist.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_request.html') 

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                form = PasswordResetForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('home')
            else:
                form = PasswordResetForm()
            return render(request, 'password_reset_confirm.html', {'form': form})
        else:
            messages.error(request, 'Invalid token. Please request a new password reset link.')
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return redirect('login')