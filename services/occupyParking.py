from flask import request, jsonify
from config.db_connect import create_connection
from utils.storeImage import store_image

def occupyParkingService():
    #  1- Gets Json Data
    car_data = request.get_json()
    if not car_data:
        return jsonify({'status':'Error','message': 'No JSON data received'}), 400
     
    

    # 2-  EXtracts Json Data
    bay_name = car_data.get('space_name')
    device_name = car_data.get('device')
    time = car_data.get('time')
    occupancy_bay = car_data.get('occupancy')
    license_plate = car_data.get('License Plate')
    vehicle_type = car_data.get('Vehicle Type')
    vehicle_color = car_data.get('Vehicle Color')
    vehicle_brand = car_data.get('Vehicle Brand')

    # 3 - Handles Bay occupancy
    if occupancy_bay is None:
        return jsonify({'status': 'Error', 'message': 'Occupancy value not found in JSON'}), 400

    if occupancy_bay == 1:
        print(" Vehicle detected (occupancy=1). Image will be saved.")
        # img_path = "dummypath"

    #TODO : ENSURE IMAGE CROPPED IS SAVED IN SNAPSHOT
    #4 - handle image storage

        snapshot, status = store_image(car_data)

        if status == 200:
            img_path = snapshot.get('file_path')
            print(f'file saved at {img_path}')
        else:
            print("save image failed")
    elif occupancy_bay ==0 :
        print("No Vehicle detected (occupancy=0). Image will not be saved.")
    
    # 5 - Try COnnect to Database
    connection = create_connection()

    if not connection:
        return jsonify({"status": "Error", "message": "Database connection failed"}), 500

    occupy_query = """

    INSERT INTO parking_bay (bay_name, time, device_name, occupancy_bay, license_plate, vehicle_type, vehicle_color, vehicle_brand , img_path)
    VALUES  (%s, %s, %s, %s, %s, %s, %s,%s,%s);
    """
    # 6 - Write into Database
    try: 
        cursor = connection.cursor()
        cursor.execute(occupy_query, (
            bay_name, 
            time, 
            device_name, 
            occupancy_bay, 
            license_plate if occupancy_bay == 1 else None,  # Only insert license plate if occupied
            vehicle_type if occupancy_bay == 1 else None,    # Only insert vehicle type if occupied
            vehicle_color if occupancy_bay == 1 else None,   # Only insert vehicle color if occupied
            vehicle_brand if occupancy_bay == 1 else None,   # Only insert vehicle brand if occupied
            img_path if occupancy_bay == 1 else None
            ))
        connection.commit()
        cursor.close()

        return jsonify({"message": "Data added succefully", "data": car_data}), 201
    except Exception as error:
        return jsonify({"message": f"Failed to insert data: {str(error)}"}), 500
    finally:
        connection.close()


