from dss import Dss


def main():
    dss = Dss()

    try:
        volume = dss.flight_planning.make_volume("2024-02-13T12:21:50.52Z", "2024-02-13T13:22:50.52Z")
        dss.conflict_manager.check_restrictions(volume)
        dss.scd.check_strategic_conflicts(volume)

        dss.scd.put_operational_intent(volume)
        
        dss.rid.create_isa(volume)
    except Exception as ex:
        print(f"Erro na criação: {ex}")



if __name__ == "__main__":
    main()