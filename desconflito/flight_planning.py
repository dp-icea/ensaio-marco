import csv

class FlightPlanning:
    
    def make_route(self):
        return self.make_volume("2024-02-12T23:21:50.52Z", "2024-02-12T23:23:50.52Z")

    def make_volume(self, time_start, time_end):
        return {
            "volume": {
                "outline_polygon": {
                    "vertices": self.make_vertices()
                },
                "altitude_lower": {
                    "value": 500,
                    "reference": "W84",
                    "units": "M"
                },
                "altitude_upper": {
                    "value": 600,
                    "reference": "W84",
                    "units": "M"
                }
            },
            "time_start": {
                "value": time_start,
                "format": "RFC3339"
            },
            "time_end": {
                "value": time_end,
                "format": "RFC3339"
            }
        }

    def make_vertices(self):
        self.make_mock_flight_data()
        maxLat = float(max(position['lat'] for position in self.drone_positions))
        maxLng = float(max(position['lon'] for position in self.drone_positions))
        minLat = float(min(position['lat'] for position in self.drone_positions))
        minLng = float(min(position['lon'] for position in self.drone_positions))

        vertices = []
        vertices.append({
            "lat": maxLat,
            "lng": minLng
        })
        vertices.append({
            "lat": maxLat,
            "lng": maxLng
        })
        vertices.append({
            "lat": minLat,
            "lng": maxLng
        })
        vertices.append({
            "lat": minLat,
            "lng": minLng
        })

        return vertices

    def make_mock_flight_data(self):
        with open('../flight_data/mock_data_1.csv') as mock_data_1:
            self.drone_positions = list(csv.DictReader(mock_data_1))