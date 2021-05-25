from django.shortcuts import render,redirect
from django.http import HttpResponse, QueryDict
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User , auth
from enter import models
from enter.models import Tasks,temp
from django.db import IntegrityError
from django.contrib.auth import authenticate
import random as r
import json


def login(request):
    return render(request,'login.html')

def reset(request):
    if(request.method=="POST"):
        uname = request.POST["username"]
        uemail = str(request.POST["email"]).capitalize()
        try:
            user = User.objects.get(username=uname,email=uemail)
        except:    
            return HttpResponse("<h2>Unknown Error! Please try again with correct username and email</h2>")
        if user is not None:
            u = User.objects.get(username=uname)
            t = temp.objects.get(name=uname) 
            fname = u.first_name
            the_otp = r.randint(100000,999999)
            t.otp = the_otp
            t.save()
            sub = "OTP for password change"
            signature = "\n\n\nThanks,\nKannan G R."
            msg = "Hello "+fname+",\n"+"The OTP for resetting the password is "+str(the_otp)+"."+signature
            from_email = settings.EMAIL_HOST_USER
            to_email = [request.POST['email'],]
            send_mail(sub,msg,from_email,to_email)
             
        else:
            return HttpResponse("<h2>Unknown Error! Please try again with correct username and email</h2>")
        return render(request,'reset.html',{'otpflag':True,'username':uname,'email':uemail,'msg':" Please Enter the OTP sent to your email."})
    else:
        return render(request,'reset.html')

def verify(request):
    uname = request.POST['username']
    uemail = request.POST['email']
    t = temp.objects.get(name=uname)
    if(t.otp == int(request.POST['otp'])):
        return render(request,'reset.html',{'otpflag':True,'verified':True,'username':uname,'email':uemail,'msg':" Please Enter the new password."})
    else:
        return HttpResponse("<html><body<h2>OTP mismatch</h2></body></html>") 
def passverify(request):
    uname = request.POST['username']
    uemail = request.POST['email']
    if(request.POST['pass1']==request.POST['pass2']):
        pw = request.POST['pass1']
        t = temp.objects.get(name=uname)
        u = User.objects.get(username=uname)
        t.otp = 0
        u.set_password(pw)
        u.save()
        t.save()    
    else:
        return render(request,'reset.html',{'otpflag':True,'verified':True,'username':uname,'email':uemail,'msg':"Password mismatch"})
    return render(request,'login.html')



def regsub(request):
    if(request.method=="POST"):
        uname = request.POST['username']
        fname = request.POST['fname']
        if (request.POST['lname'] != None):
            lname = request.POST['lname']
        else:
            lname = '-'
        email = str(request.POST['email']).capitalize()
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if(pass1==pass2):
            dictpass = {
                'username':uname,
                'fname':fname,
                'lname':lname,
                'email':email,
                'password':pass1,
            }
            the_otp = r.randint(100000,999999)
            try:
                t=temp.objects.create(name=uname,otp=the_otp)
                sub = "OTP for registration"
                signature = "\n\n\nThanks,\nKannan G R."
                msg = "Hello "+str(request.POST['fname'])+",\n"+"The OTP for registration is "+str(the_otp)+"."+signature
                from_email = settings.EMAIL_HOST_USER
                to_email = [request.POST['email'],]
                send_mail(sub,msg,from_email,to_email)
                t.save()
            except(IntegrityError):
                return render(request,'register.html',{'flag':True,'msg':"Username already exits! Please try again."})
            messages.info(request,"Password Verified! Please Enter the OTP sent to your email.")
            return render(request,'register.html',dictpass)

        elif(request.POST['pass1']!=request.POST['pass2']):
            messages.info(request,"Password Mismatch!")
            return render(request,'register.html',{'flag':True})
        else:
            return HttpResponse("<html><body<h2>Unknown Error. Please try again.</h2></body></html>")
    else:
        return render(request,'register.html',{'flag':True})

        
def reverify(request):
    uname = request.POST['username']
    fname = request.POST['fname']
    if (request.POST['lname'] != None):
        lname = request.POST['lname']
    else:
        lname = '-'
    email = str(request.POST['email']).capitalize()
    pass1 = request.POST['pass1'] 
    t = temp.objects.get(name=uname)
    if (t.otp == int(request.POST['otp'])):
        user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=email, password=pass1)
        task = Tasks()
        head=["Use this website"]
        desc=["This is a default task. You may delete this later."]
        tdate = ["--"]
        task.name = uname
        task.heading = json.dumps(head)
        task.description = json.dumps(desc)
        task.deadline = json.dumps(tdate)
        t.otp = 0
        t.save()
        user.save()
        task.save()
        sub = "Account creation successful"
        signature = "\n\n\nThanks,\nKannan G R."
        msg = "Hello "+str(request.POST['fname'])+",\n"+"Thanks for using this website.\nYour account has been created successfully, you can use the registered username and password to access the website.\nKindly share your views/feedback about this project in the website's contact part.\n\n Username : "+uname+signature
        from_email = settings.EMAIL_HOST_USER
        to_email = [request.POST['email'],]
        send_mail(sub,msg,from_email,to_email)
        messages.info(request,"Account has been created Successfully!")
        return render(request,'login.html')
    
    elif(t.otp != int(request.POST['otp'])):
        return HttpResponse("<html><body<h2>OTP mismatch</h2></body?</html>") 

    else:
        return HttpResponse("<html><body<h2>Unknown Error</h2></body?</html>")

    

def logout(request):
    auth.logout(request)
    return redirect('/')
