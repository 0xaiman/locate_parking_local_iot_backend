import os
from datetime import datetime
from utils.decodeToImages import decode_base64_to_image
from utils.overlayTextOnImage import overlay_text_on_image
from utils.crop_image import crop_image

def store_image(car_data):
    print("STORE IMAGE RUNNING OK")

    try:
        # Extract relevant data from the JSON
        trigger_time = car_data.get('time', 'no_time')
        license_plate = car_data.get('License Plate', 'no_plate')
        device_name = car_data.get('device', 'unknown_device')
        coordinates = {
            'x1': car_data.get('coordinate_x1'),
            'y1': car_data.get('coordinate_y1'),
            'x2': car_data.get('coordinate_x2'),
            'y2': car_data.get('coordinate_y2'),
        }

        # Format the date and time for the folder and file names
        try:
            dt_object = datetime.strptime(trigger_time, '%Y-%m-%d %H:%M:%S')
            formatted_time = dt_object.strftime('%Y%m%d_%H%M%S')
            folder_name = dt_object.strftime('%Y%m%d')  # Use only date for folder name
        except ValueError:
            formatted_time = 'invalid_time'
            folder_name = 'invalid_date'

        # Create a dedicated 'snapshot' folder in the current directory
        snapshot_dir = os.path.join(os.getcwd(), 'snapshot')
        os.makedirs(snapshot_dir, exist_ok=True)

        # Create the folder structure (day folder and device folder) within 'snapshot'
        daily_folder_path = os.path.join(snapshot_dir, folder_name)
        device_folder_path = os.path.join(daily_folder_path, device_name)
        os.makedirs(device_folder_path, exist_ok=True)

        # Create the folder for cropped images
        cropped_folder_path = os.path.join(device_folder_path)
        os.makedirs(cropped_folder_path, exist_ok=True)

        # Format the file name using trigger time and license plate
        file_name = f"{formatted_time}_{license_plate}.jpg"
        cropped_file_path = os.path.join(cropped_folder_path, file_name)

        # Decode and save the snapshot if it exists
        snapshot = car_data.get('snapshot')

        if snapshot:
            # Decode the base64 snapshot to a temporary file for cropping
            temp_uncropped_path = os.path.join(snapshot_dir, 'temp_uncropped.jpg')
            if not decode_base64_to_image(snapshot, temp_uncropped_path):
                print("Failed to decode the snapshot.")
                return {'status': 'Error', 'message': 'Failed to decode snapshot'}, 500

            # Crop the image and get the cropped image object
            cropped_image = crop_image(temp_uncropped_path, coordinates)
            if cropped_image:
                # Save the cropped image to the cropped file path
                cropped_image.save(cropped_file_path)

                # Overlay text on the cropped image
                if not overlay_text_on_image(cropped_file_path, f"{trigger_time} \n{license_plate}"):
                    print("Failed to overlay text on the cropped image.")
                    return {'status': 'Error', 'message': 'Failed to overlay text on cropped image'}, 500
            else:
                print("Failed to crop the image.")
                return {'status': 'Error', 'message': 'Failed to crop image'}, 500
        else:
            print("No snapshot found in the request")

        return {'status': 'OK', 'message': 'Data processed successfully', 'file_path': cropped_file_path}, 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return {'status': 'Error', 'message': str(e)}, 500
