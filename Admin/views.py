from django.shortcuts import render,redirect
from . import models
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def memberRegistrationView(request):
    msg = ''
    if request.method == 'POST':
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken')
        dd = {}
        for key,value in data.items():
            dd[key] = value
        models.MemberRegistration.objects.create(**dd)
        msg = 'success'
    context = { 'msg' : msg}
    return render(request,'registration_form.html',context = context)

def adminLoginView(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('registered')
        else:
            msg = 'auth_error'
    context = {
        'msg':msg,
    }
    return render(request,'login.html',context)

@login_required(login_url='/login/')
def RegisteredView(request):
    members = models.MemberRegistration.objects.all()
    context = { 'members' : members}
    return render(request,'data-tables.html',context = context)

@login_required(login_url='/login/')
def memberView(request,id):
    member = models.MemberRegistration.objects.get(id=id)
    context = { 'member' : member}
    return render(request,'registration_view.html',context = context)

def logoutView(request):
    logout(request)
    return redirect('login')