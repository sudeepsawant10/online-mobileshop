from django.shortcuts import render

# Create your views here.
def index(request, **kwargs):
    user = request.user
    context = {
        'id':kwargs['id'],
    }
    return render(request, 'adminapp/index.html',context)