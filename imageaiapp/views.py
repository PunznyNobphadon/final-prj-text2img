from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from imageaiapp.models import *
from imageaiapp.forms import PromptForm
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
from django.core.files.base import ContentFile
from diffusers import DiffusionPipeline , StableDiffusionPipeline
import uuid
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import numpy; np = numpy
import diffusers

def home(req):
    return render(req,"imageaiapp/home.html")

'''def diffuse(prompt):
    pipeline = DiffusionPipeline.from_pretrained(
        'runwayml/stable-diffusion-v1-5', 
        use_safetensors=True)
    image = pipeline(prompt).images[0]
    return ContentFile(image.getvalue())'''

'''def ddpm(prompt):
    from diffusers import DDPMPipeline
    ddpm = DDPMPipeline.from_pretrained("google/ddpm-cat-256", use_safetensors=True)
    image = ddpm(num_inference_steps=25).images[0]
    image.save('ddpm/result.png')'''

def media(prompt,user):
    model_id = "stabilityai/stable-diffusion-2"
    #เหตุผลที่เลือก model ตัวนี้เพราะสามารถใช้ LoRA
    #LoRA คือ model อีกประเภทที่เป็นส่วนเสริม ซึ่งจะถูกเรียกใช้หลัง checkpoint ได้ทำการวาดรูปมาแล้วก่อนหน้า เช่น LoRA หน้านาย A เพราะต่อให้ checkpoint ถูกเรียนรู้มาเยอะแค่ไหน มันก็ไม่รู้เฉพาะเจาะจงอะไรแบบนี้ LoRA เป็นส่วนเสริม เราอาจจะสั่งให้ checkpoint หลักวาดผู้ชายนั่งใต้ต้นไม้ แล้วใส่ LoRA หน้านาย A เข้าไป รูปที่ออกมามันจะเป็น นาย A นั่งใต้ต้นไม้
    media = StableDiffusionPipeline.from_pretrained(model_id,safety_checker=None)
    media.enable_sequential_cpu_offload()
    media.enable_attention_slicing("max")
    image = media(prompt).images[0]
    result = f'{uuid.uuid4()}'
    file_name = f'media/{result}.png'
    #file_name = f'images/bg_image1.png'
    image.save(file_name)
    #prompt = Prompt(prompt=Prompt,result=result)
    #prompt.save()

def imageai(req):
    form = PromptForm()
    if req.method == 'POST':
        form = PromptForm(req.POST)
        if form.is_valid():
            media(req.POST.get("prompt"),req.user)
    return render(req, 'imageaiapp/imageai.html', {
                      'form': form,
                      'prompts': Prompt.objects.all().order_by('-uploaded_at')
                  })

def logins(request):
    print(f'request.method = {request.method}')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        User.objects.filter(username=username, password=password).first()
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
        print(request.POST)
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
            return redirect('/login/')
    return render(request, 'imageaiapp/registers.html')


def sign_in(request):
    return render(request, 'imageaiapp/sign_in.html')

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('/')


def sign_out(request):
    del request.session['user_data']
    return redirect('/login/')