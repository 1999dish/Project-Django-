from django.shortcuts import render,redirect

from datetime import datetime
from .models import Product,Contact,Orders
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from math import ceil

# Create your views here.
from django.http import HttpResponse

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def signup(request):
    if request.method =="POST":
        email=request.POST.get("email")
        name=request.POST.get("name")
        username=request.POST.get("username")
        password=request.POST.get("password")
        password2=request.POST.get("password2")
        if password!=password2 :
            messages.error(request, 'Password should be same')
            return redirect('/signup')
        if len(username)<4:
            messages.error(request, 'Username too short')
            return redirect('/signup')   
        if len(password)<4:
            messages.error(request, 'Password too short should not have less than 8 characters')
            return redirect('/signup')       
         


        myuser=User.objects.create_user(username,email,password)
        myuser.first_name=name
        myuser.save()
    
        
        return HttpResponse("'Your  my awesome home account created'")
    else:
        return render(request, 'shop/signup.html')
        return HttpResponse("404-Not Found")
def loginhandle(request):
    if request.method =="POST":
        loginname=request.POST.get("loginname")
        loginpassword=request.POST.get("loginpassword")
        print(loginname,loginpassword)
        user = authenticate(username=loginname, password=loginpassword)
        print(user)
        if user is not None:
            login(request,user)
            messages.success(request, 'Successfully Logged In')
            return redirect('/shop')

        else:
            messages.error(request, 'Invalid User')
            return redirect('/login')

    return render(request, 'shop/login.html')
def handlelogout(request):
    logout(request) 
    messages.success(request, 'Successfully Logged Out')   
    return redirect('/shop')

def contact(request):
    
    if request.method =="POST":
        email=request.POST.get("email")
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        desc=request.POST.get("desc")
        service=request.POST.get("service")
        contact=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today(),service=service)
        contact.save()
    
    
        messages.success(request, 'Your request has been received.We will contact you soon!')
    return render(request, 'shop/contact.html')

def tracker(request):
    return render(request, 'shop/tracker.html')
def match(query,item):
    if query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET['search']
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if match(query,item)]
        if len(prod)>0:
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
        params = {'allProds':allProds}
    if len(allProds)==0 or len(query)<4:
        messages.success(request, ' Oops! No results found enter a valid search!')
        return redirect('/shop')
    else:
        return render(request, 'shop/search.html', params)
    


    #return render(request, 'shop/search.html',params)

def productView(request,myid):
    product = Product.objects.filter(id=myid)


    return render(request, 'shop/prodView.html', {'product':product[0]})

def checkout(request,myid):
    if request.method=="POST":
        ordername = request.POST.get('ordername', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        orderid = request.POST.get('orderid', '')
        phone = request.POST.get('phone', '')
        order = Orders(ordername=ordername, name=name, email=email, address=address, city=city,
                       state=state, orderid=orderid, phone=phone)
        
        order.save()
        messages.success(request, 'Your request has been received!')
    

    product = Product.objects.filter(id=myid)
    return render(request, 'shop/checkout.html', {'product':product[0]})
   
