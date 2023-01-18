from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from security_db.models import Security

# Create your views here.

def home(request):
    return render(request, 'home.html')

def browse(request):
    #all_securities = Security.objects.order_by(ticker).all()
    all_securities = Security.objects.all()
    paginator = Paginator(all_securities, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'browse.html', {'page_obj': page_obj})
    #return render(request, 'browse.html')
