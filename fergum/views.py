from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def frontpage(request):
    return render(request, 'frontpage.html')
