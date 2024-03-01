from django.http import HttpResponse
from django.shortcuts import redirect,render, get_object_or_404
from app.models import Category, Main_Category, Product, Product_Image, Sub_Category
from app.models import User,Product, Cart, CartItem, Order, OrderItem, UserProfile, DeliveryAssignment, Image
from django.db import IntegrityError
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay
import json


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart = user.cart

        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        try:
            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.payment_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

@csrf_exempt
def checkout(request):
    client = razorpay.Client(auth=("rzp_test_KE5hiRXWNUNLRk", "WrlDqvBYnjEIrz67ruEptIVq"))
    print(request.user)
    payment = client.order.create({
    "amount": 50000,
    "currency": "INR",
    "receipt": "receipt#1",
    "partial_payment": False,
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
    })
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    cart_count = get_cart_count(request)
    email = request.user.email
    username = request.user.username

    context = {
        "paymentId": payment['id'],
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'email':email,
        'username': username
    }
    # request.session["id"]=request.user.id
    return render(request, 'Main/checkout.html', context)

# @csrf_exempt
# def handle_payment(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         razorpay_order_id = data.get('order_id')
#         payment_id = data.get('payment_id')

#         try:
#             order = Order.objects.get(payment_id=razorpay_order_id)

#             client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             payment = client.payment.fetch(payment_id)

#             if payment['status'] == 'captured':
#                 order.payment_status = True
#                 order.save()
#                 # user = request.user
#                 # user.cart.cartitem_set.all().delete()
#                 return JsonResponse({'message': 'Payment successful'})
#             else:
#                 return JsonResponse({'message': 'Payment failed'})

#         except Order.DoesNotExist:
#             return JsonResponse({'message': 'Invalid Order ID'})
#         except Exception as e:

#             print(str(e))
#             return JsonResponse({'message': 'Server error, please try again later.'})

@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')
        csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
        print(f'CSRF Token: {csrf_token}')
        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                # Additional logic if needed, e.g., clearing the user's cart
                # user = request.user
                # user.cart.cartitem_set.all().delete()

                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:
            # Log the error for debugging purposes
            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})

    # # Return a proper response for non-POST requests
    # return HttpResponse('Method not allowed', status=405)

# @login_required(login_url='login')
# def add_to_cart(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
#     if not item_created:
#         cart_item.quantity += 1
#         cart_item.save()
    
#     return redirect('home')


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(user=request.user, cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('home')


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('cart')

@login_required(login_url='login')
def view_cart(request):
    cart = request.user.cart
    print(request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    return render(request, 'Main/cart.html', {'cart_items': cart_items})

# @login_required(login_url='login')
# def view_cart(request):
#     try:
#         cart = Cart.objects.get(user=request.user)
#         cart_items = CartItem.objects.filter(cart=cart)
#     except Cart.DoesNotExist:
#         cart_items = []

    # return render(request, 'Main/cart.html', {'cart_items': cart_items})

@login_required(login_url='login')
def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    # cart = request.user.cart
    if hasattr(request.user, 'cart') and request.user.cart:
        cart = request.user.cart
        # cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
    else:
        cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()

    return redirect('cart')

@login_required(login_url='login')
def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required(login_url='login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count

def BASE(request):
    return render(request,'base.html')


from django.db.models import Q

def HOME(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminDash')
        if request.user.userRole == 'Seller':
            return redirect('seller_page')
    
    main_category = Main_Category.objects.all()
    
    # Get search query from GET parameters
    search_query = request.GET.get('q')
    
    # Filter products based on search query
    if search_query:
        products = Product.objects.filter(
            Q(product_name__icontains=search_query) | 
            Q(model_Name__icontains=search_query)
        )
    else:
        products = Product.objects.all()
    
    context = {
        'main_category': main_category,
        'product': products,
        'search_query': search_query  # Pass search query to template
    }
    
    return render(request, 'Main/home.html', context)



def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        userRole = request.POST.get('role')

        # Validation checks for username
        if not username:
            messages.error(request, 'Username cannot be empty.')
            return redirect('handleregister')
        if not username[0].isupper():
            messages.error(request, 'Username should start with a capital letter.')
            return redirect('handleregister')
        if any(char.isdigit() for char in username):
            messages.error(request, 'Username cannot contain numbers.')
            return redirect('handleregister')
        if ' ' in username:
            messages.error(request, 'Username cannot contain spaces.')
            return redirect('reghandleregisterister')
        if len(username) <= 3:
            messages.error(request, 'Username should be more than 3 characters.')
            return redirect('handleregister')

        # Validation checks for email
        if not email:
            messages.error(request, 'Email cannot be empty.')
            return redirect('handleregister')
        if ' ' in email:
            messages.error(request, 'Email cannot contain spaces.')
            return redirect('handleregister')
        if '@' not in email or '.' not in email:
            messages.error(request, 'Invalid email format.')
            return redirect('handleregister')

        # Validation checks for password
        if not password:
            messages.error(request, 'Password cannot be empty.')
            return redirect('handleregister')
        if ' ' in password:
            messages.error(request, 'Password cannot contain spaces.')
            return redirect('handleregister')
        if '@' not in password or not any(char.isalpha() or char.isdigit() for char in password):
            messages.error(request, 'Password must contain @, numbers, and alphabets.')
            return redirect('handleregister')

        # Validation checks for phone number, address, city, state, pincode (similar to other fields)

        # Validation checks for userRole
        if not userRole:
            messages.error(request, 'Please select a role.')
            return redirect('handleregister')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already in use.')
            return redirect('handleregister')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('handleregister')

        # Create the User object
        user = User(
            username=username,
            email=email,
            userRole=userRole
        )
        user.set_password(password)
        user.save()

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')
    else:
        return render(request, 'account/register.html')


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
    # User.objects.get(id=9).delete()
    data = {
        "users": False
    }
    
    users = User.objects.exclude(is_superuser=True)
    data['users'] = users
    return render(request, 'Main/admin_dashboard.html', data)


def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
@never_cache
def profileSettings(request):
    userData = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        userData.username = request.POST['username']
        userData.first_name = request.POST['firstname']
        userData.last_name = request.POST['lastname']
       # userData.place = request.POST['place']
        userData.email = request.POST['email']
       # userData.email = request.POST['']
       # userData.save()
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
            owner_id_id = request.user.id,
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
    #mainCategories = Main_Category.objects.all()
    categories = Category.objects.all()
    #subCategories = Sub_Category.objects.all()
    data = {
        # "mc": mainCategories,
        "c": categories,
        #"sc": subCategories
    }
    return render(request, "Main/addProduct.html", data)

def seller_page(request):
    if request.user.is_authenticated and request.user.product_set.exists():
        products = request.user.product_set.all()
        return render(request, 'Main/seller_page.html', {'products': products})
    else:
        return render(request, "Main/seller_Page.html", {'products': None})

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
    #Product.objects.filter(id=16).delete()
    products=Product.objects.all()
    data={
        "products":products
    }
    
    return render(request, 'Main/products.html', data)

def category(request):
    if request.method == 'POST':
        categoryName = request.POST.get('categoryName')  # Use get() to avoid KeyError
        cat = Category(name=categoryName)  # Create a new Category instance
        cat.save()  # Save the new category to the database
        return redirect('category')
    
    # Fetch all categories from the database
    categories = Category.objects.all()
    
    # Pass the categories to the template as a context variable
    return render(request, 'Main/category.html', {'categories': categories})
    
def buy(request):
    return render(request, 'Main/buy.html')

# @csrf_exempt
# def order(request):
#     user = User.objects.get(id=request.GET["id"])
#     order = Order()
#     order.user = request.user
#     order.products
#     # print(user.username)
#     login(request, user)
#     user = request.user
#     cart = user.cart
#     cart_items = CartItem.objects.filter(cart=cart)
#     # print(cart)
#     # for item in cart_items:
#     #     print("Product:", item.product.product_name)
#     #     print("Quantity:", item.quantity)
#     total_amount = sum(item.product.price * item.quantity for item in cart_items)
#     data = {
#         "cart_items": cart_items,  # Corrected key name
#         "total_amount": total_amount
#     }
#     return render(request, 'Main/order.html', data)
#     # else:
#     #     # Redirect the user to the login page
#     #     return redirect('login')
#     # return HttpResponse("An error occurred")

from django.db import transaction

@csrf_exempt
def order(request):
    # Assuming user is authenticated
    userId = request.GET['id']
    user = User.objects.get(id=userId)
    login(request, user)
    user = request.user
    cart = user.cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Create the order instance
    order = Order.objects.create(
        user=user,
        total_amount=total_amount
    )

    # Create order items and associate them with the order
    with transaction.atomic():
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                item_total=cart_item.product.price * cart_item.quantity
            )
            print(cart_item.product)
            print(cart_item.quantity)

    # Convert cart_items to a list before deleting
    cart_items_list = list(cart_items)

    # Clear the user's cart after order creation
    cart_items.delete()

    # Pass necessary data to the template
    data = {
        'user': user,
        'cart_items': cart_items_list,  # Pass the list instead of queryset
        'total_amount': total_amount,
    }

    # Render the template with the provided data
    return render(request, 'Main/order.html', data)



def productViewC(request):
    if request.user.product_set.exists():
        products = request.user.product_set.all()
        return render(request, 'Main/productViewC.html', {'products': products})
    else:
        return render(request, 'Main/productViewC.html', {'products': None})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product belongs to the currently logged-in user
    if product.owner_id != request.user:
        messages.error(request, 'You do not have permission to edit this product.')
        return redirect('seller_page')

    if request.method == 'POST':
        # Update product details based on the form data
        product.product_name = request.POST['productName']
        product.price = request.POST['productPrice']
        product.Discount = request.POST['productDiscount']
        product.total_quantity = request.POST['productStock1']
        product.Availability = request.POST['productStock']
        product.Product_information = request.POST['productInfo']
        product.model_Name = request.POST['model']
        product.Description = request.POST['description']
        product.Categories = request.POST['c']
        
        # Check if a new featured image is provided
        if 'productImages' in request.FILES:
            product.featured_image = request.FILES['productImages']

        # Save the changes
        product.save()

        # Update additional images if provided
        product_images = request.FILES.getlist('productImages1')
        for image in product_images:
            productImage = Product_Image()
            productImage.product = product
            productImage.Image_url = image
            productImage.save()

        messages.success(request, 'Product updated successfully.')
        return redirect('seller_page')

    # Render the edit product page with current product details
    categories = Category.objects.all()
    data = {
        "product": product,
        "categories": categories,
    }
    return render(request, "Main/edit_product.html", data)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the current user is the owner of the product
    if request.user == product.owner_id:
        # Delete the product and associated images
        product.delete()
        return redirect('seller_page')  # Replace 'seller_dashboard' with the URL name of your seller dashboard
    else:
        # If the current user is not the owner, handle the permission issue (you can customize this part)
        return render(request, 'error_page.html', {'error_message': 'Permission Denied'})

def bill_invoice(request):
    # Fetch the latest order for the logged-in user (or implement your logic)
    # order = Order.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)

    # Assuming you want to fetch the latest order
    order = orders.latest('created_at') if orders.exists() else None
    # print(order.total_amount)
    return render(request, 'Main/bill_invoice.html', {'order': order})

# views.py or other files

def admin_create_delivery_man(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone_number = request.POST.get('phone_number')
        
        try:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('admin_create_delivery_man')
            
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Assign the role of Delivery Man
            user.userRole = 'Delivery Man'
            user.save()
            
            # Create the user profile with address, city, state, and phone number
            UserProfile.objects.create(user=user, address=address, city=city, state=state, phone_number=phone_number)
            
            messages.success(request, f'Delivery man {username} has been created successfully.')
            return redirect('adminDash')  # Redirect to admin dashboard or any other appropriate page
        
        except IntegrityError:
            messages.error(request, 'An error occurred while creating the user.')
            return redirect('admin_create_delivery_man')
    
    return render(request, 'Main/admin_create_delivery_man.html')

def assign_delivery(request):
    # Assuming you have a form submission to assign delivery men to orders
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        delivery_man_id = request.POST.get('delivery_man_id')

        try:
            order = Order.objects.get(id=order_id)
            delivery_man = User.objects.get(id=delivery_man_id)
            order.delivery_man = delivery_man
            order.save()
            return redirect('assign_delivery')  # Redirect to the same page after assigning
        except Order.DoesNotExist:
            # Handle the case where the order does not exist
            pass

    # Retrieve orders without a delivery man assigned
    orders = Order.objects.all()
    # Retrieve all delivery men (users with the appropriate role, e.g., 'Delivery Man')
    delivery_men = User.objects.filter(userRole='Delivery Man')

    # Pass the orders without a delivery man and the delivery men to the template
    return render(request, 'Main/assign_delivery.html', {'orders': orders, 'delivery_men': delivery_men})

def admin_Order(request):
    orders = Order.objects.all()  
    return render(request, 'Main/admin_Order.html', {'orders': orders})

def orders_with_delivery_man(request):
    # Retrieve orders with assigned delivery men
    orders_with_delivery_man = Order.objects.exclude(delivery_man=None)

    # Pass the orders to the template
    return render(request, 'orders_with_delivery_man.html', {'orders': orders_with_delivery_man})

def upload_image(request):
    if request.method == 'POST':
        image_data = request.FILES['image'].read()
        image = Image(image_data=image_data)
        image.save()
        return redirect('upload_success', image_id=image.id)  # Pass the image_id to the upload_success view
    return render(request, 'Main/upload_image.html')

def upload_success(request, image_id):
    return render(request, 'Main/upload_success.html', {'image_id': image_id}) 

def view_image(request, image_id):
    image = Image.objects.get(pk=image_id)
    response = HttpResponse(image.image_data, content_type='image/png')  # Adjust content type based on your image format
    return response


