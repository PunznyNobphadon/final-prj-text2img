from django.db import models

# Create your models here.

class GeneratedImage(models.Model):
    image = models.ImageField(upload_to='generated_images/')
    prompt = models.CharField(max_length=255)
    model = models.CharField(max_length=255, default='Ojimi/anime-kawai-diffusion')
    style = models.CharField(max_length=255, default='Sticker')
    created_at = models.DateTimeField(auto_now_add=True)
    shared = models.BooleanField(default=False)


    def __str__(self):
        return self.prompt