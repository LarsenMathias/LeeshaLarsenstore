from django.shortcuts import render,redirect
from .models import order,Product,cartitem,User,UserProfile
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.contrib import messages
from .forms import UserprofileModelform,RegistrationForm
import requests
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful. You can now log in.')
            return redirect('login')  # Replace 'login' with your login URL
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == 'password1' or field == 'password2':
                        messages.error(request, f'Invalid password: {error}')
                    else:
                        messages.error(request, f'Error in field {field}: {error}')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})
def home(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    products=Product.objects.all()
    user = request.user  # Get the authenticated user
    cart_items = cartitem.objects.filter(order__user=user)
    total_items = 0
    for item in cart_items:
        total_items+=item.quanity
    context={'products':products,
             'total_items':total_items}
    # Handle cases where the request method is not POST
    return render(request,'index.html',context)
from django.contrib.auth.decorators import login_required
 # This decorator ensures the user is authenticated
def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user  # Get the authenticated user
    cart_items = cartitem.objects.filter(order__user=user)
    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quanity
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request,"cart.html",context)# Redirect to the cart page or any other page you want




def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = UserprofileModelform(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Your order has been placed successfully")
    else:
        form = UserprofileModelform(instance=profile, initial={
            'name': profile.name,
            'email': profile.email,
            'address': profile.address,
            'pincode': profile.pincode,
            'city': profile.city,
            'state': profile.state,
        })

    return render(request, 'checkout.html', {'form': form})
def user_login(request):
    if request.method=="POST":
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            user=form.get_user()
            auth_login(request,user)
            return redirect('home')
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})
def updateItem(request):
    data = json.loads(request.body)
    productID = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productID)
    customer = request.user
    product = Product.objects.get(id=productID)
    ordered, created = order.objects.get_or_create(user=customer)

    cart_item, cart_item_created = cartitem.objects.get_or_create(order=ordered, product=product)

    if action == 'add':
        cart_item.quanity += 1
    elif action == 'remove':
        cart_item.quanity -= 1

    # Save the changes to the cart_item
    cart_item.save()

    # Check if the quantity is less than or equal to 0, and if so, delete the cart item
    if cart_item.quanity <= 0:
        cart_item.delete()

    return JsonResponse('Item was added', safe=False)
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            # Handle the case where the product doesn't exist
            return redirect('product_not_found')

        user = request.user

        # Check if the user has an incomplete order, if not, create one
        order_item, order_created = order.objects.get_or_create(user=user, completed=False)

        # Check if the product is already in the user's cart
        cart_item, cart_item_created = cartitem.objects.get_or_create(order=order_item, product=product)

        if not cart_item_created:
            # The product is already in the cart, increment the quantity
            cart_item.quanity += 1
            cart_item.save()

        return redirect('cart')  # Redirect to the cart page or a success page

    # Handle cases where the request method is not POST
    return redirect('invalid_request_method')