
from turtle import down
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from userapp.models import *
from mainapp.models import *
from ownerapp.models import *
from cloudapp.models import *
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
import requests
import random
import numpy as np
import matplotlib.pyplot as plt

from django.core.mail import EmailMultiAlternatives
from cloudproject.settings import DEFAULT_FROM_EMAIL
from mainapp.check_internet import *
# from Power.settings import DEFAULT_FROM_EMAIL
# import pandas as pd

# Create your views here.



def cloud_login(request):
    if request.method=='POST':
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        if name=='likhita' and pwd=='likhita':
            messages.info(request,"login successfull")
            return redirect('cloud_dashboard')
        else:
            messages.warning(request,'Something Wrong, Please try again.')
            return redirect ('cloud_login')
    return render(request,'main/cloud-login.html')



def cloud_dashboard(request):
    owners=ownerModel.objects.count()
    users=userModel.objects.count()
    uploads=fileModel.objects.count()
    requests=requestModel.objects.count()
    attacks=userModel.objects.filter(status='Blocked').count()
    a_users=userModel.objects.filter(status='Accepted').count()
    a_file=fileModel.objects.filter(status='Accepted').count()
    return render(request,'cloud/cloud-dashboard.html',{'owners':owners,'users':users,'requests':requests,'uploads':uploads,'attacks':attacks,'a_users':a_users,'a_file':a_file})    





def cloud_view_owners(request):
    data=ownerModel.objects.all().order_by("reg_date")

    if request.method=='POST':
         search=request.POST.get('search')
         data=ownerModel.objects.filter(Q(owner_id__icontains=search) | Q(owner_name__icontains=search))
    return render(request,'cloud/cloud-view-owners.html',{'data':data})    

def accept_owner(request,id):
    accept=get_object_or_404(ownerModel,owner_id=id)
    accept.status='Accepted'
    accept.save(update_fields=['status'])
    accept.save()
    return redirect('cloud_view_owners')

def reject_owner(request,id):
    reject=get_object_or_404(ownerModel,owner_id=id)
    reject.status='Rejected'
    reject.save(update_fields=['status'])
    reject.save()
    return redirect('cloud_view_owners') 


def cloud_download_request(request):
    data=requestModel.objects.all().order_by("requested_date")

    if request.method=='POST':
         search=request.POST.get('search')
         data=requestModel.objects.filter(Q(request_id__icontains=search) | Q(file_name__icontains=search))
    return render(request,'cloud/cloud-download-request.html',{'data':data})    


def accept_forword(request,id):
    accept=get_object_or_404(requestModel,request_id=id)
    accept.status='Forwarded'
    accept.save(update_fields=['status'])
    accept.save()
    return redirect('cloud_download_request')

def reject_forword(request,id):
    reject=get_object_or_404(requestModel,request_id=id)
    reject.status='Pending'
    reject.save(update_fields=['status'])
    reject.save()
    return redirect('cloud_download_request') 

def cancel_forword(request,id):
    reject=get_object_or_404(requestModel,request_id=id)
    reject.status='Pending'
    reject.save(update_fields=['status'])
    reject.save()
    return redirect('cloud_download_request')     



def cloud_view_files(request):
    data=fileModel.objects.all().order_by("file_uploaded_date")
    if request.method=="POST" :
     search=request.POST.get('search')
     data=fileModel.objects.filter(Q(file_id__icontains=search) | Q(file_name__icontains=search)  | Q(file__icontains=search) | Q(file_type__icontains=search) | Q(file_size__icontains=search) | Q(file_uploaded_date__icontains=search))
    return render(request,'cloud/cloud-view-files.html',{'data':data})



def accept_file(request,id):
    accept=get_object_or_404(fileModel,file_id=id)
    accept.status='Accepted'
    accept.save(update_fields=['status'])
    accept.save()
    return redirect('cloud_view_files')

def reject_file(request,id):
    reject=get_object_or_404(fileModel,file_id=id)
    reject.status='Rejected'
    reject.save(update_fields=['status'])
    reject.save()
    return redirect('cloud_view_files')      


def cloud_view_enclave_status(request):
    data=requestModel.objects.filter(enclave_status="Accepted")

    if request.method=='POST':
         search=request.POST.get('search')
         data=requestModel.objects.filter(Q(request_id__icontains=search) | Q(file_name__icontains=search))
    return render(request,'cloud/cloud-view-enclave-status.html',{'data':data})

def view_enclave_status(request,id):
    user_id=request.session['user_id']
    data=userModel.objects.get(user_id=user_id)
    email=data.email
  


    data=fileModel.objects.get(file_id=id)
    print("sssssssssssssssssssssssssssssssssssssssssssssss")
    print(data)
    file_key=data.file_key
    print('ffffffffffffffffffffffffffffffffffffff')
    # otp=random.randint(111111,999999)
    html_content =file_key
    from_mail = DEFAULT_FROM_EMAIL
    to_mail = [email]
    print(email)
    msg = EmailMultiAlternatives("Welcome to Dual Access Control in Cloud, Your Private Key is",html_content,from_mail,to_mail)
    msg.attach_alternative(html_content,"text/html")
    if connect():
        msg.send()
    # requestModel.objects.filter(request_id=id).update(otp=otp)
    # print(otp)
   

    requestModel.objects.filter(file_id=id).update(key_status="Sended")

    

    return redirect('cloud_view_enclave_status')
 

def key_status(request,id):
  
    return redirect('cloud_view_enclave_status')
    
