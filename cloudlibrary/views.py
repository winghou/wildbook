# coding: utf-8
from django.shortcuts import render


def debug(request):
    return render(request, 'cloudlibrary/people.html')
    pass
