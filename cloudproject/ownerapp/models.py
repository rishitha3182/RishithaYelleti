from django.db import models

# Create your models here.
class ownerModel(models.Model):
    owner_id=models.AutoField(primary_key=True)
    owner_name=models.CharField(help_text='owner_name',max_length=50)
    email=models.EmailField(help_text=' email', max_length=50)
    password=models.CharField(help_text='password', max_length=50)
    mobile=models.BigIntegerField(help_text='mobile')
    location=models.CharField(help_text='location', max_length=200)
    dob=models.DateField(help_text='dob')
    owner_image=models.ImageField(upload_to='owner_image')
    status=models.CharField(max_length=50,default='Pending',null="True")
    verification=models.CharField(max_length=50,default='Verified')
    otp=models.IntegerField(null=True)
    reg_date=models.DateField(auto_now_add=True)

    class Meta:
        db_table='owner_details'




class fileModel(models.Model):
    file_id=models.AutoField(primary_key=True)
    owner_id=models.IntegerField(null=True)
    user_id=models.IntegerField(null=True)
    file=models.FileField(upload_to='files/')
    file_name=models.CharField(help_text='file_name',max_length=200)
    description=models.CharField(help_text='description',max_length=250, null=True)
    file_size=models.BigIntegerField(help_text='file_size',null=True)
    file_type=models.CharField(help_text='file_type',max_length=300)
    file_key=models.CharField(null=True,max_length=200)
    file_data=models.TextField(null=True)
    search_rank = models.CharField(default="0",null=True, max_length=200)
    download_rank = models.CharField(default="0",null=True, max_length=250)
    # otp=models.IntegerField(null=True)
    status=models.CharField(max_length=50,default='Pending',null="True")
    file_uploaded_date=models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table='file_details'       