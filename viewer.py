from flask import Flask, json, jsonify, request
import random
import datetime
import requests
from flask_cors import CORS, cross_origin


api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/backend/flights', methods=['GET'])
@cross_origin()
def get_flights():
    try: 
        token = auth()

        url = "http://localhost:8081/mock/ridsp/v2/uss/flights?view=-23.61087159001373,-46.624287901311924,-23.595475890605172,-46.564833096444424"
        header = {"authorization": f"Bearer {token}"}
        response = requests.get(url, headers=header).json()
        lat = response["flights"][0]["current_state"]["position"]["lat"]
        lng = response["flights"][0]["current_state"]["position"]["lng"]
        return json.dumps({"lat": lat, "lng": lng})
    except:
        return json.dumps({"lat": -23.71087159001373, "lng": -46.564933096444434})

def auth():
    url = "http://localhost:8085/token?grant_type=client_credentials&intended_audience=localhost&issuer=localhost&scope={0}"
    return requests.get(url.format("rid.display_provider")).json()["access_token"]

if __name__ == '__main__':
    api.run()