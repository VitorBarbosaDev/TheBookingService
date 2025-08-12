from django.shortcuts import render
from accounts.models import Category


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    # Get some popular categories to show on 404 page
    popular_categories = Category.objects.filter(parent=None)[:6]  # Top-level categories

    context = {
        'popular_categories': popular_categories,
    }

    return render(request, "404.html", context, status=404)
