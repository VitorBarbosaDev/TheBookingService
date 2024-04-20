from django.shortcuts import render

def about(request):
    return render(request, 'information/about.html')

def contact(request):
    return render(request, 'information/contact.html')

def privacy_policy(request):
    return render(request, 'information/privacy_policy.html')