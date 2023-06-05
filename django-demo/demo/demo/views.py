from django.http import HttpResponse
 
def hello(request):
    return HttpResponse("Hello world ! ")

def demo(requert):
    return HttpResponse("test")