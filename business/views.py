from django.shortcuts import render
from .models import Business

def business_detail(request):
    business = Business.objects.first()
    context = {'business': business}
    return render(request, 'business/business_detail.html', context)
