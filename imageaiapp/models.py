from django.db import models

# Create your models here.
class Prompt(models.Model):
    prompt = models.CharField(max_length=4000)
    result = models.ImageField(upload_to='diffuse-result',
                               blank=True,
                               null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)