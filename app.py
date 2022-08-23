import torch
from torch import autocast
import requests
from diffusers import StableDiffusionPipeline

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"

def get_auth_token():
    """ Banana doesn't have good secrets management... """
    token = requests.get('https://gal.xeb.ai/secrets/hftoken.txt')
    return token.content

def init():
    global model
    
    token = get_auth_token()
    
    def unsafe(images, clip_input):
        """ Don't judge me, future"""
        return images, False

    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16", torch_dtype=torch.float16, use_auth_token=token)  
    model.safety_checker = unsafe
    model = model.to("cuda")

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model

    # Parse out your arguments
    prompt = model_inputs.get('prompt', None)
    if prompt == None:
        return {'message': "No prompt provided"}
    
    # Run the model
    result = {
        "image64": None
    }

    with autocast("cuda"):
        image = model(prompt)["sample"][0]  # PIL image
        path = "image.png"
        image.save(path)
        return path