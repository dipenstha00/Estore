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
        self.context['categories'] = Category.objects.all()
        self.context['subcategories'] = SubCategory.objects.all()
        self.context['brand'] = Brand.objects.all()
        self.context['slider'] = Sider.objects.all()
        self.context['ads'] = Ads.objects.all()
        self.context['hot'] = Product.objects.filter(labels='HOT')
        self.context['new'] = Product.objects.filter(labels='NEW')
        self.context['sales'] = Product.objects.filter(labels='SALE')
        self.context['reviews'] = Reviews.objects.all()

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
        for x in Cart.objects.filter(username=username, checkout=False):
            x = Cart.objects.filter(username=username, checkout=False)[c].total
            total_price = total_price + x
            c = c+1

        self.context['total_price'] = total_price
        return render(request, 'cart.html', self.context)


def add_to_cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, username=username, checkout=False).exists():
        quantity = Cart.objects.get(slug=slug, username=username, checkout=False).quantity
        price = Product.objects.get(slug=slug).price
        discounted_price =Product.objects.get(slug=slug).discoutned_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price
        quantity = quantity + 1
        total = quantity * price
        Cart.objects.filter(slug=slug, username=username,).update(quantity=quantity, total=total)
        return redirect('/cart')
    else:
        price = Product.objects.get(slug=slug).price
        discounted_price = Product.objecsts.get(slug=slug).discounted_price
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
        return redirect('/cart')


