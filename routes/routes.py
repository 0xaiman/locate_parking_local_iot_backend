from flask import request, jsonify
from services.occupyParking import occupyParkingService
from services.uploadSnapshot import upload_snapshot
from services.getParkingLocation import get_parking_location

def setup_routes(app):
    app.route('/')(home)
    app.post('/lprdata')(occupyParkingService)
    app.get('/api/parking-location/<plate_number>')(get_parking_location)

# TODO. ROUTES : use params to manage parking status
#     def setup_routes(app):
#     app.route('/')(home)
#     app.post('/api/parking-spots/<spot_id>/occupy')(occupy_parking_service)
#     app.post('/api/parking-spots/<spot_id>/vacate')(vacate_parking_service)


def home():
    return "Hello Flask!"



    
