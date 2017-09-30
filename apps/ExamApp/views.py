from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q  
from .models import User, Trip, Guest

def index(request):  
    if 'user_id' in request.session:
        current_user = User.objects.get(id=request.session['user_id'])
        usertrip_query = Trip.objects.filter(Q(user=current_user) | Q(guesttrip__user=current_user)).order_by('date_start')
        trip_query = Trip.objects.exclude(user=current_user).exclude(guesttrip__user=current_user).order_by('date_start')
        context = {
            'user': current_user,
            'usertrips': usertrip_query, 
            'trips': trip_query
            }
        return render(request, 'ExamApp/index.html', context)
    else:
        return redirect(reverse('loginreg:index'))

def add(request):  
    return render(request, 'ExamApp/add_trip.html')

def create(request):  
    current_user = User.objects.get(id=request.session['user_id'])
    tripstatus = Trip.tripManager.addtrip(user=current_user, **request.POST)
    if tripstatus[0]:
        messages.success(request, 'Trip successfully added!')
        return redirect(reverse('examapp:index'))
    else:
        for message in tripstatus[1]:
            messages.warning(request, message)
        return redirect(reverse('examapp:add_trip'))

def view(request, trip_id):  
    trip_query = Trip.objects.get(id=trip_id)
    guest_query = Guest.objects.filter(trip__id=trip_id).exclude(user__id=request.session['user_id'])
    
    context = {
        'trip': trip_query,
        'guests': guest_query
        }
    return render(request, 'ExamApp/view_trip.html', context)

def join(request, trip_id):  
    joinstatus = Trip.tripManager.jointrip(request.session['user_id'], trip_id)
    if joinstatus[0]:
        messages.success(request, joinstatus[1])
        return redirect(reverse('examapp:index'))
    else:
        messages.warning(request, joinstatus[1])
        return redirect(reverse('examapp:index'))