from django.shortcuts import render


def index(request):
    user = request.user
    return render(request, 'base.html', context = {'test':'LALALLALALAA', 'user':user})