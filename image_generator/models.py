from django.db import models

# Create your models here.

class GeneratedImage(models.Model):
    image = models.ImageField(upload_to='generated_images/')
    prompt = models.CharField(max_length=255)
    model = models.CharField(max_length=255, default='runwayml/stable-diffusion-v1-5')
    style = models.CharField(max_length=255, default=',Die-cut sticker,white background, illustration minimalism, vector, pastel colors')
    created_at = models.DateTimeField(auto_now_add=True)
    shared = models.BooleanField(default=True)


    def __str__(self):
        return self.prompt