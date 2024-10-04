from PIL import Image, ImageDraw, ImageFont
import os

def overlay_text_on_image(file_path, text):
    """
    Overlay date, time, and license plate on the left-bottom corner of the image using a specific font.
    """
    try:
        # Open an image file
        with Image.open(file_path) as img:
            draw = ImageDraw.Draw(img)

            # Define the font size and relative path
            font_size = 45
            font_path = os.path.join(os.path.dirname(__file__), 'utils', 'VCR_OSD_MONO.ttf')  # Relative path to the font

            print(f"Loading font from: {font_path}")  # Debug print

            # Check if the font file exists
            if not os.path.isfile(font_path):
                print(f"Font file does not exist at: {font_path}")
                font = ImageFont.load_default()  # Use default font if not found
            else:
                font = ImageFont.truetype(font_path, font_size)  # Load the specified font

            text_color = (255, 255, 255)  # White text
            background_color = (0, 0, 0)   # Black background for text

            # Define the position for the text in the left-bottom corner
            text_position = (10, img.height - font_size - 10)  # 10 pixels from left and bottom

            # Get bounding box of the text to draw background rectangle
            text_bbox = draw.textbbox(text_position, text, font=font)

            # Draw the black rectangle behind the text for highlighting
            draw.rectangle([text_position, (text_bbox[2], text_bbox[3])], fill=background_color)

            # Overlay the text
            draw.text(text_position, text, font=font, fill=text_color)

            # Save the edited image
            img.save(file_path)
            print(f"Image with overlay saved to {file_path}")

            return True

    except Exception as e:
        print(f"Error overlaying text on image: {e}")
        return False  # Changed 'false' to 'False'

# Example usage
# overlay_text_on_image("path/to/your/image.jpg", "ABC 1234")
