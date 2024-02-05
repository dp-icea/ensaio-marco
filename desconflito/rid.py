from http import HTTPStatus
import requests
import uuid

class Rid:

    dss_host = "http://localhost:8082"

    def __init__(self) -> None:
        self.auth()

    def auth(self):
        url = "http://localhost:8085/token?grant_type=client_credentials&intended_audience=localhost&issuer=localhost&scope={0}"
        self.service_provider = requests.get(url.format("rid.service_provider")).json()["access_token"]

    def create_isa(self, volume):
        id = str(uuid.uuid4())
        url = self.dss_host + f"/rid/v2/dss/identification_service_areas/{id}"
        body = {
            "extents": volume,
            "uss_base_url": "my.uss.com"
        }

        header = {"authorization": f"Bearer {self.service_provider}"}

        response = requests.put(url, headers=header, json=body)

        if (response.status_code == HTTPStatus.OK):
            print(f"ISA criada com id {id}")
        else:
            raise Exception("Falha na criação da ISA")

