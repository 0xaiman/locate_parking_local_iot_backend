from flask import request, jsonify


def upload_snapshot():
    print("upload snapshot is running")

    car_data = {
    "event": "Parking Detection",
    "device": "MPC_1",
    "time": "2024-09-30 12:43:24",
    "report_type": "trigger",
    "channel": 1,
    "space_name": "Name_3",
    "occupancy": 1,
    "duration": 0,
    "License Plate": "W7155L",
    "Plate Color": "Black",
    "Vehicle Type": "Car",
    "Vehicle Color": "Gray",
    "Vehicle Brand": "-"
    }

    if not car_data:
        return jsonify({'status':'Error','message': 'No JSON data received'}), 400
    
    print("JSON received OK")

    try:
        trigger_time = car_data.get('time', 'no_time')
        license_plate = car_data.get('License Plate', 'no_plate')
        device_name = car_data.get('device', 'unknown_device')
        occupancy_bay = car_data.get('occupancy', None)

        if occupancy_bay == 0:
            print("No Vehicle detected (occupancy=0). Image will not be saved.")
            return jsonify({'status': 'OK', 'message': 'No vehicle detected. Image not saved.'}), 200
            #  TODO : Handle occupancy = 0 case.
        elif occupancy_bay is None:
            return jsonify({'status': 'Error', 'message': 'Occupancy value not found in JSON'}), 400
        
        print('Data processed successfully')
        return jsonify({'status': 'OK', 'message': 'Data processed successfully'}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'status': 'Error', 'message': str(e)}), 500


    # return jsonify({"message": "Snapshot uploaded successfully"}), 200


