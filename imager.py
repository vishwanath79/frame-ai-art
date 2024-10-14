import os
import datetime
from typing import Optional

from openai import OpenAI
from PIL import Image
import shutil
import requests
from config import OPENAI_API_KEY


def generate_image(prompt: str) -> Optional[Image.Image]:
    """Generates an image from a prompt using the DALL-E 3 model and saves it to a file."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.images.generate(
        model='dall-e-3',
        prompt=prompt,
        quality='hd',
        n=1
    )
    image_url = response.data[0].url

    image_response = requests.get(image_url, stream=True)
    if image_response.status_code == 200:
        file_name = '_'.join(prompt.split(' ')[:2] + [datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")]) + '.png'
        image_path = os.path.join('images', file_name)
        os.makedirs('images', exist_ok=True)
        with open(image_path, 'wb') as file:
            image_response.raw.decode_content = True  # type: ignore
            shutil.copyfileobj(image_response.raw, file)
        #return imagepath and imagename
        return file_name,image_path
    
   
    else:
        return None

