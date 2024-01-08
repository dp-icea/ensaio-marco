
import requests
from eco_utm import EcoUtm
from dss import Dss
import time


def main():
    dss = Dss()
    dss.get_area()
    dss.make_eco_geometry()
    ecoutm = EcoUtm()
    ecoutm.area_solicitation(dss.geometry, dss.start_time, dss.end_time)
    time.sleep(10)
    ecoutm.approve_area()
    dss.inject_data(ecoutm.uas_id, ecoutm.pilot_id, ecoutm.flight_id)

if __name__ == "__main__":
    main()