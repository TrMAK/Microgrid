import sqlite3
import matplotlib.pyplot as plt
import datetime
conn = sqlite3.connect('rawdata.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM DomesticHotWaterControllerBoilerHouse5Day1")

DomesticHotWaterControllerBoilerHouse5Day1 = []

for row in cursor.fetchall():
    DomesticHotWaterControllerBoilerHouse5Day1.append(row[2])

cursor.execute("SELECT * FROM HeatPumpUsageHouse5Day1")

HeatPumpUsageHouse5Day1 = []

for row in cursor.fetchall():
    HeatPumpUsageHouse5Day1.append(row[2])

cursor.execute("SELECT * FROM PVHouse5Day1")

PVHouse5Day1 = []

for row in cursor.fetchall():
    PVHouse5Day1.append(row[1])

cursor.execute("SELECT * FROM WashingMachineUsageHouse5Day1")

WashingMachineUsageHouse5Day1 = []

for row in cursor.fetchall():
    WashingMachineUsageHouse5Day1.append(row[2])

conn.close()

LOAD = 0.0
WashingMachineCount = 0
HeatPumpUsageCount = 0
DomesticHotWaterControllerBoilerCount = 0
DomesticHotWaterControllerBoilerState = True
WashingMachineState = True
HeatPumpState = True
# clock=datetime.datetime(year=2025,month=1,day=1,hour=0,minute=0,second=0)
LOADLIMIT=False
load_values = []

for x in range(1440):
    LOAD = 0.0
    if(LOADLIMIT):
        if DomesticHotWaterControllerBoilerState:
            DomesticHotWaterControllerBoilerState = False
        elif WashingMachineState:
            WashingMachineState = False
        elif HeatPumpState:
            HeatPumpState = False
    else:
        if not DomesticHotWaterControllerBoilerState:
            DomesticHotWaterControllerBoilerState = True
        elif not WashingMachineState:
            WashingMachineState = True
        elif not HeatPumpState:
            HeatPumpState = True
    # if(DomesticHotWaterControllerBoilerState and DomesticHotWaterControllerBoilerCount < 36):
    #     LOAD = LOAD + DomesticHotWaterControllerBoilerHouse5Day1[DomesticHotWaterControllerBoilerCount]
    #     DomesticHotWaterControllerBoilerCount+=1
    if (WashingMachineState and WashingMachineCount < 72):
        LOAD = LOAD + WashingMachineUsageHouse5Day1[WashingMachineCount]
        WashingMachineCount += 1
    if (HeatPumpState and HeatPumpUsageCount < 1402):
        LOAD = LOAD + HeatPumpUsageHouse5Day1[HeatPumpUsageCount]
        HeatPumpUsageCount += 1
    LOAD = LOAD - PVHouse5Day1[x]
    if(LOAD>1500):
        LOADLIMIT=True
    else:
        LOADLIMIT=False
    print(LOAD)
    load_values.append(LOAD)

import matplotlib.pyplot as plt
# load_values = []
# for x in range(1440):
#     LOAD = 0.0
#
#     if(DomesticHotWaterControllerBoilerState and DomesticHotWaterControllerBoilerCount < 36):
#         LOAD = LOAD + DomesticHotWaterControllerBoilerHouse5Day1[DomesticHotWaterControllerBoilerCount]
#         DomesticHotWaterControllerBoilerCount+=1
#     if (WashingMachineCount < 72):
#         LOAD = LOAD + WashingMachineUsageHouse5Day1[WashingMachineCount]
#         WashingMachineCount += 1
#
#     if (HeatPumpUsageCount < 1402):
#         LOAD = LOAD + HeatPumpUsageHouse5Day1[HeatPumpUsageCount]
#         HeatPumpUsageCount += 1
#
#     LOAD = LOAD - PVHouse5Day1[x]
#
#     print(LOAD)
#     load_values.append(LOAD)
plt.plot(load_values)
plt.title("Load Over Time")
plt.xlabel("Time (minutes)")
plt.ylabel("LOAD (kW)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
code="no"
while code=="no":
    code=input()





#
#
#
# if(DomesticHotWaterControllerBoilerState and DomesticHotWaterControllerBoilerCount < 36):
#         LOAD = LOAD + DomesticHotWaterControllerBoilerHouse5Day1[DomesticHotWaterControllerBoilerCount]
#         DomesticHotWaterControllerBoilerCount+=1
#         print("DomesticHotWaterControllerBoilerHouse5Day1=",DomesticHotWaterControllerBoilerHouse5Day1[DomesticHotWaterControllerBoilerCount])
#     if (WashingMachineCount < 72):
#         LOAD = LOAD + WashingMachineUsageHouse5Day1[WashingMachineCount]
#         WashingMachineCount += 1
#         print("WashingMachineUsageHouse5Day1=",WashingMachineUsageHouse5Day1[WashingMachineCount])
#
#     if (HeatPumpUsageCount < 1402):
#         LOAD = LOAD + HeatPumpUsageHouse5Day1[HeatPumpUsageCount]
#         HeatPumpUsageCount += 1
#         print("HeatPumpUsageHouse5Day1=",HeatPumpUsageHouse5Day1[HeatPumpUsageCount])
