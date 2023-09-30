from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

'''from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login'''
# Create your views here.
def index(request):
    return render(request, 'index.html')



def login(request): 
    if request.method=="POST":
        email=request.POST['email']
        pass1=request.POST['pass1']
        myuser=authenticate(email=email,pass1=pass1)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')  # Redirect to the 'index' URL
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')  # Redirect back to the 'login' URL in case of invalid credentials

    return render(request, 'login.html')



def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        p1=request.POST['pass1']
       # p2=request.POST['pass2']
        
        user=User.objects.create_user(username,email,p1)
        user.save()
        return render(request,'login.html')
        #return HttpResponse("user is created",email)
    return render(request,'signup.html')


def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')




