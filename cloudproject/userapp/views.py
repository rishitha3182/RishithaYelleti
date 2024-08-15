from django.shortcuts import render


# Create your views here.


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
from userapp.models import *
from ownerapp.models import *
from django.shortcuts import render,redirect,get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Q, F
import random
import requests
from cryptography.fernet import Fernet
from mainapp.check_internet import *
# Create your views here.




def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)

        try:
            check = userModel.objects.get(email=email,password=password)
            print(check)
            request.session["user_id"] = check.user_id
            status = check.status
            
            if status == "Pending":
                messages.warning(request,"Your account is not activated yet")
                return redirect('user_login')

            elif status == "Rejected":
                messages.warning(request,"Your account has been Rejected")
                return redirect('user_login')

            else:
                return redirect('user_dashboard')

        except:
            messages.warning(request,"Invalid username or password")
            return redirect('user_login')


    return render(request,'user/user-login.html')


#user register
def user_register(request):
    if request.method=='POST' and request.FILES['user_image']:
        user_name=request.POST ['user_name']
        print(user_name) 
        email=request.POST['email']       
        password=request.POST['password']
        mobile=request.POST['mobile']
        dob=request.POST['dob']
        location=request.POST['location']
        user_image=request.FILES['user_image']


        if userModel.objects.filter(email=email).filter(verification = "verified"):
            messages.warning(request,"Email  Already  Exists!")
            print("Already")
        elif userModel.objects.filter(email=email).filter(verification = "Pending"):
            messages.warning(request,"Already Rejistered, Just verify your account!")
            otp=random.randint(2222,4444)
            userModel.objects.filter(email=email,verification='verified').update(otp=otp)
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
            return redirect('user_login')  

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

            userModel.objects.create(user_name=user_name,password=password,mobile=mobile,email=email,dob=dob,location=location,user_image=user_image,otp=otp)
            messages.success(request,'Account Created Successfully!')
            return redirect('user_login')
    return render(request,'user/user-register.html')

def user_otp(request):
    # user_id=request.session['user_id']

    if request.method == "POST":
        otp = request.POST.get('otp')
        print(otp)
        try:
            print('ppppppppppppppppppppp')
            check = userModel.objects.get(otp=otp)
            user_id = request.session['user_id']=check.user_id
            otp=check.otp
            print(otp)
            if otp == otp:
                userModel.objects.filter(user_id=user_id).update(verification='Verified')
                messages.info(request,'Account Created Successfully!')
                return redirect('user_login')
            else:
                return redirect('user_otp')
        except:
            pass
    return render(request,'user/user-otp.html')
        


def user_dashboard(request):
    owners=ownerModel.objects.count()
    users=userModel.objects.count()
    uploads=fileModel.objects.count()
    requests=requestModel.objects.count()
    return render(request,'user/user-dashboard.html',{'owners':owners, 'users':users, 'uploads':uploads,'requests':requests})

def user_search_files(request):
   
    data=fileModel.objects.filter(status="Accepted")

    if request.method=="POST":
      
        search=request.POST.get('search')
        print(search)
        data=fileModel.objects.filter(Q(file_name__contains=search))
        print(search)
     
    return render(request,'user/user-search-files.html',{'data':data})
       
 
     
def download_btn(request,id):
    request.session["file_id"] = id
    key=fileModel.objects.get(file_id=id)
    file_key = str(key.file_key)
    if request.method == "POST":
        print("ggggggggggggggggggggggggggggggggggg")
        entered_key = request.POST.get('otp')
        print(type(entered_key))
        print(file_key,type(file_key))
        try:           
            if entered_key == file_key:
                print(entered_key == file_key)
                f= Fernet(file_key)
                print("eeeeeeeeeee")
                
                file_name=fileModel.objects.get(file_key=file_key)
                print(file_name.file_name)
                path = 'media/files/' + file_name.file_name

                file = open(path,'rb')
                print('file')
                enc_data = file.read()
                dec_data = f.decrypt(enc_data)
                print('dec_data')

                fi = open(path,'wb')
                fi.write(dec_data)
                messages.info(request,'')
                return redirect('download_file')
           
        except Exception as e:
            
            print(e)
            user_id = request.session['user_id']
            userModel.objects.filter(user_id=user_id).update(status='Accepted')
            # requestModel.objects.filter(user_id=user_id).update(edos_attack='Attacked')
            return redirect('download_file')
            

    return render(request,'user/download-otp.html')


def download_otp(request):
    
     return render(request,'user/download-otp.html')


def download_file(request):
    print("aaaaaaaaa")
    # print(id)
    print("bbbbbbbbbb")
    filedetails = fileModel.objects.get(file_id=request.session["file_id"])
    file_id=filedetails.file_id 
    file_name = filedetails.file_name
    file=filedetails.file
    file_size = filedetails.file_size
    file_type=filedetails.file_type
    file=filedetails.file
    description=filedetails.description
    file_uploaded_date=filedetails.file_uploaded_date

    print(file) 

    return render(request,'user/download-file.html',{'file_id':file_id,'file':file,'file_type':file_type,'file_name':file_name,'file_size':file_size,'file_uploaded_date':file_uploaded_date,'description':description})



def user_response(request):
    return render(request,'user/user-response.html')


def user_download_files(request,id):
    user_id=request.session["user_id"]
    filedetails = fileModel.objects.get(file_id= id)
    owner_id=filedetails.owner_id
    file_id=filedetails.file_id 
    file_name = filedetails.file_name
    file=filedetails.file
    file_size = filedetails.file_size
    file_type=filedetails.file_type
    print(file_type)
    file=filedetails.file
    description=filedetails.description
    print(description) 
    file_uploaded_date=filedetails.file_uploaded_date
    requestModel.objects.create(file_name=file_name,file=file,file_size=file_size,user_id=user_id,owner_id=owner_id,description=description,file_type=file_type,file_id=file_id)
    print('ddddddddddddddddddddd') 
    return render(request,'user/user-download-files.html',{'file_id':file_id,'file':file,'file_type':file_type,'file_name':file_name,'file_size':file_size,'file_uploaded_date':file_uploaded_date,'description':description})




  
def user_profile(request):
    user_id=request.session["user_id"]
    data = userModel.objects.get(user_id=user_id)
    obj = get_object_or_404(userModel,user_id=user_id)
    if request.method=='POST':
        print('ftttyy')
        user_name=request.POST['user_name']
        print(user_name)
        email=request.POST['email']
        mobile=request.POST['mobile']
        location=request.POST['location']
        dob = request.POST['dob']
        password = request.POST['password']
        print('ddddddddddddddddddddd')
        if len(request.FILES) != 0:
            print("ggggggggggggggggggggggggggggggg")
            user_image = request.FILES['user_image']
            obj.user_name = user_name
            obj.mobile = mobile
            obj.email = email
            obj.location =location
            obj.dob = dob
            obj.password = password
            obj.user_image = user_image
            obj.save(update_fields=['user_name','mobile','email','location','user_image','dob','password'])
            obj.save()

   
        else:
            obj.user_name = user_name
            obj.mobile = mobile
            obj.email = email
            obj.location =location
            obj.dob = dob
            obj.password = password
            obj.save(update_fields=['user_name','mobile','email','location','dob','password'])
            obj.save()
            messages.info(request,'Updated Successfully!')
    return render(request,'user/user-profile.html',{'data':data})


    
