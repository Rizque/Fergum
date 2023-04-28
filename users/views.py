from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserCreationForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile
from properties.models import Property


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('add-property')
        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('profile')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


# def property_list(request):
#     user_profile = request.user.profile
#     properties = user_profile.property_set.all()
#     return render(request, 'users/property_list.html', {'properties': properties})

@login_required
def home(request):
    user_profile = request.user.profile
    properties = Property.objects.filter(owner=user_profile)
    pk = request.GET.get('pk')

    if pk:
        chosen_property = get_object_or_404(
            Property, pk=pk, owner=user_profile)
        return redirect('main-property', pk=pk)
    elif properties:
        return redirect('main-property', pk=properties[0].pk)
    else:
        return render(request, 'no_properties.html')


@login_required
def mainProperty(request, pk=None):
    user_profile = request.user.profile
    properties = Property.objects.filter(owner=user_profile)

    if pk:
        chosen_property = get_object_or_404(
            Property, pk=pk, owner=user_profile)
    elif properties:
        chosen_property = properties[0]
    else:
        return render(request, 'no_properties.html')

    return render(request, 'users/main_property.html', {
        'chosen_property': chosen_property,
        'properties': properties,
    })

# @login_required(login_url='login')


def profile(request):
    profile = request.user.profile
    context = {'profile': profile, }
    return render(request, 'users/profile.html', context)


def adress(request):
    return render(request, 'users/adress_locator.html')
