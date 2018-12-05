from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Store
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from datetime import datetime
import pytz
import geocoder, requests

def index(request):
    ''' This is home page view that contains all nearby shops '''
    if request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.id)
        # get all stores tha are blocked 
        blocked_stores = current_user.stores.filter(is_blocked=True)
        for bstore in blocked_stores:
            hours = abs(datetime.now(tz=pytz.utc) - bstore.date).total_seconds() / 3600.0
            # if any of the store are passed the 2h time being blocked unblock them
            if hours >= 2:
                bstore.is_blocked = False
                bstore.date = datetime.now(tz=pytz.utc)
        # then get all the store normally that are not blocked
        all_stores = current_user.stores.filter(is_blocked=False)
        paginator = Paginator(all_stores, 36)
        page = request.GET.get('page')
        stores = paginator.get_page(page)
        return render(request, 'stores/index.html', {'stores' : stores})
    else:
        return render(request, 'stores/login.html')

def login_v(request):
    ''' Log the user in if everything is fine '''
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
    ''' Log Out the current user '''
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def get_data(request):
    ''' Get longtitde and latitude from ser ip address and then get all nearby stores by sending an HTTP GET request to the url below'''
    latitude, longtitude =  tuple(map(str, geocoder.ip('me').latlng))
    r = requests.get('https://places.cit.api.here.com/places/v1/browse?at=35.7226%2C-5.9357&q=shopping&size=200&Accept-Language=en-US%2Cen%3Bq%3D0.9&app_id=3iwRXjOK1iYH4KPMUYdC&app_code=4u-MGNNl4aGp1t_0r-3_tg')
    rj = r.json()
    results = rj['results']['items']
    for result in results:
        s = Store.objects.create(name=result['title'], distance=result['distance'], category=result['category']['title'], vicinity=result['vicinity'], icon=result['icon'])
        s.users.add(User.objects.get(pk=request.user.id))
    
def add_preffer(request, store_id):
    ''' Add store to prefer list '''
    store = Store.objects.get(pk=store_id)
    store.is_preffered = True
    store.save()
    return HttpResponseRedirect(reverse('favorite'))

def favorites(request):
    ''' preferred list view to display all preferred shops '''
    current_user = User.objects.get(pk=request.user.id)
    pstores = current_user.stores.filter(is_preffered=True)
    paginator = Paginator(pstores, 10)
    page = request.GET.get('page')
    stores = paginator.get_page(page)
    return render(request, 'stores/prefferedPage.html', {'pstores' : stores})

def remove_from_favorites(request, store_id):
    ''' Remove store from favorite list '''
    store = Store.objects.get(pk=store_id)
    store.is_preffered = False
    store.save()
    return HttpResponseRedirect(reverse('favorite'))

def dislike_store(request, store_id):
    ''' Dislike a Store '''
    store = Store.objects.get(pk=store_id)
    store.is_blocked = True
    store.date = datetime.now(tz=pytz.utc)
    store.save()
    return HttpResponseRedirect(reverse('index'))
