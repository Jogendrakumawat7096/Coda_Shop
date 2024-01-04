from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import User,Product,Whishlist,Cart,Order,Contact
import random
import requests
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe


stripe.api_key = "sk_test_51ORGX1SCMGvokPZBpdiuiQgSvwoXj86d62yHPqJtleFuVktMBV8ULi5gdyZrLBl1Q9aolktwuwnLO4GD4OrXllhG00jINmbqGm"

YOUR_DOMAIN = "http://jogendra7773.pythonanywhere.com"
@csrf_exempt
def create_checkout_session(request):
    
    data = json.loads(request.body.decode('utf-8'))
    amount = int(data['amount'])
 
    final_amount = amount*0

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Checkout Session Data',
                    },
                    'unit_amount': final_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )

        
    except Exception as e:
        return JsonResponse({'error': str(e)})

    return JsonResponse({'id': session.id})







def success(request):
    
    cart_items = Cart.objects.filter(payment_status=False)
    user = User.objects.get(email=request.session['email'])
    for cart_item in cart_items:
        Order.objects.create(
            buyer=user,
            product=cart_item.product,
            product_price=cart_item.product_price,
            product_qty=cart_item.product_qty,
            total_price=(cart_item.total_price) + 199,
        )
        # Delete the current cart item
        cart_item.delete()

    total_cart = Cart.objects.filter(buyer=user).count()
    request.session['total_cart'] = total_cart 
    return render(request,"success.html")

def cancel(request):
    return render(request,"cancel.html")






def index(request):
    product=Product.objects.all()
    return render(request,"index.html",{'product':product})


def seller_index(request):
    seller=User.objects.get(email=request.session['email'])
    products=Product.objects.filter(seller=seller)
    return render(request,"seller-index.html",{'products':products})

def product(request,cat):
    if cat=='all':
        product=Product.objects.all()
        return render(request,"product.html",{'product':product})
    elif cat=='Women':
        product=Product.objects.filter(product_category='Women')
        return render(request,"product.html",{'product':product})
    elif cat=='Men':
        product=Product.objects.filter(product_category='Men')
        return render(request,"product.html",{'product':product})
    elif cat=='kids':
        product=Product.objects.filter(product_category='kids')
        return render(request,"product.html",{'product':product})

        
def shoping_cart(request):
    return render(request,"shoping-cart.html")

def blog(request):
    return render(request,"blog.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method=="POST":
        Contact.objects.create(
            email=request.POST['email'],
            message=request.POST['msg']
        )
        msg="Message Sent Successfully"
        return render(request,"contact.html",{'msg':msg})
    return render(request,"contact.html")

def product_detail(request):
    return render(request,"product-detail.html")

def signup(request):
    try:
        request.session['email']
        msg="Already Login"
        return render(request,"index.html",{'msg':msg})
    except:
        if request.method=="POST":
            try:
                User.objects.get(email = request.POST['email'])
                msg = "Email Is Already Registered , Please Enter Another Email Id"
                return render(request,"signup.html",{'msg':msg})
                
            except:
                if request.POST['password']==request.POST['cpassword']:
                    User.objects.create(
                        user_type=request.POST['usertype'],
                        name=request.POST['name'],
                        email=request.POST['email'],
                        mobile=request.POST['mobile'],
                        address=request.POST['address'],
                        image = request.FILES['profile_picture'],
                        password=make_password(request.POST['password']),                                        
                    )
                    msg = "Sign Up Successfully"
                    return render(request,"login.html",{'msgs':msg}) 
                else:
                    msg = "Password or Confirm Password Does Not Matched"
                    return render(request,"signup.html",{'msg':msg})     
        else:   
            return render(request,"signup.html")

def login(request):
    try:
        request.session['email']
        msg="Already Login"
        return render(request,"index.html",{'msg':msg})
    except:          
        if request.method=="POST":
            try:
                user = User.objects.get(email = request.POST['email'])
                
                if check_password(request.POST['password'],user.password):
                    if user.user_type=="Buyer":
                        request.session['email'] = user.email
                        request.session['name']=user.name
                        request.session['address']=user.address
                        
                        request.session['image'] = user.image.url if user.image else None  
                        buyer = User.objects.get(email=request.session['email'])
                        total_wish = Whishlist.objects.filter(buyer=buyer).count()
                        request.session['total_wish'] = total_wish
                        total_cart = Cart.objects.filter(buyer=buyer).count()
                        request.session['total_cart'] = total_cart
                        
        
                        return redirect('index')
                    else:
                        request.session['email'] = user.email
                        request.session['name']=user.name
                        request.session['image'] = user.image.url if user.image else None                
                        return render(request,"seller-index.html")
                else:
                    msg ="password Incorrect"
                    return render(request,"login.html",{'msg':msg})
            except:
                msg ="Email Not Registered"
                return render(request,"login.html",{'msg':msg})      
                
        else:      
            return render(request,"login.html")
def forgot_password(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        user = User.objects.get(mobile=mobile)

        if user:
            otp = random.randint(1000, 9999)
            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {
                "authorization": "VlO5sarhU8T76cPG0qMmvxHKYBiJ4DRZInEzfAF3L1pudekWCQf1t4D63AikUrC57TRZdJ8QMgGWbHYS",
                "variables_values": str(otp),
                "route": "otp",
                "numbers": mobile
            }
            headers = {'cache-control': "no-cache"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            
            request.session['mobile'] = mobile
            uotp = make_password(str(otp))
            return render(request, "otp.html", {'otp': uotp})
        else:
            msg = "Mobile Number Not Exists"
            return render(request, "forgot-password.html", {'msg': msg})

    return render(request, "forgot-password.html")

    
def verify_otp(request):
    otp = request.POST['otp']
    if check_password(request.POST['uotp'],otp):
        return render(request,"new-password.html")
    else:
        msg = "Invalid otp"
        return render(request,"otp.html",{'msg':msg})

def new_password(request):
    if request.POST['new-password']==request.POST['cnew-password']:
        mobile= request.session['mobile']
        user = User.objects.get(mobile=mobile)
        user.password=make_password(request.POST['new-password'])
        user.save()
        return redirect('login')
    else:
        msg= "password and confirm password does not matched"  
        return render(request,"new-password.html",{'msg':msg})

def logout(request):
    user = User.objects.get(email = request.session['email'])
    if user.user_type=="Buyer":
        del request.session['email']
        del request.session['image']
        del request.session['name']
        del request.session['total_cart']
        del request.session['total_wish']
        del request.session['address']
    else:
        del request.session['email']
        del request.session['image']
        del request.session['name']
    
          
    return render(request,"login.html")


def update_profile(request):
    user = User.objects.get(email = request.session['email'])
    if user.user_type=="Buyer":    
        return render(request,"update-profile.html",{'user':user})
    else:
        return render(request,"seller-update-profile.html",{'user':user})
    
def update_data(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        
        user.name = request.POST['name']
        user.mobile = request.POST['mobile']
        user.address = request.POST['address']
        
        if 'pimage' in request.FILES:
            user.image = request.FILES['pimage']
        
        user.save()
        request.session['image'] = user.image.url if user.image else None
        msg = "Profile update successful"
        if user.user_type=="Buyer":
            return render(request, "update-profile.html", {'msg': msg, 'user': user})
        else:
            return render(request, "seller-update-profile.html", {'msg': msg, 'user': user})            
    else:
        if user.user_type=="Buyer":
            return render(request, "update-profile.html",{'user':user})
        else:
            return render(request, "seller-update-profile.html",{'user':user})

            
    
def change_password(request):
    user = User.objects.get(email=request.session['email'])
    if request.method=='POST':        
        if check_password(request.POST['old-password'],user.password):
            if request.POST['new-password']==request.POST['cnew-password']:
                user.password=make_password(request.POST['new-password'])                
                user.save()
                return redirect('logout')
            else:
                msg= "password or confirm password not matched"
                if user.user_type=="Buyer": 
                    return render(request,"change-password.html",{'msg':msg})
                else:
                    return render(request,"seller-change-password.html",{'msg':msg})
                    
        else:
            msg= "old Password Does Not Matched"
            if user.user_type=="Buyer": 
                return render(request,"change-password.html",{'msg':msg})
            else:
                return render(request,"seller-change-password.html",{'msg':msg})
                
    else:
        if user.user_type=="Buyer":   
            return render(request,"change-password.html")
        else:
            return render(request,"seller-change-password.html")

def seller_add_product(request):
    
    seller=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        Product.objects.create(
            seller=seller,
            product_name=request.POST['product-name'],
            product_price=request.POST['product-price'],
            product_category=request.POST['product-category'],
            product_size=request.POST['product-size'],
            product_brand=request.POST['product-brand'],
            product_desc=request.POST['product-desc'],
            product_fimage=request.FILES['product-fimage'],
            product_bimage=request.FILES['product-bimage'],          
            
         
        )
        msg="Product Add SuccessFull"
        return render(request,"seller-add-product.html",{'msg':msg})
    else:   
        return render(request,"seller-add-product.html")

def seller_view_product(request):
    
    seller=User.objects.get(email=request.session['email'])
    products=Product.objects.filter(seller=seller)
    return render(request,"seller-view-product.html",{'products':products})


def seller_product_detail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,"seller-product-detail.html",{'product':product})

def seller_edit_product(request,pk):
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.product_name=request.POST['product-name']
        product.product_price=request.POST['product-price']
        product.product_category=request.POST['product-category']
        product.product_size=request.POST['product-size']
        product.product_brand=request.POST['product-brand']
        product.product_desc=request.POST['product-desc']
        try:
            product.product_fimage=request.FILES['product-fimage']
            product.product_bimage=request.FILES['product-bimage']
        except:
            pass 
        product.save()
        msg="Product Update Successfull"
        return render(request,"seller-edit-product.html",{'product':product,'msg':msg})
    else:
        return render(request,"seller-edit-product.html",{'product':product})
    
def seller_product_delete(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect('seller-view-product')

def product_detail(request, pk):
    try:
        whishlist_flag = False
        cart_flag = False
        
        buyer = User.objects.get(email=request.session['email'])
        product=Product.objects.get(pk=pk)

        try:
            Whishlist.objects.get(buyer=buyer, product=product)
            whishlist_flag = True
            
        except :
            pass

        if Cart.objects.filter(buyer=buyer, product=product).exists():
            cart_flag = True

        return render(request, "product-detail.html", {'product': product, 'whishlist_flag': whishlist_flag, 'cart_flag': cart_flag})
    except:
        product=Product.objects.get(pk=pk)
        return render(request, "product-detail.html", {'product': product,})

def add_to_cart(request, pk):
    try:
        product=Product.objects.get(pk=pk)
        user = User.objects.get(email=request.session['email'])
        product_qty = 1
        total_price = product.product_price * product_qty
        if not Cart.objects.filter(buyer=user, product=product).exists():
            Cart.objects.create(
                buyer=user,
                product=product,
                product_price=product.product_price,
                product_qty=product_qty,
                total_price=total_price,
                
            )
            total_cart = Cart.objects.filter(buyer=user).count()
            request.session['total_cart'] = total_cart 

            cart_flag = False
            try:
                Cart.objects.get(buyer=user, product=product)
                cart_flag = True
            except:
                pass
            return render(request, "product-detail.html",{'product':product,'cart_flag':cart_flag})
        else:
            cart_flag = False
            try:
                Cart.objects.get(buyer=user, product=product)
                cart_flag = True
            except:
                pass
            return render(request, "product-detail.html",{'product':product,'cart_flag':cart_flag})
    except:
        return redirect('login')

def shoping_cart(request):
    try:
        buyer = User.objects.get(email=request.session['email'])
        carts= Cart.objects.filter(buyer=buyer)

        sub_price = sum(carts.values_list('total_price', flat=True))
        return render(request, "shoping-cart.html",{'carts':carts,'sub_price':sub_price})
    except:
        return redirect('login')
    

def add_to_whishlist(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        buyer = User.objects.get(email=request.session['email'])
        if not Whishlist.objects.filter(buyer=buyer, product=product).exists():
            Whishlist.objects.create(buyer=buyer, product=product)
            total_wish = Whishlist.objects.filter(buyer=buyer).count()
            request.session['total_wish'] = total_wish
            return redirect('product-detail',pk=product.pk)
        else:
            return redirect('product-detail',pk=product.pk)
    except:
        return redirect('login')


def whishlist(request):  
    buyer = User.objects.get(email=request.session['email'])
    whishlists=Whishlist.objects.filter(buyer=buyer)
    return render(request, "whishlist.html", {'whishlists':whishlists})
    
def remove_whishlist(request,pk):
    product = Product.objects.get(pk=pk)
    buyer = User.objects.get(email=request.session['email'])
    whishlists=Whishlist.objects.filter(buyer=buyer,product=product)
    whishlists.delete()
    total_wish = Whishlist.objects.filter(buyer=buyer).count()
    request.session['total_wish'] = total_wish
    return render(request, "product-detail.html", {'product': product})


def cart_qty(request, pk):
    product = Product.objects.get(pk=pk)
    user = User.objects.get(email=request.session.get('email'))
    cart = Cart.objects.get(product=product, buyer=user)
    
    cart.product_qty +=1
    cart.total_price=cart.product_qty*product.product_price    
    cart.save()
    return redirect('shoping-cart')

def cart_qty_minus(request, pk):
    product = Product.objects.get(pk=pk)
    user = User.objects.get(email=request.session.get('email'))
    cart = Cart.objects.get(product=product, buyer=user)    
    cart.product_qty -=1
    cart.total_price=cart.product_qty*product.product_price    
    cart.save()
    if cart.product_qty==0:
        cart.delete()
    return redirect('shoping-cart')                                                          

def remove_cart(request, pk):
    product = Product.objects.get(pk=pk)
    user = User.objects.get(email=request.session.get('email'))
    cart = Cart.objects.get(product=product, buyer=user)
    cart.delete() 
    total_cart = Cart.objects.filter(buyer=user).count()
    request.session['total_cart'] = total_cart 
    return redirect('shoping-cart')

def customer_order(request):
    buyer = User.objects.get(email=request.session['email'])
    orders= Order.objects.filter(buyer=buyer)
    return render(request,"customer-order.html",{'orders':orders})

def customer_cancel_order(request,pk):
    order = Order.objects.get(pk=pk)
    order.order_status = "cancel"
    order.save()

    return redirect('customer-order')



def seller_view_order(request):
    try:
        user = User.objects.get(email=request.session['email'])
        products = Product.objects.filter(seller=user)
        orders = Order.objects.filter(product__in=products)
        return render(request, "seller-order.html", {'orders': orders})
    except User.DoesNotExist:
        return HttpResponse("User not found")
    except Product.DoesNotExist:      
        return HttpResponse("No products found for the user")



def seller_cancel_order(request,pk):
    order = Order.objects.get(pk=pk)
    order.order_status = "cancel"
    order.save()

    return redirect('seller-view-order')

def seller_accept_order(request,pk):
    order = Order.objects.get(pk=pk)
    order.order_status = "Accepted"
    order.save()

    return redirect('seller-view-order')

def seller_shipped_order(request,pk):
    order = Order.objects.get(pk=pk)
    order.order_status = "Shipped"
    order.save()

    return redirect('seller-view-order')





    