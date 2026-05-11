from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
    contact = models.CharField(max_length=12)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'register'
