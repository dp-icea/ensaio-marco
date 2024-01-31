
import csv
import datetime
import json
import uuid

class Telemetry:
    drone_positions = []
    time_offset_seconds = 90
    seconds_between_telemetries = 4

    def __init__(self):
        
        with open('flight_data/mock_data_1.csv') as mock_data_1:
            self.drone_positions = list(csv.DictReader(mock_data_1))

    def make_single_position(self, count: int) -> dict:
        current_position = self.drone_positions[count]
        timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds= self.time_offset_seconds + (self.seconds_between_telemetries*count))
        return {
          "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
          "timestamp_accuracy": 0,
          "operational_status": "Undeclared",
          "position": {
            "lat": current_position["lat"],
            "lng": current_position["lon"],
            "alt": 900,
            "accuracy_h": "HAUnknown",
            "accuracy_v": "VAUnknown",
            "extrapolated": True,
            "pressure_altitude": 0
          },
          "track": 360,
          "speed": 1,
          "speed_accuracy": "SAUnknown",
          "vertical_speed": 0,
          "height": {
            "distance": 0,
            "reference": "TakeoffLocation"
          },
        }
    
    def make_telemetry_payload(self):
        positions = []
        for index in range(len(self.drone_positions)):
            positions.append(self.make_single_position(index))
        return positions
    
    def make_flight_payload(self, uas_id, pilot_id, eco_id):
        timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds= self.time_offset_seconds)
        return {
            "injection_id": str(uuid.uuid4()),
            "telemetry": self.make_telemetry_payload(),
            "details_responses": [
                {
                    "effective_after": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "details": {
                        "id": f"{uas_id}.{eco_id}",
                        "operator_id": f"{pilot_id}",
                        "operator_location": {
                            "lng": -118.456,
                            "lat": 34.123
                        },
                        "operation_description": "Voo de drone mockado para ensaio",
                        "auth_data": {
                            "format": 0,
                            "data": ""
                        },
                        "uas_id": {
                            "utm_id": f"{uas_id}"
                        },
                        "operator_altitude": {
                            "altitude": 1321.2,
                            "altitude_type": "Takeoff"
                        },
                        "eu_classification": {
                            "category": "EUCategoryUndefined",
                            "class": "EUClassUndefined"
                        }
                    }
                }
            ]
        }
    
    def make_payload(self, uas_id, pilot_id, eco_id):
        return {
            "requested_flights": [self.make_flight_payload(uas_id, pilot_id, eco_id)],
            "isa_id": eco_id
        }
