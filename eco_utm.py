import requests
import uuid
import time


class EcoUtm:

    def __init__(self) -> None:
        self.eco_user_id = "1ee10fc1-dc5a-6df4-91c7-0242ac1c0005"
        self.uas_id = "1ed0e6d9-e88e-6812-bd5f-0242ac12001c"


    def area_solicitation(self, geometry, start_time, end_time):
        self.auth_eco_utm()
        self.create_asa_id(geometry, start_time, end_time)
        self.create_solicitation(geometry, start_time, end_time)
        


    def auth_eco_utm(self):
        url = "http://kong.icea.decea.mil.br:64235/eco-utm/v1/providers/auth"
        data = { 
            "data" : {
                "provider_secret": "ZcRMOvPEbXoc0raV81veps7oqLlk5k8jDmdUk58uk5JbhfsCzZNs6bjM7Jj0g4wV",
                "provider_id": "d9b6c0d9-2c49-4cc5-8d81-06ef797649be",
                "user_id": self.eco_user_id
            }  
        }
        headers = {
            "apikey": "ZcRMOvPEbXoc0raV81veps7oqLlk5k8jDmdUk58uk5JbhfsCzZNs6bjM7Jj0g4wV",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json = data, headers=headers).json()


        self.auth_token = response["token"]
        self.pilot_id = response["pilot"]["operational_id"]

    def create_asa_id(self, geometry, start_time, end_time):
        self.asa_id = str(uuid.uuid4())
        url = f"http://kong.icea.decea.mil.br:64236/api/polygon/{self.asa_id}/{self.eco_user_id}"
        data = {
            "type": "Feature",
            "properties": {
                "poligonoId": self.asa_id,
                "perfil": "1",
                "datasHoras": "{" + f"\"date1\":\"{start_time[0:9]}\",\"date2\":\"{end_time[0:9]}\",\"hora1\":\"{start_time[11:15]}\",\"hora2\":\"{end_time[11:15]}\"" + "}",
                "elevacoes": {
                    "criarAreaMaximo": 10,
                    "criarAreaMinimo": 0,
                    "criarAreaMaximoFt": 32.8084,
                    "criarAreaMinimoFt": 0,
                    "criarAreaNome": "",
                    "criarAreaDescricao": "",
                    "alturaEditavelMetros": "10",
                    "alturaEditavelPes": 32.8084,
                    "dataInicio": f"{start_time[0:9]}",
                    "dataTermino": f"{end_time[0:9]}",
                    "horaInicio": f"{start_time[11:15]}",
                    "horaTermino": f"{end_time[11:15]}",
                    "update": []
                },
                "raio": 0,
                "altura": "10",
                "formato": "poligono",
                "contextoId": 1,
                "pontoDecolagem": {
                    "latLng": {
                        "lat": geometry["coordinates"][0][0][0],
                        "lng": geometry["coordinates"][0][0][1],
                        "valido": True
                    },
                    "unidade": "gms",
                    "elevationM": 10,
                    "elevationFt": 32.8084,
                    "valido": True
                }
            },
            "geometry": geometry
        }
        headers = {
            "authorization": f"Bearer {self.auth_token}"
        }
        response = requests.post(url, json=data, headers=headers)
        print (f"ASA ID criado: {self.asa_id}")

    def create_solicitation(self, geometry, start_time, end_time):
        data = {
            "data": {
                "type": "/pilots/flights",
                "attributes": {
                    "airplane_id": f"{self.uas_id}",
                    "operation": {
                        "aircrafts": [
                        {
                                "id": 4,
                                "uuid": f"{self.uas_id}"
                        }
                        ],
                        "flight": {
                            "pilots": [f"{self.pilot_id}"],
                            "date": {
                                "start_day": f"{start_time[0:10]}",
                                "start_hour": f"{start_time[11:16]}",
                                "finish_day": f"{end_time[0:10]}",
                                "finish_hour": f"{end_time[11:16]}"
                            },
                            "type": "VLOS",
                            "observations": "teste",
                            "communication": {
                                "id": "1",
                                "ats_call_type": "vhf-fm",
                                "rpa_call_type": "vhf-am",
                                "rps": [
                                    {
                                        "name": "1",
                                        "lat": "1",
                                        "lng": "1",
                                        "contact_info": "1",
                                        "radius": 100
                                    }
                                ]
                            },
                            "sarpas_code": f"{self.pilot_id}",
                            "area": {
                                "asa_id": "283797ce-73e9-4395-adcf-6c6119b3f20f",
                                "takeoff_point": [geometry["coordinates"][0][0][0],geometry["coordinates"][0][0][1]],
                                "landing_point": [geometry["coordinates"][0][0][0],geometry["coordinates"][0][0][1]],
                                "required_route": {
                                    "geojson": {
                                                                    "type": "Feature",
                                                                    "properties": {},
                                                                    "geometry": geometry
                                                                }
                                    },
                                    "flight_type": "height",
                                    "flight_distance": 100
                                },
                                "documents": []
                            },
                            "basic_information": {
                                "name": "teste 2",
                                "type": "101",
                                "agree_terms": 1
                            }
                        }
                    }
                }
            }
        
        url = "http://kong.icea.decea.mil.br:64235/eco-utm/v1/pilots/flights"
        header = {
            "authorization": f"Bearer {self.auth_token}"
        }

        response = requests.post(url, json=data, headers=header).json()

        self.eco_protocol = response["data"]["attributes"]["protocol"]
        self.flight_id = response["data"]["id"]
        print (self.eco_protocol)
        
    def approve_area(self):
        self.bypass_categoryze()
        self.bypass_analyze()
        
        #Aguarda filas do ASA e ECO-UTM
        time.sleep(10)
        self.bypass_result_analysis()
        time.sleep(5)
        self.bypass_result_analysis()

        self.check_status()

    def bypass_categoryze(self):
        url = f"http://kong.icea.decea.mil.br:64235/eco-utm/v1/bypass/categorize/{self.eco_protocol}"
        header = { "authorization": f"Bearer {self.auth_token}"}
        response = requests.get(url, headers=header)
        print (response.text)
    
    def bypass_analyze(self):
        url = f"http://kong.icea.decea.mil.br:64235/eco-utm/v1/bypass/analyze/{self.eco_protocol}"
        header = { "authorization": f"Bearer {self.auth_token}"}
        response = requests.get(url, headers=header)
        print (response.text)

    def bypass_result_analysis(self):
        url = f"http://kong.icea.decea.mil.br:64236/api/polygon/{self.eco_protocol}/result"
        header = { "authorization": f"Bearer {self.auth_token}"}
        response = requests.get(url, headers=header)

    def check_status(self):
        url = f"http://kong.icea.decea.mil.br:64235/eco-utm/v1/flight-status?filtro={self.eco_protocol}"
        header = { "authorization": f"Bearer {self.auth_token}"}
        response = requests.get(url, headers=header).json()
        print (response["data"][0]["status"]["name"])
