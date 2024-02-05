import requests
import uuid

class Scd:
    dss_host = "http://localhost:8082"

    def __init__(self) -> None:
        self.auth()

    def auth(self):
        url = "http://localhost:8085/token?grant_type=client_credentials&intended_audience=localhost&issuer=localhost&scope={0}"
        self.strategic_coordination = requests.get(url.format("utm.strategic_coordination")).json()["access_token"]

    def check_strategic_conflicts(self, volume):
        url = self.dss_host + "/dss/v1/operational_intent_references/query"
        body = {
            "area_of_interest": volume
        }
        header = {"authorization": f"Bearer {self.strategic_coordination}"}
        response = requests.post(url, headers=header, json=body).json()

        if (len(response['operational_intent_references']) > 0):
            raise Exception("Interseção com outra Intenção")
        else:
            print("Sem intenções para o volume")
        
    def put_operational_intent(self, volume):
        id = str(uuid.uuid4())
        url = self.dss_host + f"/dss/v1/operational_intent_references/{id}"

        body = {
            "flight_type": "VLOS",
            "extents": [volume],
            "key": [],
            "state": "Accepted",
            "uss_base_url": "my.url.com",
            "new_subscription": {
                "uss_base_url": "my.url.com",
                "notify_for_constraint": False
            }
        }

        header = {"authorization": f"Bearer {self.strategic_coordination}"}

        response = requests.put(url, headers=header, json=body).json()

        print(f"OIR criada com id: {id}")
