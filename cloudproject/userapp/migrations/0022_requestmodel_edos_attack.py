# Generated by Django 4.0.4 on 2022-06-03 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0021_usermodel_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestmodel',
            name='edos_attack',
            field=models.CharField(default='Pending', max_length=50, null='True'),
            preserve_default='True',
        ),
    ]
