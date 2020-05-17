from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os
# import zipfile
# Create your views here.

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    keyword = search_for = msg = ''
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
            msg = 'sucdlt'
    context = { 
        'msg':msg,
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

@login_required(login_url='/login/')
def memberPdfView(request,id):
    member = models.MemberRegistration.objects.get(id=id)
    try:
        back = root + '/media/bg.jpg'
        # princi = root + '/media/'+ str(details.principalSign)
        # logoright = root + '/media/'+ str(details.parentLogo)
        logoleft = root + '/media/jpac.png'
        width = 540*mm
        height = 860*mm
        c = canvas.Canvas("pdf/"+ str(member.member_id)+'_'+member.first_name+'_'+member.last_name +'.pdf')
        if member.photo != None:
            pic = root + member.photo.url
        c.setPageSize((width, height))
        # if details.backgroundDesign:
        c.drawImage(back, 0, 0, height=height, width=width)
        #c.saveState()
        # if details.collegeLogo:
        c.drawImage(logoleft, 30*mm, 740*mm, height=80*mm, width=80*mm)
        # if details.parentLogo:
            # c.drawImage(logoright, 450*mm, 740*mm, height=80*mm, width=80*mm)
        # c.setFont(str(details.collegeNameFont), int(details.collegeNameFontSize))
        # c.drawCentredString(width/2, height-(60*mm),str(details.collegeName))
        # c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
        # c.drawCentredString(width/2, height-(80*mm),str(details.addressLine1))
        # c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
        # c.drawCentredString(width/2, height-(100*mm), str(details.addressLine2))
        #c.drawCentredString(width/2, height-(120*mm), "")  Kerala, India, PIN: 682 021 
        # c.drawCentredString(width/2, height-(120*mm),str(details.addressLine3))
        # c.drawCentredString(width/2, height-(140*mm),str(details.addressLine4))
        # c.setFont(str(details.addressLine1To5Font), int(details.addressLine1To5FontSize))
        # c.drawCentredString(width/2, height-(160*mm), str(details.addressLine5))
        if member.photo != None:
            c.drawImage(pic, 170*mm, height-(375*mm), height=225*mm, width=175*mm)
        c.setFont('Times-Bold', 63)
        c.drawString(40*mm, 420*mm, "Member Id  ")
        c.drawString(175*mm, 420*mm,": " + str(member.member_id))
        c.setFont('Times-BoldItalic', 60)
        c.drawString(40*mm, 360*mm, "Fist Name  ")
        c.drawString(175*mm, 360*mm,": " + member.first_name)
        c.drawString(40*mm, 300*mm, "Last Name  ")
        c.drawString(175*mm, 300*mm,": " + member.last_name)
        c.drawString(40*mm, 240*mm, "Mobile No  ")
        c.drawString(175*mm, 240*mm, ": " + member.mobile)
        c.drawString(40*mm, 180*mm, "Unit  ")
        c.drawString(175*mm, 180*mm, ": " + member.unit)
        c.drawString(40*mm, 120*mm, "Sector  ")
        c.drawString(175*mm, 120*mm, ": " + member.sector)
        c.drawString(40*mm, 60*mm, "Central  ")
        c.drawString(175*mm, 60*mm, ": " + member.central)
        # c.drawString(30*mm, 120*mm, "Valid Till :")
        # c.drawString(165*mm, 120*mm,str(i.validtill.day)+'/'+str(i.validtill.month)+'/'+str(i.validtill.year))
        # c.drawString(30*mm, 60*mm, "Date Of Birth:")
        # c.drawString(165*mm, 60*mm,str(i.dateofbirth.day)+'/'+str(i.dateofbirth.month)+'/'+str(i.dateofbirth.year))
        # c.setFont('Times-Bold', 60)
        # c.drawString(420*mm, 20*mm, "Principal")
        # if details.principalSign:
            # c.drawImage(princi, 420*mm, 45*mm, height= 50*mm, width=80*mm)
        c.showPage()
        c.save()
        # arch=zipfile.ZipFile("pdf/"+"id.zip","w")
        # arch.write("pdf/"+ str(member.member_id)+'_'+member.first_name+'_'+member.last_name +'.pdf')
        # arch.close()
        response = HttpResponse(open(root+"/pdf/"+ str(member.member_id)+'_'+member.first_name+'_'+member.last_name +'.pdf', 'rb').read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+str(member.member_id)+'_'+member.first_name+'_'+member.last_name +'.pdf'
        return response
    except:
        return redirect('registered')
    

def logoutView(request):
    logout(request)
    return redirect('login')