from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Prompt(models.Model):
    prompt = models.CharField(max_length=4000)
    result = models.CharField(max_length=100,default="")
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    uploaded_at = models.DateTimeField(auto_now_add=True)