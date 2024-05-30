import io
from django.contrib.auth import logout
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from image_generator.forms import GeneratedImageForm ,UserRegisterForm, UserUpdateForm
from image_generator.models import GeneratedImage
from django.contrib.auth.decorators import login_required , user_passes_test
from diffusers import DiffusionPipeline ,StableDiffusionPipeline

def is_admin(user):
    return user.is_staff

# Generator
@login_required
def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        model_id = request.POST.get('model')
        style = request.POST.get('style')

        prompt_with_style = f"{prompt}, {style}"

        # เลือกโมเดลตามที่กำหนด
        if model_id == "Ojimi/anime-kawai-diffusion":
            pipe = DiffusionPipeline.from_pretrained(model_id)
            pipe.enable_sequential_cpu_offload()
            pipe.enable_attention_slicing("max")
        elif model_id == "runwayml/stable-diffusion-v1-5":
            pipe = StableDiffusionPipeline.from_pretrained(model_id, safety_checker=None)
            pipe.enable_sequential_cpu_offload()
        elif model_id == "stabilityai/stable-diffusion-2":
            pipe = StableDiffusionPipeline.from_pretrained(model_id, safety_checker=None)
            pipe.enable_sequential_cpu_offload()
            pipe.enable_attention_slicing("max")
        elif model_id == "stabilityai/stable-diffusion-2-1-base":
            pipe = StableDiffusionPipeline.from_pretrained(model_id, safety_checker=None)
            pipe.enable_sequential_cpu_offload()
            pipe.enable_attention_slicing("max")
        
        generated_image = pipe(prompt_with_style , negative_prompt="lowres, bad anatomy, inappropriate content, explicit, suggestive").images[0]
        
        # บันทึกรูปภาพ
        img_name = f'{prompt}.png'
        img_path = f'media/generated_images/{img_name}'
        generated_image.save(img_path)
        
        # บันทึกภาพไปยังข้อมูลที่กำหนด
        new_image = GeneratedImage.objects.create(prompt=prompt, image=f'generated_images/{img_name}')
        
        return redirect('display_image', pk=new_image.pk)

    return render(request, 'image_generator/generate_image.html')

@login_required
def display_image(request, pk):
    image = GeneratedImage.objects.get(pk=pk)
    if request.method == 'POST':
        share_action = request.POST.get('share_action')
        if share_action == 'share':
            image.shared = True
        elif share_action == 'unshare':
            image.shared = False
        image.save()
        return redirect('display_image', pk=image.pk)
    return render(request, 'image_generator/display_image.html', {'image': image})

# เพิ่ม , แก้ไข , ลบ

def add_image(request):
    if request.method == 'POST':
        form = GeneratedImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GeneratedImageForm()
    return render(request, 'image_generator/add_image.html', {'form': form})

def edit_image(request, pk):
    image = get_object_or_404(GeneratedImage, pk=pk)
    if request.method == 'POST':
        form = GeneratedImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GeneratedImageForm(instance=image)
    return render(request, 'image_generator/edit_image.html', {'form': form, 'image': image})

def delete_image(request, pk):
    image = get_object_or_404(GeneratedImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('home')
    return render(request, 'image_generator/delete_image.html', {'image': image})

def home(request):
    images = GeneratedImage.objects.filter(shared=True).order_by('-created_at')
    return render(request, 'image_generator/home.html', {'images': images})

# About

def about(request):
    return render(request, 'image_generator/about.html')

#login และ User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'image_generator/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }

    return render(request, 'image_generator/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

# Admin views
@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'image_generator/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    return render(request, 'image_generator/manage_users.html', {'user': user})