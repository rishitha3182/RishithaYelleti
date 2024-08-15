from django.shortcuts import render

from re import M
from django.shortcuts import render
from ast import Pass
from dataclasses import field
from tkinter.tix import COLUMN
from urllib import request
from email.headerregistry import Address
from unicodedata import name
from django.contrib import messages
from tabnanny import check
from django.shortcuts import render
from cloudproject.settings import ALLOWED_HOSTS
from ownerapp.models import *
from userapp.models import *
from django.shortcuts import render,redirect,get_object_or_404
from ownerapp.views import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Q
import random
import requests
from cryptography.fernet import Fernet 
from mainapp.check_internet import *
# Create your views here.

ALLOWED_EXTENSIONS=set(['txt','py','html'])


def owner_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)

        try:
            check = ownerModel.objects.get(email=email,password=password)
            print(check)
            request.session["owner_id"] = check.owner_id
            status = check.status
            
            if status == "Pending":
                messages.warning(request,"Your account is not activated yet")
                return redirect('owner_login')

            elif status == "Rejected":
                messages.warning(request,"Your account has been Rejected")
                return redirect('owner_login')

              

            else:
                return redirect('owner_dashboard')

        except:
            messages.warning(request,"Invalid username or password")
            return redirect('owner_login')

    return render(request,'owner/owner-login.html')



def owner_register(request):
    if request.method=='POST' and request.FILES['owner_image']:
        print("ggggggggggggggggggggggggggggggg")
        owner_name=request.POST ['owner_name'] 
        print(owner_name)
        email=request.POST['email']       
        password=request.POST['password']
        mobile=request.POST['mobile']
        dob=request.POST['dob']
        location=request.POST['location']
        owner_image=request.FILES['owner_image']
        
        if ownerModel.objects.filter(email=email).filter(verification = "verified"):
            messages.warning(request,"Email  Already  Exists!")
            print("Already")
        elif ownerModel.objects.filter(email=email).filter(verification = "Pending"):
            messages.warning(request,"Already Rejistered, Just verify your account!")
            otp=random.randint(2222,4444)
            ownerModel.objects.filter(email=email,verification='Pending').update(otp=otp)
            url = "https://www.fast2sms.com/dev/bulkV2"
            # create a dictionary
            my_data = {'sender_id': 'FSTSMS', 
                        'message': 'Welcome to Dual Access Control in Cloud, your verification OPT is '+str(otp)+'Thanks for request of OTP.', 
                        'language': 'english', 
                        'route': 'p', 
                        'numbers': mobile
            }

            # create a dictionary
            headers = {
                'authorization': 'D4vuFnk1sNQOl6SRpfZUT23ewPX0BoLrzAJVgqtW8bxyHEGjImfkE0NtULg1TG9xImYHpVZjQMnBSOoa',
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache"
            }
            
            if connect():

            # make a post request
                response = requests.request("POST",
                                            url,
                                            data = my_data,
                                            headers = headers)
            
                print(response.text)      
            return redirect('owner_login')  

        else:
            print("vssdvsdvsd")
            otp=random.randint(2222,4444)
            url = "https://www.fast2sms.com/dev/bulkV2"
            # create a dictionary
            my_data = {'sender_id': 'FSTSMS', 
                        'message': 'Welcome to CloudHost, your verification OPT is '+str(otp)+'Thanks for request of OTP.', 
                        'language': 'english', 
                        'route': 'p', 
                        'numbers': mobile
            }

            # create a dictionary
            headers = {
                'authorization': 'D4vuFnk1sNQOl6SRpfZUT23ewPX0BoLrzAJVgqtW8bxyHEGjImfkE0NtULg1TG9xImYHpVZjQMnBSOoa',
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache"
            }

            if connect():
            # make a post request
                response = requests.request("POST",
                                            url,
                                            data = my_data,
                                            headers = headers)
            
                print(response.text)        

            ownerModel.objects.create(owner_name=owner_name,password=password,mobile=mobile,email=email,dob=dob,location=location,owner_image=owner_image,otp=otp)
            messages.success(request,'Account Created Successfully!')
            return redirect('owner_login')
    return render(request,'owner/owner-register.html')

def owner_otp(request):
    # owner_id=request.session['owner_id']

    if request.method == "POST":
        otp = request.POST.get('otp')
        print(otp)
        try:
            print('ppppppppppppppppppppp')
            check = ownerModel.objects.get(otp=otp)
            owner_id = request.session['owner_id']=check.owner_id
            otp=check.otp
            print(otp)
            if otp == otp:
                ownerModel.objects.filter(owner_id=owner_id).update(verification='Verified')
                messages.info(request,'Account Created Successfully!')
                return redirect('owner_login')
            else:
                return redirect('owner_otp')
        except:
            pass
    return render(request,'owner/owner-otp.html')
            



def owner_dashboard(request):
    owners=ownerModel.objects.count()
    users=userModel.objects.count()
    uploads=fileModel.objects.count()
    requests=requestModel.objects.count()
    return render(request,'owner/owner-dashboard.html',{'owners':owners, 'users':users, 'uploads':uploads,'requests':requests})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 


def owner_upload_files(request):
      
    if request.method=='POST' and 'file' in request.FILES:
        file = request.FILES['file']
        print(file)
        description = request.POST['description']
        print(description)
        file_name=file.name
        file_size=file.size
        file_type=file.content_type
        user_id=request.session["owner_id"]
        owner_id=request.session["owner_id"]

        if not allowed_file(file_name):
            messages.warning(request,"Allowed File Types are: txt, html, py")
            return redirect('owner_upload_files')

        key = Fernet.generate_key()
        file_key = key.decode()

        if fileModel.objects.filter(file_name=file_name):
         messages.warning(request,"File Already Exists")
         return redirect('owner_upload_files')
     
        else:
            data_storage=fileModel.objects.create(file=file,file_name=file_name,file_size=file_size,file_type=file_type,user_id=user_id,owner_id=owner_id,description=description,file_key=file_key)
            data_storage.save()

        #File Encryption



        print('ggggggggggggggggggggggggggggggggggggggggggg')
        if data_storage:
             messages.info(request,"Uploaded Successfully")
             request.session['file_name'] = file_name
             return redirect ('owner_encrypt_files')
    #     print(messages)
        else:
            messages.info(request,"Something Wrong, Please try again.")
           
    return render(request,'owner/owner-upload-files.html')    




def owner_encrypt_files(request):
    
    file_name = request.session["file_name"]
    path = 'media/files/' + file_name
    file_data = ''
    
    
    file = open(path,'r')
    file_data=str(file.read())    
    file.close()
    key = fileModel.objects.get(file_name=file_name)

    if request.method=='POST':
        
        file = open(path,'rb')
        file_data = file.read()        
        file.close()
      
        f = Fernet(key.file_key)
        file_data = f.encrypt(file_data)
       
        fi = open(path,'wb')
        fi.write(file_data)
        fi.close()

        fileModel.objects.filter(file_name=file_name,file_key=key.file_key).update(file_data=file_data)
        messages.info(request,"Encrypted Successfully.")
        return redirect('owner_dashboard')
    return render(request,'owner/owner-encript-files.html',{'filename': file_name,'file':file_data})




def owner_view_files(request):
    owner_id=request.session["owner_id"]
    data = fileModel.objects.filter(owner_id=owner_id)
    print(owner_id)
    return render(request,'owner/owner-view-files.html',{'data':data})




def owner_profile(request):
    owner_id=request.session["owner_id"]
    data = ownerModel.objects.get(owner_id=owner_id)
    obj = get_object_or_404(ownerModel,owner_id=owner_id)
    if request.method=='POST':
        print('ftttyy')
        owner_name=request.POST['owner_name']
        print(owner_name)
        email=request.POST['email']
        mobile=request.POST['mobile']
        location=request.POST['location']
        dob = request.POST['dob']
        password = request.POST['password'] 
        print('ddddddddddddddddddddd')
        if len(request.FILES) != 0:
            print("ggggggggggggggggggggggggggggggg")
            owner_image = request.FILES['owner_image']
            obj.owner_name = owner_name
            obj.mobile = mobile
            obj.email = email
            obj.location =location
            obj.dob = dob
            obj.password = password
            obj.owner_image = owner_image
            obj.save(update_fields=['owner_name','mobile','email','location','owner_image','dob','password'])
            obj.save()

   
        else:
            obj.owner_name = owner_name
            obj.mobile = mobile
            obj.email = email
            obj.location =location
            obj.dob = dob
            obj.password = password
            obj.save(update_fields=['owner_name','mobile','email','location','dob','password'])
            obj.save()
            messages.info(request,'Updated Successfully!')
    return render(request,'owner/owner-profile.html',{'data':data})

  
def owner_edos_attacks(request):

   data=userModel.objects.filter(status="Blocked")
   return render(request,'owner/owner-edos-attacks.html',{'data':data})
