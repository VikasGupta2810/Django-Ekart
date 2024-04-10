from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import Product,Cart,Order
from django.db.models import Q 
import random
import razorpay
from django.http import HttpResponse


# Create your views here.

def contact(request):
    return HttpResponse("This is contact page")

def home(request):
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['products']=p
   # userid=request.user.id
   # print("id of logged in user",userid)
   # print("result",request.user.is_authenticated)
    return render(request,'index.html',context)

def edit(request,rid):
    print("Id to be edited is",rid)
    return HttpResponse("id to be edited is:"+rid)

def del1(request,pid):
    print("Id to be deleted is",pid)
    return HttpResponse("Id to be deleted is:"+pid)

def newhome(request):
    return render(request,'index.html')

class SimpleView(View):
    def get(self,request):
        return HttpResponse("Hello world!")

class NewView(View):
    def get(self,request):
        return HttpResponse("This is His view")
    
class OldView(View):
    def get(self,request):
        return HttpResponse("This is Old view")
    
def page2(request):
    return redirect('/page2')

def page1(request):
    return render(request,'index.html')

def oldpath(request):
    return redirect('/oldpath')

def newpath(request):
    return render(request,'new.html')

def hello(request):
    context={}
    context['name']='yashmahi'
    return render(request,'hello.html',context)
    
def city(request):
    newcont={}
    newcont['city']='pune'
    return render(request,'hello.html',newcont)

def number(request):
    numb={}
    numb['x']=90
    numb['y']=70
    numb['z']=100
    numb['list']=[10,20,30,40,50]
    return render(request,"hello.html",numb)

def prod(request):
    cont={}
    cont['product']=[
        {'id':1,'name':'samsung','cat':'mobile','price':20000},
        {'id':2,'name':'jeans','cat':'clothes','price':4000},
        {'id':3,'name':'adidas','cat':'shoes','price':14000},
        {'id':4,'name':'vivo','cat':'mobile','price':18000}
    ]
    return render(request,"hello.html",cont)

def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            context['errormsg']="Field cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errormsg']="Password didn't match"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=uname,password=upass,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User added successfully"
                return render(request,'register.html',context)
            except Exception:
                   context['errormsg']="User Already Aadded"
                   return render(request,'register.html',context)
    else:
         return render(request,'register.html')

def user_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context['errormsg']="Field cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass) #here authenticate is used to check whether the login password&username are same while registering.
            print(u)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errormsg']="Invalid username and passowrd"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect("/home")

def productdetail(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_deatils.html',context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'   

    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def cart(request):
    return render(request,'cart.html')

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    print(p)
    context={}
    context['products']=p
  
    return render(request,'index.html',context)


def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #print(pid)
        #print(userid)
        #return HttpResponse("id fetched Successfully")
        u=User.objects.filter(id=userid)
        print(u[0])
        p=Product.objects.filter(id=pid)
        print(p[0])
        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save() 
        return HttpResponse("product added to cart")
    else:
        return redirect('/login2')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np=len(c)
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    context={}
    context['products']=c
    context['n']=np
    context['total']=s
    return render(request,'cart.html',context)

def updateqty(request,qv,cid):
    #print(type(qv))
    c=Cart.objects.filter(id=cid)
    #print(c)
    #print(c[0])
    #print(c[0].qty)
    #return HttpResponse("qty fetched")
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
           t=c[0].qty-1
           c.update(qty=t)     
    return redirect('/viewcart')          


def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print("Order id is:",oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)   
    for x in orders:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    context={}
    context['products']=orders
    context['n']=np
    context['total']=s
    return render(request,'place_order.html',context)    


def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_5e81Zc8ASlT1l6", "GYt1T7fsmZ3SxDFxSTJMSIiM"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request ,"pay.html",context)
    






















client = razorpay.Client(auth=("rzp_test_5e81Zc8ASlT1l6", "GYt1T7fsmZ3SxDFxSTJMSIiM"))