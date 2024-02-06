from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from imageaiapp.models import *
from imageaiapp.forms import PromptForm
import torch, torchvision, io
from torchvision import transforms
from PIL import Image
from django.core.files.base import ContentFile
from diffusers import DiffusionPipeline , StableDiffusionPipeline
import uuid
# Create your views here.

#@login_required
def home(req):
    return render(req,"imageaiapp/home.html")

def diffuse(prompt):
    pipeline = DiffusionPipeline.from_pretrained(
        'runwayml/stable-diffusion-v1-5', 
        use_safetensors=True)
    image = pipeline(prompt).images[0]
    return ContentFile(image.getvalue())

#def ddpm(prompt):
    #from diffusers import DDPMPipeline
    #ddpm = DDPMPipeline.from_pretrained("google/ddpm-cat-256", use_safetensors=True)
    #image = ddpm(num_inference_steps=25).images[0]
    #image.save('ddpm/result.png')

def ddpm(prompt):
    ddpm = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2",safety_checker=None)
    ddpm.enable_sequential_cpu_offload()
    ddpm.enable_attention_slicing("max")
    image = ddpm(prompt).images[0]
    #file_name = f'ddpm/imageforyou_{uuid.uuid4()}.png'
    file_name = f'ddpm/imageforyou.png'
    image.save(file_name)

def imageai(req):
    form = PromptForm()
    if req.method == 'POST':
        form = PromptForm(req.POST)
        if form.is_valid():
            ddpm(form.instance.prompt)
            #result = diffuse(form.instance.prompt)
            #form.instance.result.save(f'{form.instance.id}', result)
            form.save()
    return render(req, 'imageaiapp/imageai.html', {
                      'form': form,
                      'prompts': Prompt.objects.all().order_by('-uploaded_at')
                  })

def logins(request):
    print(f'request.method = {request.method}')
    if request.method == 'POST':
        #print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # User.objects.filter(username=username, password=password).first()
        u = authenticate(username=username, password=password)
        if u:
            auth_login(request, u)
            print('authenticate & logged in')
            return redirect('/')
    return render(request,'imageaiapp/logins.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def registers(request):
    print(f'request.method = {request.method}')
    if request.method == 'POST':
        #print(request.POST)
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            u = User.objects.filter(username=username).first()
            if u:
                print(f'มีผู้ใช้ชื่อ {username} อยู่แล้ว')
                #u.set_password(password1)
                #u.save()
            else:
                User.objects.create_user(username=username, password=password1)
                print(f'สร้าง username={username} password={password1} แล้ว')
            return redirect('/logins/')
    return render(request, 'imageaiapp/registers.html')