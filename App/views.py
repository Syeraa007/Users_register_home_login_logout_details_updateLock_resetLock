from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from App.forms import *
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def register(request):
    d={'UFO':Users(),'PFO':Profiles()}
    if request.method=='POST' and request.FILES:
        UFD=Users(request.POST)
        PFD=Profiles(request.POST,request.FILES)
        if UFD.is_valid() and PFD.is_valid():
            UUFO=UFD.save(commit=False)
            pswd=UFD.cleaned_data['password']
            UUFO.set_password(pswd)
            UUFO.save()
            UPFO=PFD.save(commit=False)
            UPFO.username=UUFO
            UPFO.save()
            send_mail('Registration','Registration is Succefully done in Django Project Application','jacksparrow.7828.007@gmail.com',[UUFO.email],fail_silently=True)
            return HttpResponse('<center><h1><b>Regsitration is successfully done</b></h1></center>')
        else:
            return HttpResponse('<center><h1><b>Invalid Details Encountered</b></h1></center>')
    return render(request,'register.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def signin(request):
    if request.method=='POST':
        username = request.POST["user"]
        password = request.POST["pass"]
        AO=authenticate(username=username,password=password)
        if AO:
            if AO.is_active:
                login(request,AO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('No User is Active')
        else:
            return HttpResponse('<center><h1><b> Invalid Details Encountered </b></h1></center>')
    return render(request,'signin.html')

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display(request):
        username=request.session['username']
        UO=User.objects.get(username=username)
        PO=Profile.objects.get(username=UO)
        d={'UO':UO,'PO':PO}
        return render(request,'display.html',d)

@login_required
def change(request):
    if request.method=='POST':
        pswd=request.POST['password']
        username=request.session['username']
        UO=User.objects.get(username=username)
        UO.set_password(pswd)
        UO.save()
        return HttpResponse('<center><h1><b> Password Changed Successfully </b></h1></center>')
    return render(request,'change.html')

def reset(request):
    if request.method=='POST':
        un=request.POST['username']
        pw=request.POST['password']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save
            return HttpResponse('<center><h1><b>Password Reset done successfully </b></h1></center>')
        else:
            return HttpResponse('<center><h1><b> Please Enter a valid username </b></h1></center>')
    return render(request,'reset.html')