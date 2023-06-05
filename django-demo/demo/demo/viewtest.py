from django.shortcuts import render
 
def demo(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 't.html', context)