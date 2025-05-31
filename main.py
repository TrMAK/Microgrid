import sqlite3
import datetime
import matplotlib.pyplot as plt

def is_within_time_window(current_time, windows):
    return any(start <= current_time < end for start, end in windows)

def simulate_load(load_shift_enabled):
    conn = sqlite3.connect('rawdata.db')
    cursor = conn.cursor()

    devices = [
        ["DomesticHotWaterControllerBoiler", 1, datetime.time(hour=5), datetime.time(hour=9), datetime.time(hour=16), datetime.time(hour=21)],
        ["HeatPump", 2, datetime.time(hour=4), datetime.time(hour=8)],
        ["SmartMeter", 4],
        ["WashingMachine", 3],
        ["DishWasher", 5],
        ["ElectricVehicle", 6]
    ]
    houses = [1,2,3,4,5,6,7,8,9,10]

    device_time_windows = {}
    for entry in devices:
        device_name = entry[0]
        time_pairs = entry[2:]
        if len(time_pairs) >= 2:
            windows = []
            for i in range(0, len(time_pairs), 2):
                windows.append((time_pairs[i], time_pairs[i + 1]))
            device_time_windows[device_name] = windows

    days_to_simulate = 5
    load_values = []

    for day in range(1, days_to_simulate + 1):
        date_filter = f"{day:02d}/01/2023"

        cursor.execute(f"""
            SELECT time, SUM(watts_generated)
            FROM pv
            WHERE time LIKE ?
            AND house_id IN ({','.join(['?'] * len(houses))})
            GROUP BY time
            ORDER BY time
        """, (f"{date_filter}%", *houses))
        PV_data = [row[1] for row in cursor.fetchall()]

        device_data = {house: {} for house in houses}
        device_state = {house: {} for house in houses}
        device_counter = {house: {} for house in houses}
        device_priority = {house: {} for house in houses}

        for house_id in houses:
            for entry in devices:
                device_name = entry[0]
                priority = entry[1]

                device_priority[house_id][device_name] = priority
                device_state[house_id][device_name] = True
                device_counter[house_id][device_name] = 0

                cursor.execute("""
                    SELECT au.mean_energy_kwh
                    FROM ApplianceUsage au
                    JOIN Appliances a ON au.appliance_id = a.appliance_id
                    WHERE a.appliance_name = ?
                    AND a.house_id = ?
                    AND au.mean_energy_kwh > 0
                    AND strftime('%d', au.timestamp) = ?
                    AND strftime('%m', au.timestamp) = '01'
                    AND strftime('%Y', au.timestamp) = '2023'
                """, (device_name, house_id, f"{day:02d}"))
                device_data[house_id][device_name] = [row[0] for row in cursor.fetchall()]

        global_device_list = sorted((entry[1], house, entry[0]) for house in houses for entry in devices)

        for minute in range(1440):
            current_time = datetime.time(hour=minute // 60, minute=minute % 60)
            LOAD = 0.0

            if load_shift_enabled:
                for house_id in houses:
                    for entry in devices:
                        device_name = entry[0]
                        if device_name in device_time_windows:
                            if not is_within_time_window(current_time, device_time_windows[device_name]):
                                device_state[house_id][device_name] = False

            for house_id in houses:
                for entry in devices:
                    device_name = entry[0]
                    values = device_data[house_id].get(device_name, [])
                    counter = device_counter[house_id][device_name]
                    if device_state[house_id][device_name] and counter < len(values):
                        LOAD += values[counter]

            if minute < len(PV_data):
                LOAD -= PV_data[minute]

            if load_shift_enabled:
                if LOAD > 15000:
                    for _, house_id, device_name in global_device_list:
                        if device_state[house_id][device_name]:
                            device_state[house_id][device_name] = False
                            break
                else:
                    for _, house_id, device_name in global_device_list:
                        if not device_state[house_id][device_name]:
                            if device_name in device_time_windows:
                                if is_within_time_window(current_time, device_time_windows[device_name]):
                                    device_state[house_id][device_name] = True
                                    break
                            else:
                                device_state[house_id][device_name] = True
                                break

            for house_id in houses:
                for entry in devices:
                    device_name = entry[0]
                    values = device_data[house_id].get(device_name, [])
                    counter = device_counter[house_id][device_name]
                    if device_state[house_id][device_name] and counter < len(values):
                        device_counter[house_id][device_name] += 1

            load_values.append(LOAD)

    conn.close()
    return load_values


baseline_load = simulate_load(load_shift_enabled=False)
shifted_load = simulate_load(load_shift_enabled=True)

plt.figure(figsize=(12, 6))
plt.plot(baseline_load, label='Before Load Shift', alpha=0.7)
plt.plot(shifted_load, label='After Load Shift', alpha=0.7)
plt.axhline(y=50000, color='red', linestyle='--', label='Threshold')
plt.title("Load Comparison Before and After Load Shifting")
plt.xlabel("Time (minutes)")
plt.ylabel("LOAD (kW)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
