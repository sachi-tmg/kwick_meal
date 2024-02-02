from django.forms import ValidationError
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from customer_orders.models import Customer, Food_Item,Food,Order,Reservations
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from .models import Customer
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.contrib.auth import logout,login,authenticate
import requests
import json



# Create your views here.

def SignupPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the phone number is already in use
        if Customer.objects.filter(phone_no=phone).exists():
            messages.error(request, 'Phone number is already in use. Please choose a different one.')
            return redirect('signup')  # Redirect back to the signup page

        # Check if the email is already in use
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please use a different email address.')
            return redirect('signup')  # Redirect back to the signup page

        # If the phone number and email are not in use, create a new customer
        hashed_password = (password)
        my_customer = Customer(customer_name=name, phone_no=phone, email=email, password=hashed_password)
        my_customer.save()
        user=User.objects.create(username=name, email=email)
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'signup.html')

  # Adjust the import path based on your project structure

def LoginPage(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        error_message = None

        # Check if a customer with the provided phone_no and password exists
        customer_exists = Customer.objects.filter(phone_no=phone_no, password=password).first()

        if customer_exists:
            user=authenticate(request, username=customer_exists.customer_name,password=password)
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong Phone no or Password.')

        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def HomePage(request):
    user_email = request.user.email

    return render(request,'home.html', context={'user_email':user_email})

def Menu(request):
    food_item = Food.objects.all()
    food_list = Food_Item.objects.all()
    if request.user.is_authenticated:
        print (request.user)

   
    return render(request, 'menu.html', context={'food_item':food_item, 'food_list':food_list})

def filter_food(request, id):
    food_item = Food_Item.objects.prefetch_related('food_set').filter(id=id).first()
    food_item=food_item.food_set.all()
    food_list = Food_Item.objects.all()


    return render(request,'menu.html', context={'food_item':food_item, 'food_list':food_list})

def order(request, id):

    food= Food.objects.get(id=id)
    if request.user.is_authenticated:
        user = Customer.objects.filter(email = request.user.email).first()
        print(request.user.email)

    quantity = request.POST.get('quantity')
    order_date = datetime.now()
    Order.objects.create(customer = user, food= food, quantity= int(quantity), date= order_date, total = int(quantity)*food.price)
    food_item = Food.objects.all()
    food_list = Food_Item.objects.all()


    return render(request,'menu.html', context={'food_item':food_item, 'food_list':food_list})




def Cart_view(request):
    # Get the current user's email
    user_email = request.user.email

    # Get the current date and time
    current_datetime = datetime.now()

    # Filter orders based on user email and today's date
    filtered_orders = Order.objects.filter(
        customer__email=user_email,
        date__date=current_datetime.date()
    )
    total_price = sum(order.total for order in filtered_orders)


    return render(request, 'cart.html', {'filtered_orders': filtered_orders, 'total_price':total_price})

def AboutPage(request):
    return render(request,'about.html')

def Blog(request):
    return render(request,'blog.html')


def verify_payment(request):
    data = request.POST
    product_id = data['product_identity']
    token = data['token']
    amount = data['amount']

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
    "token": token,
    "amount": amount
    }
    headers = {
    "Authorization": "Key test_secret_key_2e13ded0a52640a9b945de97955e3370"
    }
    

    response = requests.post(url, payload, headers = headers)
    
    response_data = json.loads(response.text)
    status_code = str(response.status_code)

    print(response_data)
    if status_code == '400':
        response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
    return response

def Reservation(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('fname')
            email = request.POST.get('email')
            date = request.POST.get('date')
            time = request.POST.get('time')
            number_of_guest = request.POST.get('number_of_guest')

            Reservations.objects.create(name=name,email=email, date=date, time=time, number_of_guest=number_of_guest)


            # Check if the fields are empty
            if not name or not email or not number_of_guest or not date or not time:
                messages.error(request, 'All fields are required. Please fill in all the fields.')
                return redirect('reservation')  # Redirect back to the signup page
            if date:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()

        except ValidationError as e:
            messages.error(request, 'All fields are required. Please fill in all the fields.')
            return redirect('reservation') 

    return render(request,'reservation.html')
