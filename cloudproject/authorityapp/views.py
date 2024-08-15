
from turtle import down
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from userapp.models import *
from mainapp.models import *
from ownerapp.models import *
from cloudapp.models import *
from authorityapp.models import *
from enclaveapp.models import *
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404

import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd

# Create your views here.



def authority_login(request):
    if request.method=='POST':
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        if name=='authority' and pwd=='authority':
            messages.info(request,"login successfull")
            return redirect('authority_dashboard')
        else:
            messages.warning(request,'Something Wrong, Please try again.')
            return redirect ('authority_login')
    return render(request,'main/authority-login.html')



def authority_dashboard(request):
    owners=ownerModel.objects.count()
    users=userModel.objects.count()
    uploads=fileModel.objects.count()
    requests=requestModel.objects.count()
    attacks=userModel.objects.filter(status='Blocked').count()
    a_users=userModel.objects.filter(status='Accepted').count()
    a_file=fileModel.objects.filter(status='Accepted').count()
    return render(request,'authority/authority-dashboard.html',{'owners':owners, 'users':users, 'uploads':uploads,'requests':requests,'attacks':attacks,'a_users':a_users,'a_file':a_file})    





def authority_view_users(request):
    data=userModel.objects.all().order_by("reg_date")

    if request.method=='POST':
         search=request.POST.get('search')
         data=userModel.objects.filter(Q(user_id__icontains=search) | Q(user_name__icontains=search))
    return render(request,'authority/authority-view-users.html',{'data':data})    




def authority_cloud_request(request):
 return render(request,'authority/authority-cloud-request.html')    




def accept_user(request,id):
    accept=get_object_or_404(userModel,user_id=id)
    accept.status='Accepted'
    accept.save(update_fields=['status'])
    accept.save()
    return redirect('authority_view_users')

def reject_user(request,id):
    reject=get_object_or_404(userModel,user_id=id)
    reject.status='Rejected'
    reject.save(update_fields=['status'])
    reject.save()
    return redirect('authority_view_users') 

