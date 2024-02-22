'''from diffusers import UNet2DConditionModel, AutoPipelineForText2Image
import torch

model_id = 'stabilityai/stable-diffusion-2-1-base'

# Initialize the UNet model with the appropriate parameters
unet = UNet2DConditionModel.from_pretrained(
    model_id,
    subfolder="unet",
    revision="fp16",  # Ensure you're using the fp16 revision if available
    torch_dtype=torch.float16,
    low_cpu_mem_usage=False,
    ignore_mismatched_sizes=True
).to("cuda")

# Initialize the pipeline with the UNet model
pipeline = AutoPipelineForText2Image(unet=unet)

# Load LoRA weights
pipeline.load_lora_weights(
    'artificialguybr/stickers-redmond-2-1-version-stickers-lora-for-freedom-redmond-sd-2-1',
    weight_name="StickersRedmond21V-FreedomRedmond-Sticker-Stickers.safetensors"
)

# Generate an image
prompt = 'A cute astronaut wearing sunglasses,sticker,stickers'
image = pipeline(prompt).images[0]

# Save the image
file_name = 'imgtest/testingimg.png'
image.save(file_name)'''

from diffusers import StableDiffusionPipeline
#stabilityai/stable-diffusion-2-1-base
#stabilityai/stable-diffusion-2

model_id = 'stabilityai/stable-diffusion-2'

media = StableDiffusionPipeline.from_pretrained(model_id,safety_checker=None)
media.enable_sequential_cpu_offload()
media.enable_attention_slicing("max")
prompt = input("")
image = media(prompt).images[0]

#file_name = f'static/images/bg_image1.png'
file_name = f'imgtest/testingimg.png'
image.save(file_name)