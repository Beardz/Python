from django.http import HttpResponse


# def hello(request):
#     return HttpResponse("hello")
 
from django.shortcuts import render
 
def runoob(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'runoob.html', context)