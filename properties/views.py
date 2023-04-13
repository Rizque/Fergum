from django.shortcuts import render, redirect
from .models import Property
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm


# Create your views here.
@login_required(login_url='login')
def addProperty(request):
    profile = request.user.profile
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = profile
            product.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'properties/property_form.html', context)


@login_required(login_url='login')
def updateProduct(request, pk):
    profile = request.user.profile
    product = profile.property_set.get(id=pk)
    form = PropertyForm(instance=product)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'properties/property_form.html', context)


@login_required(login_url='login')
def deleteProduct(request, pk):
    profile = request.user.profile
    product = profile.property_set.get(id=pk)
    product.delete()
    return redirect('profile')
