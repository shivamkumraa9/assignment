from django.db import models
from django.contrib.auth.models import User,AbstractUser


class MyUser(AbstractUser):
   username = models.CharField(max_length=150,unique=False,blank=True)	
   email = models.EmailField(unique = True)
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']

   def __str__(self):
   	return self.email


class UserAuth(models.Model):
	secret_key = models.CharField(max_length = 255)
	has_two = models.BooleanField(default = False)
	user = models.OneToOneField(MyUser,on_delete = models.CASCADE)

	def __str__(self):
		return f"{self.user.email} : Auth"