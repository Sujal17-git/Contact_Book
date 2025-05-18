from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female')])

class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='contacts')
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name