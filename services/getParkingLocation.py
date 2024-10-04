from flask import request, jsonify
from config.db_connect import create_connection


def get_parking_location(plate_number):
    print("getParkingLocation OK")
    print(f"GET request for plate number {plate_number}")

    #  find plate njumber in record.
    # take the latest

    connection = create_connection()

    if not connection:
        return jsonify({"status": "Error", "message": "Database connection failed"}), 500

    get_parking_query = '''
        SELECT bay_name 
        FROM parking_bay
        WHERE license_plate = %s
        ORDER BY time
        DESC
        LIMIT 1;
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(get_parking_query, (plate_number,))
        result = cursor.fetchone()

        if result:
            bay_name = result[0]
            return jsonify({"status": "Success", "bay_name": bay_name}), 200
        else:
            return jsonify({"status": "Error", "message": "No record found for this plate number"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "Error", "message": "An error occurred while fetching the data"}), 500

    finally:
        cursor.close()
        connection.close()



