import os
import uuid
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from imageaiapp.models import *
from diffusers import DiffusionPipeline , StableDiffusionPipeline

class Command(BaseCommand):
    def handle(self, *a, **kw):
        print('Mocking Data for New website')

        # 1. Create User
        USERS = [
            ['a', 'a@ubu.ac.th', 'aaa'],
            ['b', 'b@ubu.ac.th', 'bbb'],
            ['c', 'c@ubu.ac.th', 'ccc'],
            ['d', 'd@ubu.ac.th', 'ddd'],
            ['e', 'e@ubu.ac.th', 'eee'],
        ]
        users = []
        for u in USERS:
            user, created = User.objects.get_or_create(username=u[0], email=u[1])
            user.set_password(u[2])
            user.save()
            users.append(user)

        # 2. create questions
        Prompts = [
            'a photo of an astronaut riding a horse on mars',
        ]
        for q in Prompts:
            media = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2",safety_checker=None)
            media.enable_sequential_cpu_offload()
            media.enable_attention_slicing("max")
            image = media(q).images[0]
            result = f'{uuid.uuid4()}'
            file_name = f'media/{result}.png'
            image.save(file_name)
            prompt = Prompt(prompt=prompt,result=result)
            prompt.save()
            '''qq, created = Prompt.objects.get_or_create(
                user=users[randint(0, len(users)-1)],
                prompt=q)
            qq.save()'''
