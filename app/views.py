from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import JsonResponse
from .models import Product, OrderPlaced, Cart, Customer
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .forms import SignupForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  data = Product.objects.filter(category='TW')
#  return render(request, 'app/home.html', {'items':data})

class ProductView(View):
    def get(self, request):
        totalitem = 0
        bw = Product.objects.filter(category='BW')
        tw = Product.objects.filter(category='TW')
        mb = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'bottomwears': bw, 'topwears': tw, 'mobiles': mb, 'total_item': totalitem})


class Product_detail(DetailView):
    # template_name = 'app/productdetail.html'
    # model = Product
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart = Cart(user=user, product=product)
    cart.save()

    return HttpResponseRedirect('/cart/')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_data = Cart.objects.filter(user=user)
        print(cart_data)
        print()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.discount_price)
                amount += temp_amt
                total_amount = amount + shipping_amount
        return render(request, 'app/addtocart.html', {'cart_data': cart_data, 'total_amount': total_amount, 'amount': amount})
    else:
        return HttpResponseRedirect('/')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        user = request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.discount_price)
                amount += temp_amt
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': amount+shipping_amount
            }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        user = request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.discount_price)
                amount += temp_amt

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': amount+shipping_amount
            }
            return JsonResponse(data)



@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        user = request.user
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.discount_price)
                amount += temp_amt

            data = {
                'amount': amount,
                'total_amount': amount+shipping_amount
            }
            return JsonResponse(data)





def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'address': address})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data=='Oppo' or data=='Apple':
        mobiles =  Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discount_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discount_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})

def laptops(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')

    elif data == 'DELL' or data == 'HP' or data == 'Lenovo' or data == 'Apple' or data == 'ASUS':
        laptops =  Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discount_price__lt=10000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discount_price__gt=10000)

    return render(request, 'app/laptops.html', {'laptops': laptops})

def top_wears(request, data=None):
    if data == None:
        top_wears = Product.objects.filter(category='TW')
    elif data == 'Blazzerx' or data == 'Raymonds' or data == 'tshirt':
        top_wears = Product.objects.filter(category='TW').filter(brand=data)
    return render(request, 'app/topwears.html', {'tw': top_wears})

def bottom_wears(request, data=None):
    if data == None:
        bottom_wears = Product.objects.filter(category='BW')

    elif data == 'jens' or data == 'formal' or data == 'lower':
        bottom_wears = Product.objects.filter(category='BW').filter(brand=data)
    return render(request, 'app/bottomwears.html', {'BW': bottom_wears})

class CustomerRegistration(FormView):
    template_name = 'app/customerregistration.html'
    form_class = SignupForm
    success_url = '/registration/'

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered Sucessfully!!')
        return HttpResponseRedirect('/registration/')

@login_required
def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        address = Customer.objects.filter(user=user)
        orders = Cart.objects.filter(user=user)

        amount = 0.0
        shipping_amount = 70.0

        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                temp_amt = (p.quantity * p.product.discount_price)
                amount += temp_amt
            total_amount = amount + shipping_amount
        return render(request, 'app/checkout.html', {'address': address, 'orders': orders, 'total_amount': total_amount})
    else:
        return HttpResponseRedirect('/')
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            nam = form.cleaned_data['name']
            loc = form.cleaned_data['locality']
            cit = form.cleaned_data['city']
            stat = form.cleaned_data['state']
            zipcod = form.cleaned_data['zipcode']
            fm = Customer(name=nam, locality=loc, city=cit, state=stat, zipcode=zipcod, user=usr)
            fm.save()
            messages.success(request, 'Congratulations ! Profile Updated Succcessfully')

        return HttpResponseRedirect('/profile/')

