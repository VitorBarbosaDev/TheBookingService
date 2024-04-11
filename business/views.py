from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Business
from .forms import BusinessForm

@login_required
def business_detail(request):
    try:
        business = Business.objects.get(owner=request.user)
    except Business.DoesNotExist:
        messages.error(request, "Business profile not found.")
        return redirect('home')
    context = {'business': business}
    return render(request, 'business/business_detail.html', context)


@login_required
def edit_business(request, pk):
    business = get_object_or_404(Business, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your business profile has been updated.')
            return redirect('business_detail')
    else:
        form = BusinessForm(instance=business)
    return render(request, 'business/edit_business.html', {'form': form, 'business': business})




@login_required
def delete_business(request, pk):
    business = get_object_or_404(Business, pk=pk, owner=request.user)
    if request.method == 'POST':
        business.delete()
        messages.success(request, 'Your business profile has been deleted.')
        return redirect('some_safe_url')  # Redirect to a safe URL
    return render(request, 'business/delete_business.html', {'business': business})
