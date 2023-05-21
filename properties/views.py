from django.shortcuts import render, redirect
from .models import Property
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
# from django.shortcuts import get_object_or_404


# def main_page(request, pk):
#     if 'chosen_property' in request.session:
#         property_name = request.session['chosen_property']
#         property = get_object_or_404(Property, id=pk)
#     else:
#         property = Property.objects.first()

#     return render(request, 'main_page.html', {'property': property})


@login_required(login_url='login')
def addProperty(request):
    profile = request.user.profile
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = profile
            product.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'properties/property_form.html', context)


@login_required(login_url='login')
def updateProperty(request, pk):
    profile = request.user.profile
    property = profile.property_set.get(property_id=pk)
    form = PropertyForm(instance=property)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'properties/property_form.html', context)


@login_required(login_url='login')
def deletePropertry(request, pk):
    profile = request.user.profile
    product = profile.property_set.get(property_id=pk)
    product.delete()
    return redirect('profile')
