from django.shortcuts import render, redirect, reverse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

def index(request):   
    return render(request, 'LogReg/index.html')

def create(request):
    regstatus = User.userManager.register(**request.POST)
    if regstatus[0]:
        messages.success(request, 'You have successfully registered!')
        request.session['user_id'] = regstatus[1]
        return redirect(reverse('examapp:index'))
    else:
        for message in regstatus[1]:
            messages.warning(request, message)
        return redirect(reverse('logreg:index'))

def login(request):
    loginstatus = User.userManager.login(request.POST['username'], request.POST['password'])
    if loginstatus[0]:
        request.session['user_id'] = loginstatus[1]
        return redirect(reverse('examapp:index'))
    else:
        messages.warning(request, loginstatus[1])
        return redirect(reverse('logreg:index'))

def logout(request):
    request.session.clear()
    redirect(reverse('logreg:index'))