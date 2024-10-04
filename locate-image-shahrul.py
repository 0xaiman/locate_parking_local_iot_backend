import os
import shutil
import tkinter as tk
from tkinter import filedialog
from flask import Flask, request, jsonify, Response
import base64
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import json  # Import json module to handle JSON file creation

# Initialize the Flask application
app = Flask(__name__)

# Global variables for font path and save directory
FONT_PATH = None
ROOT_SAVE_DIR = None

# Function to choose a directory for saving files
def choose_save_directory():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select Directory to Save Files")

# Function to choose a font file
def choose_font_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Select Font File", filetypes=[("Font files", "*.ttf *.otf")])

# Function to decode base64 string into an image
def decode_base64_to_image(base64_string, output_path):
    try:
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(base64_string))
        return True
    except Exception as e:
        print(f"Error decoding image: {e}")
        return False

# Function to overlay text on an image
def overlay_text_on_image(image_path, text, position=(1, 997), font_size=45, color=(255, 255, 255), background_color=(0, 0, 0)):
    try:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(FONT_PATH, font_size) if FONT_PATH else ImageFont.load_default()
            text_bbox = draw.textbbox(position, text, font=font)
            draw.rectangle(text_bbox, fill=background_color)
            draw.text(position, text, font=font, fill=color)
            img.save(image_path)
        return True
    except Exception as e:
        print(f"Error overlaying text: {e}")
        return False

# Function to crop an image based on provided coordinates
def crop_image(image_path, coordinates):
    try:
        with Image.open(image_path) as img:
            cropped_img = img.crop((coordinates['x1'], coordinates['y1'], coordinates['x2'], coordinates['y2']))
            return cropped_img  # Return cropped image instead of saving it directly
    except Exception as e:
        print(f"Error cropping image: {e}")
        return None

# Function to encode an image to base64
def encode_image_to_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

# Authentication check function
def check_auth(username, password):
    return username == 'bigtac' and password == 'bigtac123'

# Authentication handler
def authenticate():
    return Response('Authentication required.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Decorator for routes requiring authentication
def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Define the index route
@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Image Processing API"

# Define a route for uploading snapshots with authentication
@app.route('/lprdata', methods=['POST'])
@requires_auth
def upload_snapshot():
    try:
        car_data = request.json
        if not car_data:
            return jsonify({'status': 'Error', 'message': 'No JSON data received'}), 400

        # Extract relevant data from the JSON
        trigger_time = car_data.get('time', 'no_time')
        license_plate = car_data.get('License Plate', 'no_plate')
        device_name = car_data.get('device', 'unknown_device')
        snapshot = car_data.get('snapshot')
        occupancy = car_data.get('occupancy', None)  # Extract occupancy
        coordinates = {
            'x1': car_data.get('coordinate_x1'),
            'y1': car_data.get('coordinate_y1'),
            'x2': car_data.get('coordinate_x2'),
            'y2': car_data.get('coordinate_y2'),
        }  # Extract coordinates using the new keys

        if occupancy is None:
            return jsonify({'status': 'Error', 'message': 'Occupancy field is missing'}), 400
        
        # Check occupancy; if it's 0, generate JSON file but do not process further
        if occupancy == 0:
            # Parse date and time for generating file names
            try:
                dt_object = datetime.strptime(trigger_time, '%Y-%m-%d %H:%M:%S')
                formatted_time = dt_object.strftime('%Y%m%d_%H%M%S')
                folder_name = dt_object.strftime('%Y%m%d')
            except ValueError:
                formatted_time = 'invalid_time'
                folder_name = 'invalid_date'

            # Construct file paths
            daily_folder_path = os.path.join(ROOT_SAVE_DIR, folder_name)
            device_folder_path = os.path.join(daily_folder_path, device_name)
            
            # Create directories if they don't exist
            os.makedirs(device_folder_path, exist_ok=True)
            
            # Construct JSON file path
            json_file_path = os.path.join(device_folder_path, f"{formatted_time}_{license_plate}.json")
            
            # Create JSON data
            json_data = {
                "time": trigger_time,
                "License Plate": license_plate,
                "device": device_name,
                "occupancy": occupancy,
                "coordinates": coordinates,
            }
            
            # Save JSON file
            try:
                with open(json_file_path, "w") as json_file:
                    json.dump(json_data, json_file, indent=4)
            except Exception as e:
                print(f"Error saving JSON file: {e}")
                return jsonify({'status': 'Error', 'message': 'Failed to save JSON file'}), 500
            
            return jsonify({'status': 'OK', 'message': 'No occupancy detected; JSON file generated', 'json_file': json_file_path}), 200

        if not snapshot:
            return jsonify({'status': 'Error', 'message': 'No snapshot provided'}), 400

        # Parse date and time
        try:
            dt_object = datetime.strptime(trigger_time, '%Y-%m-%d %H:%M:%S')
            formatted_time = dt_object.strftime('%Y%m%d_%H%M%S')
            folder_name = dt_object.strftime('%Y%m%d')
        except ValueError:
            formatted_time = 'invalid_time'
            folder_name = 'invalid_date'

        # Construct file paths
        file_name = f"{formatted_time}_{license_plate}.jpg"
        daily_folder_path = os.path.join(ROOT_SAVE_DIR, folder_name)
        device_folder_path = os.path.join(daily_folder_path, device_name)

        # Create directories if they don't exist
        os.makedirs(device_folder_path, exist_ok=True)
        
        # Paths for original and cropped images
        original_file_path = os.path.join(device_folder_path, file_name)
        cropped_file_name = f"{formatted_time}_{license_plate}_cropped.jpg"
        cropped_file_path = os.path.join(device_folder_path, cropped_file_name)

        # Decode base64 image
        if not decode_base64_to_image(snapshot, original_file_path):
            return jsonify({'status': 'Error', 'message': 'Failed to decode snapshot'}), 500

        # Overlay text onto the original image
        overlay_text = f"{trigger_time}\n{license_plate}"
        if not overlay_text_on_image(original_file_path, overlay_text):
            return jsonify({'status': 'Error', 'message': 'Failed to overlay text on original image'}), 500

        # If coordinates are provided, crop the image
        cropped_image = None
        if all(coord is not None for coord in coordinates.values()):  # Ensure all coordinates are present
            cropped_image = crop_image(original_file_path, coordinates)
            if cropped_image is None:
                return jsonify({'status': 'Error', 'message': 'Failed to crop the image based on coordinates'}), 500
            
            # Save the cropped image and overlay text
            cropped_image.save(cropped_file_path)  # Save cropped image
            
            if not overlay_text_on_image(cropped_file_path, overlay_text):
                return jsonify({'status': 'Error', 'message': 'Failed to overlay text on cropped image'}), 500

        return jsonify({'status': 'OK', 'message': 'Data processed successfully', 'original_image': original_file_path, 'cropped_image': cropped_file_path}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'status': 'Error', 'message': str(e)}), 500

# Main execution block
if __name__ == '__main__':
    FONT_PATH = choose_font_file()  # Select the font file
    ROOT_SAVE_DIR = choose_save_directory()  # Select the save directory
    app.run(host='0.0.0.0', port=5000, debug=True)