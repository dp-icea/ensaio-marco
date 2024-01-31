from conflict_manager import ConflictManager
from flight_planning import FlightPlanning
from scd import Scd
from rid import Rid


class Dss:
    def __init__(self) -> None:
        self.flight_planning = FlightPlanning()
        self.conflict_manager = ConflictManager()
        self.scd = Scd()
        self.rid = Rid()


        