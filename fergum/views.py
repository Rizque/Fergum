from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test


def frontpage(request):
    if request.user.is_authenticated:
        return redirect('home')  # Or whatever URL you want to redirect to
    else:
        return render(request, 'frontpage.html')
