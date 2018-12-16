from django.shortcuts import render
from django.http import HttpResponse
from .models import Logs

# Create your views here.
def index(request):
    #return HttpResponse('Test')
    trades = Logs.objects.all()[:10]
    data = {
        'title': 'Logs',
        'trades': trades
    }
    return render(request, 'log/index.html', data)

def details(request, id):
    #TODO validate id
    trade = Logs.objects.get(id=id)
    data = {
        'trade': trade
    }
    return render(request, 'log/details.html', data)

def handler404(request, exception):
    return render(request, 'log/404.html', locals())