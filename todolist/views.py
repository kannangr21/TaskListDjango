from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User , auth
from django.contrib import messages
from enter.models import Tasks
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
import json
def onlogin(request):
    if request.method=="POST":
        name = request.POST['username']
        pw = request.POST['password']
        user = auth.authenticate(username=name,password=pw)
        if user is not None:
            auth.login(request,user)
            tasks = Tasks.objects.get(name=name)
            jsonDEC = json.decoder.JSONDecoder()
            heading = jsonDEC.decode(tasks.heading)
            description = jsonDEC.decode(tasks.description)
            tdate = jsonDEC.decode(tasks.deadline)
            num = list(x for x in range(len(heading)))
            task = zip(heading,description,tdate,num)
            return render(request,"todolist.html",{'flag':True,'name':name,'tasks':task})

            
        else:
            messages.error(request,"Authentication Failed! Please enter correct credentials")
            return render(request,'login.html')
    else:
        messages.error(request,"Please login to access this page!")
        return render(request,'login.html') 

def addtask(request):
    if request.method=="GET":
        messages.error(request,"Please login to access this page!")
        return render(request,'login.html')
    else:
        try:
            uname = request.POST['username']
            heading = request.POST['heading']
            description = request.POST['description']
            deadline = request.POST['date']
            task = Tasks.objects.get(name=uname)
            jsonDEC = json.decoder.JSONDecoder()
            temphead = jsonDEC.decode(task.heading)
            tempdesc = jsonDEC.decode(task.description)
            temptdate = jsonDEC.decode(task.deadline)
            temphead.append(heading)
            tempdesc.append(description)
            temptdate.append(deadline)
            task.heading = json.dumps(temphead)
            task.description = json.dumps(tempdesc)
            task.deadline = json.dumps(temptdate)
            task.save()
            return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/login/";</script>')

        except:        

            uname = request.POST['username']
            return render(request,'addtask.html',{'name':uname})
def deltask(request):
    if request.method == "GET":
        messages.error(request,"Please login to access this page!")
        return render(request,'login.html')
    else:
        uname = request.POST['username']
        tasks = Tasks.objects.get(name=uname)
        jsonDEC = json.decoder.JSONDecoder()
        heading = jsonDEC.decode(tasks.heading)
        description = jsonDEC.decode(tasks.description)
        tdate = jsonDEC.decode(tasks.deadline)
        num = list(x for x in range(len(heading))) 
        task = zip(heading,description,tdate,num)
        return render(request,'deletetasks.html',{'name':uname,'tasks':task})
def delete(request):        
    uname = request.POST['username']
    task = Tasks.objects.get(name=uname)
    jsonDEC = json.decoder.JSONDecoder()
    temphead = jsonDEC.decode(task.heading)
    tempdesc = jsonDEC.decode(task.description)
    temptdate = jsonDEC.decode(task.deadline)
    temp2head,temp2desc,temp2tdate = [],[],[]
    num = list(x for x in range(len(temphead)))
    for c in num:
        if request.POST.get(str(c),False):
            continue
        else:
            temp2head.append(temphead[c])
            temp2desc.append(tempdesc[c])
            temp2tdate.append(temptdate[c])
        task.heading = json.dumps(temp2head)
        task.description = json.dumps(temp2desc)
        task.deadline = json.dumps(temp2tdate)
        task.save()
    return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/login/";</script>')

def sendmsg(request):
    if(request.method == "GET"):
        return HttpResponse("Page not found!")
    name = request.POST['Name']
    user = User.objects.get(username=name)
    uemail = user.email
    fname = user.first_name
    signature = "\n\n\nThanks,\nKannan G R."
    subuser = "Feedback"
    msguser = "Hello " + fname + ",\n" + "Thanks for using this website. We have received your feedback.\n\nWe will try to reply within 24 hrs if there's any query." + signature
    rating = request.POST['Rating']
    msg = request.POST['Message']
    subadm = "User review"
    msgadm = "\nName : " + name + "\nRating : " + rating + "\nMessage : " + msg
    from_email = settings.EMAIL_HOST_USER
    datatuple = (
        (subuser,msguser,from_email,[uemail]),
        (subadm,msgadm,from_email,['technicalstuff215@gmail.com']),
    )
    send_mass_mail(datatuple)
    tasks = Tasks.objects.get(name=name)
    jsonDEC = json.decoder.JSONDecoder()
    heading = jsonDEC.decode(tasks.heading)
    description = jsonDEC.decode(tasks.description)
    tdate = jsonDEC.decode(tasks.deadline)
    num = list(x for x in range(len(heading)))
    task = zip(heading,description,tdate,num)
    return render(request,'todolist.html',{'name':name,'tasks':task,'msg':"Thanks for your feedback"})