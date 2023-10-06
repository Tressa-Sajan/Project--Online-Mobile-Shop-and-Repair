from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

'''from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login'''
# Create your views here.
def index(request):
    return render(request, 'index.html')
def login(request): 
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        myuser = authenticate(request, email=email, password=password)
        if myuser is not None:
                login(request, myuser)
                if myuser.role=='SELLER':
                    return redirect('/index')
                elif myuser.role=='PRODUCT':
                    return redirect('/index')
                elif myuser.role=='ADMIN':
                    messages.success(request,"Login Sucess!!!")
                    return HttpResponse("Admin login ")
                          
        else:
                   messages.error(request,"Something went wrong")
                   return redirect('/login')
    return render(request, 'login.html')

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmPassword=request.POST['confirmPassword']
       # p2=request.POST['confirmPassword']
        if '@' not in  email or '.' not in email:
                messages.warning(request, "Enter a valid email")
                return render(request, 'signup.html')
        if password!=confirmPassword:
                    messages.warning(request,"password is not matching")
                    return render(request,'signup.html')
        try:
                      if User.objects.get(username=email):
                             messages.warning(request,"Email is already taken")
                             return render(request,'signup.html')
        except Exception as identifiers:
                      pass

        user=User.objects.create_user(username=username,email=email,role='USER') 
        user=User(password=password)
        user.save()
    return render(request,'signup.html')

def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')
def inside(request):
    return render(request, 'inside.html')
#def logout_view(request):
    #logout(request)
    #return redirect('login')
#here
#def sellerRegistration(request):
     #return render(request, 'sellerRegistration.html')

#def seller_template(request):
     #return render(request, 'seller_template.html')


#
#
#
#

