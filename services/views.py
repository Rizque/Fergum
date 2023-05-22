from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WorkerServiceForm
from .models import ServiceCategory, ServiceSubCategory, Service
# Create your views here.


def categories(request):
    categories = ServiceCategory.objects.all()
    return render(request, 'services/categories.html', {'categories': categories})


def subcategories(request, category_id):
    category = get_object_or_404(ServiceCategory, category_id=category_id)
    subcategories = ServiceSubCategory.objects.filter(category=category)
    return render(request, 'services/subcategories.html', {'subcategories': subcategories})


def service(request, service_id):
    service = get_object_or_404(Service, service_id=service_id)
    return render(request, 'services/service.html', {'service': service})


def category_services(request, category_id):
    category = ServiceCategory.objects.get(category_id=category_id)
    services = Service.objects.filter(category=category)
    return render(request, 'services/category_services.html', {'category': category, 'services': services})


@login_required(login_url='login')
def addWorkerService(request):
    profile = request.user.profile
    form = WorkerServiceForm  # ()  # Create an instance of the form

    if request.method == 'POST':
        form = WorkerServiceForm(request.POST)
        if form.is_valid():
            workerservice = form.save(commit=False)
            workerservice.worker = profile  # Assign the logged-in user's profile as the worker
            workerservice.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'services/workerservice_form.html', context)


@login_required(login_url='login')
def deleteWorkerService(request, pk):
    profile = request.user.profile
    workerservice = profile.workerservice_set.get(id=pk)
    workerservice.delete()
    return redirect('profile')
