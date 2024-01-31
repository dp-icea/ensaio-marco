
import requests
from eco_utm import EcoUtm
from dss import Dss
import time


def main():
    # EcoUtm é a classe que interage com o ECO-UTM.
    ecoutm = EcoUtm()
    ecoutm.auth_eco_utm()

    # Dss é a classe responsável por interagir com o mock_dss. 
    # Cada provedor deve implementar a sua solução
    dss = Dss()
    
    mock_geometry_data = dss.make_eco_geometry(ecoutm.uas_id, ecoutm.pilot_id, ecoutm.eco_user_id)
    print(mock_geometry_data)
    return
    mock_start_time = dss.get_start_time()
    mock_end_time = dss.get_end_time()

    # Cada provedor deve requisitar eo ECO-UTM uma área, antes de prover dados de tracking para ela
    ecoutm.area_solicitation(mock_geometry_data, mock_start_time, mock_end_time)
    time.sleep(10)
    ecoutm.approve_area()

    # Cria ISA utilizando o mock_rid_provider
    dss.inject_data(ecoutm.uas_id, ecoutm.pilot_id, ecoutm.flight_id)

if __name__ == "__main__":
    main()