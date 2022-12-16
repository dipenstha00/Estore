from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=300)
    slug = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=300)
    slug = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.name


STOCK = (('in stock', 'In Stock'), ('out of stock', 'Out of Stock'))
LABELS = (('HOT', 'HOT'), ('NEW', 'NEW'), ('SALE', 'SALE'))


class Product(models.Model):
    name = models.CharField(max_length=300)
    slug = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.ImageField(upload_to='media')
    stock = models.CharField(max_length=100, choices=STOCK)
    labels = models.CharField(max_length=100, choices=LABELS)
    description = models.TextField(blank=True)
    specification = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Sider(models.Model):
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=300, default='')
    descript = models.TextField(default='')
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.name


class Ads(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media')
    rank = models.IntegerField()

    def __str__(self):
        return self.name


class Reviews(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media')
    post = models.CharField(max_length=300, default='')
    feedback = models.TextField()

    def __str__(self):
        return self.name


class ProductReviews(models.Model):
    name = models.CharField(max_length=300)
    slug = models.CharField(max_length=500)
    email = models.EmailField(max_length=100)
    review = models.TextField()
    star = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Cart(models.Model):
    username = models.CharField(max_length=300)
    slug = models.CharField(max_length=500)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField()
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return self.items.name


class Wishlist(models.Model):
    username = models.CharField(max_length=300)
    slug = models.CharField(max_length=500)
    trueprice = models.IntegerField(default=0)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.items.name


class About(models.Model):
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=300)


class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    subject = models.CharField(max_length=500)
    company = models.CharField(max_length=300)
    message = models.TextField()

    def __str__(self):
        return self.name


STATES = (
    ('province no.1 ', 'Province No. 1'),
    ('madesh province', 'Madhesh Province'),
    ('bagmati province', 'Bagmati Province'),
    ('gandaki province', 'Gandaki Province'),
    ('lumbini province', 'Lumbini Province'),
    ('karnali province', 'Karnali Province'),
    ('mahakali province', 'Mahakali Province')
)
PAYMENT_METHOD = (
    ('cash on delivery', 'Cash on Delivery'),
    ('paypal', 'Via PayPal'),
)

STATUS = (
    ('Pending', 'Pending'),
    ('Shipping', 'Shipping'),
    ('Delivered', 'Delivered')
)


class Order(models.Model):
    username = models.CharField(max_length=300,default='')
    fname = models.CharField(max_length=300)
    lname = models.CharField(max_length=300)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    province = models.CharField(max_length=100, choices=STATES)
    district = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    city = models.CharField(max_length=300)
    total = models.IntegerField(null=False)
    payment = models.CharField(max_length=100, choices=PAYMENT_METHOD)
    payment_id = models.CharField(max_length=150, null=True)
    status = models.CharField(max_length=150, choices=STATUS, default='Pending')
    message = models.TextField()
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)