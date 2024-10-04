from PIL import Image, ImageDraw, ImageFont
import os

def crop_image(image_path, coordinates):
    try:
        with Image.open(image_path) as img:
            cropped_img = img.crop((coordinates['x1'], coordinates['y1'], coordinates['x2'], coordinates['y2']))
            return cropped_img  # Return cropped image instead of saving it directly
    except Exception as e:
        print(f"Error cropping image: {e}")
        return None