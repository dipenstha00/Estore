from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Sider)
admin.site.register(Ads)
admin.site.register(Reviews)
admin.site.register(ProductReviews)
admin.site.register(Cart)
admin.site.register(Wishlist)