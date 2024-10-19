"""
A script to control a Samsung TV's art mode using the SamsungTVWS library.
"""
import logging
import re
from imager import generate_image
from samsungtvws import SamsungTVWS
from config import PPX, PROMPT
from typing import List, Tuple, Optional
from news import get_prompt
import os

# Set the TV IP address
TV_IP_ADDRESS = '192.168.50.251'

# Connect to the TV
tv = SamsungTVWS(TV_IP_ADDRESS)


def upload_image_to_tv(image_name: str) -> None:
    """
    Upload the image to the TV
    """
    # Switch art mode on or off
    tv.art().set_artmode(True)
    # upload the image from the images folder
    os.makedirs('images', exist_ok=True)
    with open(image_name, 'rb') as file:
        data = file.read()

        # Show the image
        tv.art().upload(data)


def delete_art_from_tv(content_id: str) -> None:
    """
    Delete the image from the TV
    """
    tv.art().delete(content_id)


def get_current_art_content_id() -> Optional[str]:
    """
    Get the current art info
    """
    current_art = tv.art().get_current()

    # Extract the content ID from the current art info
    pattern = r"'content_id': '(.*?)'"
    match = re.search(pattern, str(current_art), re.DOTALL)

    if match:
        return match.group(1)
    else:
        return None


if __name__ == '__main__':
    # Check if art mode is supported
    info = tv.art().supported()
    print(f"ART mode supported: {info}")

    # Generate an image using the DALL-E 3 model and save it to a file
    
    image, image_name = generate_image(PROMPT)
    print(image_name)

    # List available art
    art_list = tv.art().available()
    print("AVAILABLE ART:")
  
    for art in art_list:
        if art['content_id'].startswith('MY'):
        #and art['content_id'] != get_current_art_content_id():
            print("My Art currently to be deleted: ", art)

            delete_art_from_tv(art['content_id'].startswith('MY'))
    
    print("Uploading new art...")
    upload_image_to_tv(image_name)
    #set the first image that passes the test as the  current art
    
    latest_art = max((art for art in art_list if art['content_id'].startswith('MY')), key=lambda x: x['content_id'])
    print("LATEST ART: ", latest_art)
    content_id = latest_art['content_id']
    print(content_id)
    #tv.art().select_image(content_id)
            

