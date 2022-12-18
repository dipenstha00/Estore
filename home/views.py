import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.


class BaseView(View):
    context = {'categories': Category.objects.all(), 'brand': Brand.objects.all(),
               'sales': Product.objects.filter(labels='sales')}


class HomeView(BaseView):
    def get(self, request):
        self.context
        username = request.user.username
        self.context['categories'] = Category.objects.all()
        self.context['subcategories'] = SubCategory.objects.all()
        self.context['brand'] = Brand.objects.all()
        self.context['slider'] = Sider.objects.all()
        self.context['ads'] = Ads.objects.all()
        self.context['hot'] = Product.objects.filter(labels='HOT')
        self.context['new'] = Product.objects.filter(labels='NEW')
        self.context['sales'] = Product.objects.filter(labels='SALE')
        self.context['reviews'] = Reviews.objects.all()
        self.context['about'] = About.objects.all()
        self.context['carts'] = Cart.objects.filter(username=username, checkout=False)

        return render(request, 'index.html', self.context)


class Categories(BaseView):
    def get(self, request, slug):
        self.context
        ids = Category.objects.get(slug=slug).id
        self.context['category_product'] = Product.objects.filter(category_id=ids)
        return render(request, 'category.html', self.context)


class ProductView(BaseView):
    def get(self, request, slug):
        self.context
        self.context['product_details'] = Product.objects.filter(slug=slug)
        self.context['product_reviews'] = ProductReviews.objects.filter(slug=slug)
        return render(request, 'product-detail.html', self.context)


class SearchView(BaseView):
    def get(self, request):
        self.context
        query = request.GET.get('query')
        if not query:
            return redirect('/')
        self.context['search_product'] = Product.objects.filter(name__contains = query)
        return render(request, 'search.html', self.context)


def reviews(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        review = request.POST['review']
        star = request.POST['star']
        slug = request.POST['slug']
        data = Reviews.objects.create(
            name=name,
            email=email,
            review=review,
            star=star,
            slug=slug,
        )
        data.save()
        return redirect(f'/product-detail/{{slug}}')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
                return redirect('/signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
                return redirect('/login')
        else:
            messages.error(request, "The password don't match!Please enter the same password.")
            return redirect('/signup')
    return render(request, 'account.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,
                            password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome {{user.username}}")
            return redirect('/')
        else:
            messages.error(request, "Wrong credentials! Please enter correct credentials")
            return redirect('login')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/')


class CartView(BaseView):
    def get(self, request):
        self.context
        username = request.user.username
        self.context['cart_views'] = Cart.objects.filter(username=username, checkout=False)
        c = 0
        total_price = 0
        for i in Cart.objects.filter(username=username, checkout=False):
            x = Cart.objects.filter(username=username, checkout=False)[c].total
            total_price = total_price + x
            c = c + 1

        self.context['total_price'] = total_price
        return render(request, 'cart.html', self.context)


def add_to_cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, username=username, checkout=False).exists():
        quantity = Cart.objects.get(slug=slug, username=username, checkout=False).quantity
        price = Product.objects.get(slug=slug).price
        discounted_price = Product.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price
        quantity = quantity + 1
        total = quantity * price
        Cart.objects.filter(slug=slug, username=username, ).update(quantity=quantity, total=total)
        messages.success(request, 'Added to Cart')
        return redirect('/')

    else:
        price = Product.objects.get(slug=slug).price
        discounted_price = Product.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price
        data = Cart.objects.create(
            slug=slug,
            username=username,
            total=original_price,
            items=Product.objects.filter(slug=slug)[0],
        )
        data.save()
        return redirect('/')


def remove_cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, username=username, checkout=False).exists():
        quantity = Cart.objects.get(slug=slug, username=username, checkout=False).quantity
        price = Product.objects.get(slug=slug).price
        discounted_price = Product.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price
        quantity = quantity - 1
        total = quantity * price
        Cart.objects.filter(slug=slug, username=username, ).update(quantity=quantity, total=total)
        return redirect('/cart')


def delete_cart(request, slug):
    username = request.user.username
    Cart.objects.filter(slug=slug, username=username, checkout=False).delete()
    messages.info(request, "Removed from cart!")
    return redirect('/cart')



def get_cart_count(request):
    username = request.user.username
    return Cart.objects.filter(username=username, checkout=False).count()


def remove_item_cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, username=username, checkout=False).exists():
        quantity = Cart.objects.filter(slug=slug, username=username, checkout=False).quantity
        price = Cart.objects.get(slug=slug).price
        discounted_price = Cart.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price
        if quantity > 1:
            quantity = quantity - 1
        total = quantity * original_price
        Cart.objects.filter(slug=slug, username=username).update(quantity=quantity, total=total)
        return redirect('/cart')


class WishlistView(BaseView):
    def get(self, request):
        self.context
        username = request.user.username
        self.context['wishlist_views'] = Wishlist.objects.filter(username=username)
        return render(request, 'wishlist.html', self.context)


def add_to_wishlist(request, slug):
    username = request.user.username
    if Wishlist.objects.filter(username=username, slug=slug).exists():
        return redirect('/wishlist')
    else:
        price = Product.objects.get(slug=slug).price
        discounted_price = Product.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            true_price = discounted_price
        else:
            true_price = price
        data = Wishlist.objects.create(
            username=username,
            slug=slug,
            trueprice=true_price,
            items=Product.objects.filter(slug=slug)[0],
        )
        data.save()
        return redirect('/wishlist')


def delete_wishlist(request, slug):
    username = request.user.username
    Wishlist.objects.filter(username=username, slug=slug).delete()
    return redirect('/wishlist')


def contact(request):
    msg = About.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        company = request.POST['company']
        message = request.POST['message']
        data = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            company=company,
            message=message
        )
        data.save()
    return render(request, 'contact.html', {'info': msg})


class CheckoutView(BaseView):
    def get(self, request):
        self.context
        username = request.user.username
        self.context['carts'] = Cart.objects.filter(username=username, checkout=False)
        return render(request, 'checkout.html', self.context)


def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.username = request.user.username
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.province = request.POST.get('province')
        neworder.district = request.POST.get('district')
        neworder.zipcode = request.POST.get('zipcode')
        neworder.city = request.POST.get('city')

        neworder.payment = request.POST.get('payment_mode')

        cart = Cart.objects.filter(username=request.user.username)
        cart_total_price = 0

        for item in cart:
            if item.items.discounted_price > 0:
                true_price = item.items.discounted_price
            else:
                true_price = item.items.price
            cart_total_price = cart_total_price + true_price * item.quantity
        neworder.total = cart_total_price
        trackno = 'estore' + str(random.randint(111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'estore' + str(random.randint(111111, 9999999))
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(username=request.user.username)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.items,
                price=true_price,
                quantity=item.quantity,

            )
            # To decrease the product quantity from available stock
            orderproduct = Cart.objects.filter(id=item.id).first()
            orderproduct.quantity = orderproduct.quantity - item.quantity
            orderproduct.save()

        # To clear user's Cart
        Cart.objects.filter(username=request.user.username).delete()

        messages.success(request, "Your order has been placed successfully")
    return redirect('/')


class OrderView(BaseView):
    def get(self,request):
        self.context
        username=request.user.username
        self.context['order_list'] = Order.objects.filter(username=username)
        
        return render(request, 'order.html', self.context)


def vieworder(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(username=request.user.username).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={'order':order, 'orderitems':orderitems}

    return render(request, 'vieworder.html', context)