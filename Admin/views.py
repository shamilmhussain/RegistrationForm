from django.shortcuts import render,redirect
from . import models
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def memberRegistrationView(request):
    msg = ''
    try:
        if request.method == 'POST':
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken')
            dd = {}
            for key,value in data.items():
                dd[key] = value
            dd['photo'] = request.FILES['photo']
            try:
                obj = models.MemberRegistration.objects.last()
                dd['member_id'] = obj.member_id + 1
            except:
                dd['member_id'] = 101
            models.MemberRegistration.objects.create(**dd)
            msg = 'success'
    except Exception as e:
        first_name =  request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        mobile =  request.POST.get('mobile')
        models.RegisterErrorLog.objects.create(
            error = str(e),first_name=first_name,last_name=last_name,mobile=mobile)
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
    keyword = search_for = ''
    members = models.MemberRegistration.objects.all()
    if request.method == 'POST':
        if 'search' in request.POST:
            keyword = request.POST.get('keyword')
            search_for = request.POST.get('search_for')
            if search_for == 'job':
                members = members.filter(job__icontains=keyword)
            elif search_for == 'job_type':
                members = members.filter(job_type__icontains=keyword)
            elif search_for == 'company':
                members = members.filter(company__icontains=keyword)
            elif search_for == 'education':
                members = members.filter(education__icontains=keyword)
            elif search_for == 'blood_group':
                members = members.filter(blood_group__icontains=keyword)
        elif 'delete_id' in request.POST:
            models.MemberRegistration.objects.get(id=request.POST.get('delete_id')).delete()
    context = { 
        'keyword':keyword,
        'search_for':search_for,
        'members' : members
        }
    return render(request,'data-tables.html',context = context)

@login_required(login_url='/login/')
def editMemberView(request,id):
    msg = ''
    member = models.MemberRegistration.objects.get(id=id)
    try:
        if request.method == 'POST':
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken')
            dd = {}
            for key,value in data.items():
                dd[key] = value
            if 'photo' in dd:
                if dd['photo'] == '':
                    dd.pop('photo')
            models.MemberRegistration.objects.filter(id=id).update(**dd)
            if 'photo' in request.FILES:
                if request.FILES['photo'] != '':
                    member.photo.delete()
                    member.photo = request.FILES['photo']
                    member.save()
            return redirect('registered')
    except Exception as e:
        first_name =  request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        mobile =  request.POST.get('mobile')
        models.RegisterErrorLog.objects.create(
            error = 'EDIT ERROR' + str(e),first_name=first_name,last_name=last_name,mobile=mobile)
    context = { 'member' : member}
    return render(request,'registration_edit.html',context = context)

@login_required(login_url='/login/')
def memberView(request,id):
    member = models.MemberRegistration.objects.get(id=id)
    context = { 
        'member' : member
        }
    return render(request,'registration_view.html',context = context)

def logoutView(request):
    logout(request)
    return redirect('login')