from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserCreationForm, ProfileForm
from django.contrib.auth.models import User, Group
from .models import Profile
from properties.models import Property
from .decorators import unauthenticated_user, allowed_users, worker_only


@unauthenticated_user
def loginUser(request):
    page = 'login'
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


@unauthenticated_user
def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')

            # Save the user without committing to the database
            user.username = user.username.lower()
            user.save()

            # Render a form for the user to select their group
            return render(request, 'users/select_group.html', {'user_id': user.id})

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def selectGroup(request):
    if request.method == 'POST':
        group_name = request.POST.get('group')
        user_id = request.POST.get('user_id')

        group = Group.objects.get(name=group_name)
        user = User.objects.get(id=user_id)
        user.groups.add(group)
        user.save()
        profile = Profile.objects.get(user=user)
        profile.chosen_group = group_name
        profile.save()

        messages.success(request, 'Group has been set successfully!')

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')

    return render(request, 'users/select_group.html')


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


@login_required
def add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        group = Group.objects.get(name=group_name)
        request.user.groups.add(group)
        # Redirect the user to a desired page after adding the group
        return redirect('home')


@login_required
def mainService(request):
    return render(request, 'users/main_service.html')


@login_required(login_url='login')
def home(request):
    user_profile = request.user.profile
    user_groups = request.user.groups.values_list('name', flat=True)
    if 'worker' in user_groups and 'owner' in user_groups:
        # Check if the chosen group is already stored in the session
        chosen_group = user_profile.chosen_group
        print(chosen_group)
        if chosen_group == 'worker' and 'worker' in user_groups:
            return redirect('main-service')
        elif chosen_group == 'owner' and 'owner' in user_groups:
            properties = Property.objects.filter(owner=user_profile)
            pk = request.GET.get('pk')

            if pk:
                chosen_property = get_object_or_404(
                    Property, pk=pk, owner=user_profile)
                # convert pk to string and store in session
                request.session['chosen_property'] = str(pk)
                return redirect('main-property', pk=pk)
            elif 'chosen_property' in request.session:
                chosen_property_pk = request.session['chosen_property']
                chosen_property = get_object_or_404(
                    Property, pk=chosen_property_pk, owner=user_profile)
                return redirect('main-property', pk=chosen_property_pk)
            elif properties:
                return redirect('main-property', pk=properties[0].pk)
            else:
                return render(request, 'users/no_properties.html')
        #         properties = Property.objects.filter(owner=user_profile)
        #         pk = request.session.get('chosen_property', None)
        #         if pk:
        #             chosen_property = get_object_or_404(
        #                 Property, pk=pk, owner=user_profile)
        #             return redirect('main-property', pk=pk)
        #         elif properties:
        #             return redirect('main-property', pk=properties[0].pk)
        #         else:
        #             return render(request, 'users/no_properties.html')
        # else:
        #     # If no group is chosen, set the default group to "worker"
        #     if 'worker' in user_groups:
        #         request.session['chosen_group'] = 'worker'
        #         return redirect('main-service')
    elif 'worker' in user_groups:
        return redirect('main-service')
    elif 'owner' in user_groups:
        properties = Property.objects.filter(owner=user_profile)
        pk = request.GET.get('pk')

        if pk:
            chosen_property = get_object_or_404(
                Property, pk=pk, owner=user_profile)
            # convert pk to string and store in session
            request.session['chosen_property'] = str(pk)
            return redirect('main-property', pk=pk)
        elif 'chosen_property' in request.session:
            chosen_property_pk = request.session['chosen_property']
            chosen_property = get_object_or_404(
                Property, pk=chosen_property_pk, owner=user_profile)
            return redirect('main-property', pk=chosen_property_pk)
        elif properties:
            return redirect('main-property', pk=properties[0].pk)
        else:
            return render(request, 'users/no_properties.html')
    else:
        user = request.user
        return render(request, 'users/select_group.html', {'user_id': user.id})


@login_required
def mainProperty(request, pk=None):

    user_profile = request.user.profile
    properties = Property.objects.filter(owner=user_profile)

    if pk:
        chosen_property = get_object_or_404(
            Property, pk=pk, owner=user_profile)
        # convert pk to string and store in session
        request.session['chosen_property'] = str(pk)
    elif 'chosen_property' in request.session:
        chosen_property_pk = request.session['chosen_property']
        chosen_property = get_object_or_404(
            Property, pk=chosen_property_pk, owner=user_profile)
    elif properties:
        chosen_property = properties[0]
    else:
        return render(request, 'no_properties.html')

    return render(request, 'users/main_property.html', {
        'chosen_property': chosen_property,
        'properties': properties,

    })


def switch_group(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        if profile.chosen_group == 'worker':
            profile.chosen_group = 'owner'
        else:
            profile.chosen_group = 'worker'
        profile.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    all_groups = Group.objects.all()

    context = {'profile': profile, 'all_groups': all_groups}
    return render(request, 'users/profile.html', context)


def history(request):
    profile = request.user.profile
    context = {'profile': profile, }
    return render(request, 'users/history.html', context)


def adress(request):
    return render(request, 'users/adress_locator.html')
