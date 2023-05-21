from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WorkerServiceForm

# Create your views here.


def services(request):
    return render(request, 'services/services.html')


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
