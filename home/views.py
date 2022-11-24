from django.shortcuts import render
from django.views.generic import View
from .models import *


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
