from diffusers import StableDiffusionPipeline , DiffusionPipeline
import time

t = 0
for i in range(10):
    x = time.time()
    pipe = DiffusionPipeline.from_pretrained("Ojimi/anime-kawai-diffusion", safety_checker=None)
    pipe.enable_sequential_cpu_offload()
    pipe.enable_attention_slicing("max")

    prompt = "Closeup face portrait of a girl wearing crown of flowers, smooth soft skin, big dreamy eyes, beautiful intricate colored hair, symmetrical, anime wide eyes, soft lighting, detailed face, by makoto shinkai, stanley artgerm lau, wlop, rossdraws, concept art, digital painting, looking into camera"
    image = pipe(prompt,negative_prompt="lowres , bad antomy").images[0]
    v = time.time()
    t += v-x

print(t/10)