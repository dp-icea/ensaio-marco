import requests
import uuid
from inject_mock import Telemetry

class Dss:

    def __init__(self) -> None:
        self.telemetry = Telemetry()
    
    def auth(self):
        url = "http://localhost:8085/token?grant_type=client_credentials&intended_audience=localhost&issuer=localhost&scope={0}"
        self.auth_read_isa = requests.get(url.format("identification_service_areas")).json()["access_token"]
        self.auth_inject_data = requests.get(url.format("rid.inject_test_data")).json()["access_token"]

    def inject_data(self, uas_id, pilot_id, eco_id):
        self.auth()
        injection_id = str(uuid.uuid4())
        url = f"http://localhost:8081/ridsp/injection/tests/{injection_id}"
        header = {"authorization": f"Bearer {self.auth_inject_data}"}
        data = self.telemetry.make_payload(uas_id, pilot_id, eco_id)

        response = requests.put(url, headers=header, json=data).json()
        id = response["injected_flights"][0]["details_responses"][0]["details"]["id"]
        print (f"ISA Criada: {id}")

    def get_area(self):
        url = "http://localhost:8081/ridsp/injection/tests/area"
        data = self.telemetry.make_payload("1ed0e6d9-e88e-6812-bd5f-0242ac12001c", "QGRK", "1eea4bbb-f46a-6860-92d6-0242ac180007")
        response = requests.post(url, json=data).json()
        self.start_time = response["start_time"]
        self.end_time = response["end_time"]
        self.vertices = response["vertices"]

    def make_eco_geometry(self):
        result_list = []
        for latlong in self.vertices:
            lat = latlong["lat"]
            long = latlong["lng"]
            result_list.append([lat,long])

        #Fecha o poligono, ultimo vertice = primeiro vertice
        result_list.append([self.vertices[0]["lat"], self.vertices[0]["lng"]])

        self.geometry = {
            "type": "Polygon",
            "coordinates": [result_list]
        }
    

    