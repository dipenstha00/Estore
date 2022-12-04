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