import datetime


Heat_Pump_start1 = datetime.datetime(hour=4)
Heat_Pump_end1 = datetime.datetime(hour=8)
Heat_Pump_start2 = datetime.datetime(hour=16)
Heat_Pump_end2 = datetime.datetime(hour=23)


# WashingMachine_start = datetime.datetime(hour=23,minute=54)
# WashingMachine_end = datetime.datetime(hour=5,minute=54)

DomesticHotWaterControllerBoiler_start1 = datetime.datetime(hour=5)
DomesticHotWaterControllerBoiler_end1 = datetime.datetime(hour=9)
DomesticHotWaterControllerBoiler_start2 = datetime.datetime(hour=16)
DomesticHotWaterControllerBoiler_end2 = datetime.datetime(hour=21)

def TurnDishwasherOn():
    print("Dishwasher is on")
def TurnHeatPumpOn():
    print("Heat Pump is on")
def TurnWashingMachineOn():
    print("Washing Machine is on")
def TurnDomesticHotWaterControllerBoilerOn():
    print("Domestic Hot Water Controller Boiler is on")
usage=1;
while(1):

    now = datetime.datetime.now()

    if now > Heat_Pump_start1 or now < Heat_Pump_end1:
        TurnHeatPumpOn()
        if usage > 1:
            pass

    if now > DomesticHotWaterControllerBoiler_start1 or now < DomesticHotWaterControllerBoiler_end1:
        TurnDomesticHotWaterControllerBoilerOn()
        if usage > 1:
            pass
    if usage > 1:
        pass
