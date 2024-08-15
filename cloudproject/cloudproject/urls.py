"""cloudproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ast import If
from xml.dom.minidom import Document


from django.conf.urls.static import static
from django.conf import settings
from cloudapp import views as cloudapp_views
from userapp import views as userapp_views
from mainapp import views as mainapp_views
from ownerapp import views as ownerapp_views
from enclaveapp import views as enclaveapp_views
from authorityapp import views as authorityapp_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('',mainapp_views.home,name='home'),



# cloud

   

    path('cloud_login',cloudapp_views.cloud_login,name='cloud_login'),

    path('cloud_dashboard', cloudapp_views.cloud_dashboard,name='cloud_dashboard'),

    path('cloud_view_owners', cloudapp_views.cloud_view_owners,name='cloud_view_owners'),

    path('cloud_download_request', cloudapp_views.cloud_download_request,name='cloud_download_request'),

    path('accept_owner/<int:id>/',cloudapp_views.accept_owner,name='accept_owner'),

    path('reject_owner/<int:id>/',cloudapp_views.reject_owner,name='reject_owner'),

    path('cloud_view_files', cloudapp_views.cloud_view_files,name='cloud_view_files'),

    path('accept_file/<int:id>/',cloudapp_views.accept_file,name='accept_file'),

    path('reject_file/<int:id>/',cloudapp_views.reject_file,name='reject_file'),

    path('accept_forword/<int:id>/',cloudapp_views.accept_forword,name='accept_forword'),

    path('reject_forword/<int:id>/',cloudapp_views.reject_forword,name='reject_forword'),

    path('cancel_forword/<int:id>/',cloudapp_views.cancel_forword,name='cancel_forword'),

    path('cloud_view_enclave_status', cloudapp_views.cloud_view_enclave_status,name='cloud_view_enclave_status'),

    path('view_enclave_status/<int:id>/', cloudapp_views.view_enclave_status,name='view_enclave_status'),

    path('key_status/<int:id>/', cloudapp_views.key_status,name='key_status'),
# authority

    path('authority_login',authorityapp_views.authority_login,name='authority_login'),

    path('authority_dashboard', authorityapp_views.authority_dashboard,name='authority_dashboard'),

    path('authority_view_users', authorityapp_views.authority_view_users,name='authority_view_users'),

    path('authority_cloud_request', authorityapp_views.authority_cloud_request,name='authority_cloud_request'),

    path('accept_user/<int:id>/',authorityapp_views.accept_user,name='accept_user'),

    path('reject_user/<int:id>/',authorityapp_views.reject_user,name='reject_user'),

    




# enclave
   
    path('enclave_login',enclaveapp_views.enclave_login,name='enclave_login'),

    path('enclave_dashboard', enclaveapp_views.enclave_dashboard,name='enclave_dashboard'),

    path('enclave_cloud_request', enclaveapp_views.enclave_cloud_request,name='enclave_cloud_request'),

    path('accept_enclave_status/<int:id>/',enclaveapp_views.accept_enclave_status,name='accept_enclave_status'),

    path('reject_enclave_status/<int:id>/',enclaveapp_views.reject_enclave_status,name='reject_enclave_status'),

# user
  

    # 
    
    # path('user_otp',userapp_views.user_otp,name='user_otp'),
    
    # path('my_downloads/<>/',userapp_views.my_downloads,name='my_downloads'),




    path('user_otp',userapp_views.user_otp,name='user_otp'),

    path('user_login',userapp_views.user_login,name='user_login'),

    path('user_register', userapp_views.user_register,name='user_register'),

    path('user_dashboard', userapp_views.user_dashboard,name='user_dashboard'),

    path('user_search_files',userapp_views.user_search_files,name='user_search_files'),

    path('user_download_files/<int:id>/',userapp_views.user_download_files,name='user_download_files'),

    # path('user_download_request/<int:id>/',userapp_views.user_download_request,name='user_download_request'),


    path('download_file',userapp_views.download_file,name='download_file'),

    # path('user_downloads',userapp_views.user_downloads,name='user_downloads'),

    path('download_btn/<int:id>/', userapp_views.download_btn,name='download_btn'), 
   

    path('user_profile',userapp_views.user_profile,name='user_profile'),

    path('user_response',userapp_views.user_response,name='user_response'),




   
# Owner
   
    # path('user_otp',ownerapp_views.user_otp,name='user_otp'),
    # path('owner_otp',ownerapp_views.owner_otp,name='owner_otp'),
    path('owner_otp',ownerapp_views.owner_otp,name='owner_otp'),

    path('owner_login',ownerapp_views.owner_login,name='owner_login'),

    # path('owner_file_status',ownerapp_views.owner_file_status,name='owner_file_status'),

    path('owner_register', ownerapp_views.owner_register,name='owner_register'),

    path('owner_dashboard', ownerapp_views.owner_dashboard,name='owner_dashboard'),

    path('owner_upload_files',ownerapp_views.owner_upload_files,name='owner_upload_files'),

    # path('upload_files',ownerapp_views.upload_files,name='upload_files'),


    path('owner_view_files',ownerapp_views.owner_view_files,name='owner_view_files'),

    path('owner_edos_attacks',ownerapp_views.owner_edos_attacks,name='owner_edos_attacks'),

    path('owner_profile',ownerapp_views.owner_profile,name='owner_profile'),

    path('owner_encrypt_files',ownerapp_views.owner_encrypt_files,name='owner_encrypt_files'),



]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
