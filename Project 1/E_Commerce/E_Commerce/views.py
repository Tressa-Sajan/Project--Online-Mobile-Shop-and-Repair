from django.http import HttpResponse
from django.shortcuts import redirect,render
from app.models import Category, Main_Category,Product, Product_Image, Sub_Category
from app.models import User
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # messages.success(request, 'Login successful! Welcome back, {}.'.format(username))
            return redirect('adminDash')
        if request.user.userRole == 'Seller':
            return redirect('sellerPage')
     #sliders = slider.objects.all().order_by('-id')[0:3]
     #banner = banner_area.objects.all().order_by('-id')[0:3]
    
    main_category = Main_Category.objects.all()
    products = Product.objects.all()
    context = {
         'main_category':main_category,
         'product':products,
   }
    return render(request,'Main/home.html',context)

def LOGIN(request):
    return render(request,'account/login.html')

def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        userRole = request.POST['role']
        if User.objects.filter(username = username).exists():
            messages.error(request,'Username is already exists')
            return redirect('login')
        if User.objects.filter(email = email).exists():
            messages.error(request,'Email is already exists')
            return redirect('login')
        user = User(
            username = username,
            email = email,    
            userRole = userRole
        )
        user.set_password(password)
        user.save() 
        return redirect('login')
        
    else:
        return render(request,'account/register.html')

def LOGIN(request):   
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful! Welcome back, {}.'.format(username))
            return redirect('home')
        else:
            messages.error(request, 'Email and password are invalid.')
            return redirect('login') 
    return render(request, 'account/login.html')
#def logout(request):   
    #return render(request, 'account/ login/')
#def password_change(request):   
    #return render(request, 'account/ password_change/')
#def password_change_done(request):   
    #return render(request, 'account/ password_change/done/')
#def password_reset(request):   
    #return render(request, 'account/ password_reset/')
#def password_reset_done(request):   
    #return render(request, 'account/ password_reset/done/')
#def password_reset_confirm(request):   
    #return render(request, 'account/ reset/<uidb64>/<token>/')
#def password_reset_complete(request):   
    #return render(request, 'account/ reset/done/')


# View For Admin Panel
@login_required
@never_cache
def admin_DashBoard_View(request):
    data = {
        "users": False
    }
    # User.objects.get(id=1).delete()
    users = User.objects.exclude(is_superuser=True)
    data['users'] = users
    return render(request, 'Main/admin_dashboard.html', data)


def logoutUser(request):
    logout(request)
    return redirect('home')

def productDetails(request):
    return redirect('productDetails')

@login_required
@never_cache
def profileSettings(request):
    userData = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        userData.username = request.POST['username']
        userData.first_name = request.POST['firstname']
        userData.last_name = request.POST['lastname']
        userData.email = request.POST['email']
        userData.save()
    data = {
        "user": userData
    }
    return render(request, "Main/user_settings.html", data)

@login_required
@never_cache
def addProduct(request):
    if request.method == 'POST':
        pname = request.POST['productName']
        price = request.POST['productPrice']
        disc = request.POST['productDiscount']
        stock = request.POST['productStock']
        pinfo = request.POST['productInfo']
        model = request.POST['model']
        desc = request.POST['description']
        cat = request.POST['c']
        featured_image = request.FILES['productImages']
        cat = Category.objects.get(id=cat)
        new_product = Product(
            product_name = pname,
            price = price,
            Discount = disc,
            total_quantity = stock,
            Availability = stock,
            Product_information = pinfo,
            model_Name = model,
            Description = desc,
            Categories = cat,
            featured_image = featured_image
        )
        new_product.save()
        product_images = request.FILES.getlist('productImages1')
        for image in product_images:
            productImage = Product_Image()
            productImage.product = new_product
            productImage.Image_url = image
            productImage.save()
        return redirect('addProduct')
    mainCategories = Main_Category.objects.all()
    categories = Category.objects.all()
    subCategories = Sub_Category.objects.all()
    data = {
        "mc": mainCategories,
        "c": categories,
        "sc": subCategories
    }
    return render(request, "Main/addProduct.html", data)

def sellerPage(request):
    return render(request, "Main/seller_Page.html")

def deactivate(request):
    uid=request.GET['id']
    user=User.objects.get(id=uid)
    user.is_active = False
    user.save()
    return redirect ('adminDash')

def activate(request):
    uid=request.GET['id']
    user=User.objects.get(id=uid)
    user.is_active=True
    user.save()
    return redirect('adminDash')

def productView(request):
    return render(request, 'Main/products.html')