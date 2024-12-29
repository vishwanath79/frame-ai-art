"""
A script to control a Samsung TV's art mode using the SamsungTVWS library.
This module handles the TV connection, art management, and image display functionality.
"""
import logging
import re
import os
from typing import List, Tuple, Optional

from samsungtvws import SamsungTVWS
from imager import generate_image
from config import TV_IP_ADDRESS, PROMPT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SamsungArtController:
    """Controls Samsung TV Art Mode operations."""
    
    def __init__(self, ip_address: str):
        """
        Initialize the TV controller.
        
        Args:
            ip_address: IP address of the Samsung TV
        """
        self.tv = SamsungTVWS(ip_address)
        self.images_dir = 'images'
        os.makedirs(self.images_dir, exist_ok=True)

    def check_art_mode_support(self) -> bool:
        """Check if the TV supports art mode."""
        try:
            return self.tv.art().supported()
        except Exception as e:
            logger.error(f"Failed to check art mode support: {e}")
            return False

    def upload_image_to_tv(self, image_path: str) -> bool:
        """
        Upload an image to the TV and enable art mode.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Enable art mode
            self.tv.art().set_artmode(True)
            
            # Read and upload the image
            with open(image_path, 'rb') as file:
                self.tv.art().upload(file.read())
            logger.info(f"Successfully uploaded image: {image_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload image: {e}")
            return False

    def delete_art_from_tv(self, content_id: str) -> bool:
        """
        Delete art from the TV by content ID.
        
        Args:
            content_id: The content ID of the art to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.tv.art().delete(content_id)
            logger.info(f"Successfully deleted art with content_id: {content_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete art: {e}")
            return False

    def get_current_art_content_id(self) -> Optional[str]:
        """Get the content ID of the currently displayed art."""
        try:
            current_art = self.tv.art().get_current()
            pattern = r"'content_id': '(.*?)'"
            match = re.search(pattern, str(current_art), re.DOTALL)
            return match.group(1) if match else None
        except Exception as e:
            logger.error(f"Failed to get current art content ID: {e}")
            return None

    def clean_old_art(self) -> None:
        """Delete all existing custom art from the TV."""
        try:
            art_list = self.tv.art().available()
            for art in art_list:
                if art['content_id'].startswith('MY'):
                    self.delete_art_from_tv(art['content_id'])
        except Exception as e:
            logger.error(f"Failed to clean old art: {e}")

    def set_latest_art(self) -> Optional[str]:
        """
        Set the most recently uploaded art as current.
        
        Returns:
            Optional[str]: Content ID of the selected art if successful
        """
        try:
            art_list = self.tv.art().available()
            custom_art = [art for art in art_list if art['content_id'].startswith('MY')]
            if not custom_art:
                logger.warning("No custom art found")
                return None
                
            latest_art = max(custom_art, key=lambda x: x['content_id'])
            content_id = latest_art['content_id']
            self.tv.art().select_image(content_id)
            logger.info(f"Set latest art with content_id: {content_id}")
            return content_id
        except Exception as e:
            logger.error(f"Failed to set latest art: {e}")
            return None

def main():
    """Main execution function."""
    try:
        # Initialize controller
        controller = SamsungArtController(TV_IP_ADDRESS)
        
        # Verify art mode support
        if not controller.check_art_mode_support():
            logger.error("Art mode not supported on this TV")
            return

        # Generate new image
        image, image_path = generate_image(PROMPT)
        if not image or not image_path:
            logger.error("Failed to generate image")
            return

        # Clean old art and upload new
        controller.clean_old_art()
        if not controller.upload_image_to_tv(image_path):
            return

        # Set as current art
        content_id = controller.set_latest_art()
        if content_id:
            logger.info("Successfully updated TV art")
        else:
            logger.error("Failed to set new art as current")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
            

