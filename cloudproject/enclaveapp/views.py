
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

import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd

# Create your views here.



def enclave_login(request):
    if request.method=='POST':
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        if name=='enclave' and pwd=='enclave':
            messages.info(request,"login successfull")
            return redirect('enclave_dashboard')
        else:
            messages.warning(request,'Something Wrong, Please try again.')
            return redirect ('enclave_login')
            
    return render(request,'main/enclave-login.html')



def enclave_dashboard(request):
    owners=ownerModel.objects.count()
    users=userModel.objects.count()
    uploads=fileModel.objects.count()
    requests=requestModel.objects.count()
    attacks=userModel.objects.filter(status='Blocked').count()
    a_users=userModel.objects.filter(status='Accepted').count()
    a_file=fileModel.objects.filter(status='Accepted').count()
    return render(request,'enclave/enclave-dashboard.html',{'owners':owners, 'users':users, 'uploads':uploads,'requests':requests,'attacks':attacks,'a_users':a_users,'a_file':a_file})    





def enclave_cloud_request(request):
    data=requestModel.objects.filter(status="Forwarded").order_by("requested_date")

    if request.method=='POST':
         search=request.POST.get('search')
         data=requestModel.objects.filter(Q(request_id__icontains=search) | Q(file_name__icontains=search))
        
    return render(request,'enclave/enclave-cloud-request.html',{'data':data})    




def accept_enclave_status(request,id):
    accept=get_object_or_404(requestModel,request_id=id)
    accept.enclave_status='Accepted'
    accept.save(update_fields=['enclave_status'])
    accept.save()
    return redirect('enclave_cloud_request')

def reject_enclave_status(request,id):
    reject=get_object_or_404(requestModel,request_id=id)
    reject.enclave_status='Rejected'
    reject.save(update_fields=['enclave_status'])
    reject.save()
    return redirect('enclave_cloud_request') 




# def cloud_view_files(request):
#     data=fileModel.objects.all().order_by("file_uploaded_date")
#     if request.method=="POST" :
#      search=request.POST.get('search')
#      data=fileModel.objects.filter(Q(file_id__icontains=search) | Q(file_name__icontains=search)  | Q(file__icontains=search) | Q(file_type__icontains=search) | Q(file_size__icontains=search) | Q(file_uploaded_date__icontains=search))
#     return render(request,'cloud/cloud-view-files.html',{'data':data})



# def accept_file(request,id):
#     accept=get_object_or_404(fileModel,file_id=id)
#     accept.status='Accepted'
#     accept.save(update_fields=['status'])
#     accept.save()
#     return redirect('cloud_view_files')

# def reject_file(request,id):
#     reject=get_object_or_404(fileModel,file_id=id)
#     reject.status='Rejected'
#     reject.save(update_fields=['status'])
#     reject.save()
#     return redirect('cloud_view_files')      



# def cloud_view_top_k_download_files(request):
#     data=fileModel.objects.all().order_by("-download_rank")
#     if request.method=="POST" :
#      search=request.POST.get('search')
#      data=fileModel.objects.filter(Q(file_id__icontains=search) | Q(file_name__icontains=search)  | Q(file__icontains=search) | Q(file_type__icontains=search) | Q(file_size__icontains=search) | Q(file_uploaded_date__icontains=search)).order_by('-download_rank')
#     return render(request,'cloud/top-k-download-files.html',{'data':data})



# def cloud_view_top_k_search_files(request):
#     data=fileModel.objects.all().order_by("-search_rank")
#     if request.method=="POST" :
#      search=request.POST.get('search')
#      data=fileModel.objects.filter(Q(file_id__icontains=search) | Q(file_name__icontains=search)  | Q(file__icontains=search) | Q(file_type__icontains=search) | Q(file_size__icontains=search) | Q(file_uploaded_date__icontains=search)).order_by('-search_rank')
#     return render(request,'cloud/top-k-search-files.html',{'data':data})    




# def download_graph(request):
   
#     data = fileModel.objects.all ()
#     context = {"data":data}
   
#     return render(request,'cloud/download-graph.html', context)


# def search_graph(request):
   
#     data = fileModel.objects.all ()
#     context = {"data":data}
   
#     return render(request,'cloud/search-graph.html', context)    
