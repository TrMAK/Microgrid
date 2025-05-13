import sqlite3
import matplotlib.pyplot as plt
import datetime

conn = sqlite3.connect('rawdata.db')
cursor = conn.cursor()

devices = [
    ["DomesticHotWaterControllerBoiler", 1, datetime.time(hour=5), datetime.time(hour=9), datetime.time(hour=16), datetime.time(hour=21)],
    ["HeatPump", 2, datetime.time(hour=4), datetime.time(hour=8)],
    ["SmartMeter", 4],
    ["WashingMachine", 3],
    ["DishWasher",5]
]


device_data = {}
device_state = {}
device_counter = {}
device_priority = {}
device_time_windows = {}

cursor.execute("SELECT * FROM PVHouse5Day1")
PVHouse5Day1 = [row[1] for row in cursor.fetchall()]
for entry in devices:
    device_name = entry[0]
    priority = entry[1]
    time_pairs = entry[2:]

    device_priority[device_name] = priority
    device_state[device_name] = True
    device_counter[device_name] = 0

    if len(time_pairs) >= 2:
        windows = []
        for i in range(0, len(time_pairs), 2):
            start = time_pairs[i]
            end = time_pairs[i + 1]
            windows.append((start, end))
        device_time_windows[device_name] = windows

    query = (
        "SELECT au.mean_energy_kwh "
        "FROM ApplianceUsage au "
        "JOIN Appliances a ON au.appliance_id = a.appliance_id "
        "WHERE a.appliance_name = ? "
        "AND a.house_id = 5 "
        "AND au.mean_energy_kwh > 0 "
        "AND strftime('%d', au.timestamp) = '01' "
        "AND strftime('%m', au.timestamp) = '01' "
        "AND strftime('%Y', au.timestamp) = '2023';"
    )
    cursor.execute(query, (device_name,))
    device_data[device_name] = [row[0] for row in cursor.fetchall()]
conn.close()

devices_sorted = sorted(devices, key=lambda x: x[1])

LOAD = 0.0
LOADLIMIT = False
load_values = []
def is_within_time_window(current_time, windows):
    return any(start <= current_time < end for start, end in windows)



for minute in range(1440):
    LOAD = 0.0
    current_time = datetime.time(hour=minute // 60, minute=minute % 60)

    for device_name in device_state:
        if device_name in device_time_windows:
            windows = device_time_windows[device_name]
            if not is_within_time_window(current_time, windows):
                device_state[device_name] = False

    if LOADLIMIT:
        for entry in devices_sorted:
            device_name = entry[0]
            if device_state[device_name]:
                device_state[device_name] = False
                break
    else:
        for entry in devices_sorted:
            device_name = entry[0]
            if not device_state[device_name]:
                if device_name in device_time_windows:
                    windows = device_time_windows[device_name]
                    if is_within_time_window(current_time, windows):
                        device_state[device_name] = True
                        break
                else:
                    device_state[device_name] = True
                    break

    for entry in devices:
        device_name = entry[0]
        values = device_data.get(device_name, [])
        counter = device_counter[device_name]

        if device_state[device_name] and counter < len(values):
            LOAD += values[counter]
            device_counter[device_name] += 1

    if minute < len(PVHouse5Day1):
        LOAD -= PVHouse5Day1[minute]

    LOADLIMIT = LOAD > 20000

    print(f"{current_time} -> Load: {LOAD:.2f} kWh")
    load_values.append(LOAD)
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

#Without Load Shifting


# import sqlite3
# import matplotlib.pyplot as plt
# import datetime
#
# conn = sqlite3.connect('rawdata.db')
# cursor = conn.cursor()
#
# devices = [
#     ["DomesticHotWaterControllerBoiler", 1, datetime.time(hour=5), datetime.time(hour=9), datetime.time(hour=16), datetime.time(hour=21)],
#     ["HeatPump", 2, datetime.time(hour=4), datetime.time(hour=8)],
#     ["SmartMeter", 4],
#     ["WashingMachine", 3],
#     ["DishWasher",5]
# ]
#
#
# device_data = {}
# device_state = {}
# device_counter = {}
# device_priority = {}
# device_time_windows = {}
#
# cursor.execute("SELECT * FROM PVHouse5Day1")
# PVHouse5Day1 = [row[1] for row in cursor.fetchall()]
# for entry in devices:
#     device_name = entry[0]
#     priority = entry[1]
#     time_pairs = entry[2:]
#
#     device_priority[device_name] = priority
#     device_state[device_name] = True
#     device_counter[device_name] = 0
#
#     if len(time_pairs) >= 2:
#         windows = []
#         for i in range(0, len(time_pairs), 2):
#             start = time_pairs[i]
#             end = time_pairs[i + 1]
#             windows.append((start, end))
#         device_time_windows[device_name] = windows
#
#     query = (
#         "SELECT au.mean_energy_kwh "
#         "FROM ApplianceUsage au "
#         "JOIN Appliances a ON au.appliance_id = a.appliance_id "
#         "WHERE a.appliance_name = ? "
#         "AND a.house_id = 5 "
#         "AND au.mean_energy_kwh > 0 "
#         "AND strftime('%d', au.timestamp) = '01' "
#         "AND strftime('%m', au.timestamp) = '01' "
#         "AND strftime('%Y', au.timestamp) = '2023';"
#     )
#     cursor.execute(query, (device_name,))
#     device_data[device_name] = [row[0] for row in cursor.fetchall()]
# conn.close()
#
# devices_sorted = sorted(devices, key=lambda x: x[1])
#
# LOAD = 0.0
# LOADLIMIT = False
# load_values = []
#
# def is_within_time_window(current_time, windows):
#     return any(start <= current_time < end for start, end in windows)
#
#
#
# for minute in range(1440):
#     LOAD = 0.0
#     current_time = datetime.time(hour=minute // 60, minute=minute % 60)
#
#     for entry in devices:
#         device_name = entry[0]
#         values = device_data.get(device_name, [])
#         counter = device_counter[device_name]
#
#         if device_state[device_name] and counter < len(values):
#             LOAD += values[counter]
#             device_counter[device_name] += 1
#
#     if minute < len(PVHouse5Day1):
#         LOAD -= PVHouse5Day1[minute]
#
#     LOADLIMIT = LOAD > 1500
#
#     print(f"{current_time} -> Load: {LOAD:.2f} kWh")
#     load_values.append(LOAD)
# plt.plot(load_values)
# plt.title("Load Over Time")
# plt.xlabel("Time (minutes)")
# plt.ylabel("LOAD (kW)")
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
# code="no"
# while code=="no":
#     code=input()
