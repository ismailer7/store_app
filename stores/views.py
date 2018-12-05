from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Store
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
import geocoder, requests

def index(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.id)
        all_stores = current_user.stores.all()
        paginator = Paginator(all_stores, 36)
        page = request.GET.get('page')
        stores = paginator.get_page(page)
        return render(request, 'stores/index.html', {'stores' : stores})
    else:
        return render(request, 'stores/login.html')

def login_v(request):
    if request.method == 'POST':
        username = request.POST.get('username', False) # was a problem
        password = request.POST.get('password', False)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'stores/login.html', {'message' : 'Invalid Username/Password'})
    else:
        return render(request, 'stores/login.html')

def register(request):
    ''' we will get all stores here after he signed up '''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get all stores to add them to data base.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            get_data(request)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'stores/register.html', {'form' : form})
    else:
        form = UserCreationForm()
        return render(request, 'stores/register.html', {'form' : form})

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def get_data(request):
    latitude, longtitude =  tuple(map(str, geocoder.ip('me').latlng))
    r = requests.get('https://places.cit.api.here.com/places/v1/browse?at=35.7226%2C-5.9357&q=shopping&size=200&Accept-Language=en-US%2Cen%3Bq%3D0.9&app_id=3iwRXjOK1iYH4KPMUYdC&app_code=4u-MGNNl4aGp1t_0r-3_tg')
    rj = r.json()
    results = rj['results']['items']
    for result in results:
        s = Store.objects.create(name=result['title'], distance=result['distance'])
        s.users.add(User.objects.get(pk=request.user.id))
    
def add_preffer(request, store_id):
    store = Store.objects.get(pk=store_id)
    store.is_preffered = True
    store.save()
    return HttpResponseRedirect(reverse('index'))

def favorites(request):
    current_user = User.objects.get(pk=request.user.id)
    pstores = current_user.stores.filter(is_preffered=True)
    paginator = Paginator(pstores, 10)
    page = request.GET.get('page')
    stores = paginator.get_page(page)
    return render(request, 'stores/prefferedPage.html', {'pstores' : stores})

def remove_from_favorites(request, store_id):
    store = Store.objects.get(pk=store_id)
    store.is_preffered = False
    store.save()
    return HttpResponseRedirect(reverse('favorite'))