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

        return render(request, 'index.html', self.context)