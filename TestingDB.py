import sqlite3
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict


def input_day_and_month(year="2023"):
    """
    Prompt for day (01–31) and month (01–12), zero-pad them,
    and return (day_str, month_str, year_str).
    """
    # Day
    while True:
        d = input("Enter day (01–31): ").strip()
        if d.isdigit() and 1 <= int(d) <= 31:
            day_str = f"{int(d):02d}"
            break
        print(" → Invalid. Please enter a number from 01 to 31.")
    # Month
    while True:
        m = input("Enter month (01–12): ").strip()
        if m.isdigit() and 1 <= int(m) <= 12:
            month_str = f"{int(m):02d}"
            break
        print(" → Invalid. Please enter a number from 01 to 12.")
    return day_str, month_str, year


def build_and_sort_house_map(cursor, day_str, month_str, year_str, max_house_id=5):
    """
    Queries ApplianceUsage & Appliances for all houses ≤ max_house_id
    on the given date (day, month, year) with mean_energy_kwh>0,
    builds a house_map {house_id: {'count', 'devices'}}, and returns:
      - house_map (dict)
      - sorted_houses (list of (house_id, info) sorted by count desc)
    """
    query = """
    SELECT 
        a.house_id,
        a.appliance_name
    FROM ApplianceUsage au
    JOIN Appliances a 
      ON au.appliance_id = a.appliance_id
    WHERE au.mean_energy_kwh     > 0
      AND strftime('%d', au.timestamp) = ?
      AND strftime('%m', au.timestamp) = ?
      AND strftime('%Y', au.timestamp) = ?
      AND a.house_id            <= ?;
    """
    params = (day_str, month_str, year_str, max_house_id)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    house_map = defaultdict(lambda: {'count': 0, 'devices': []})
    for house_id, appliance in rows:
        entry = house_map[house_id]
        if appliance not in entry['devices']:
            entry['devices'].append(appliance)
            entry['count'] += 1

    sorted_houses = sorted(
        house_map.items(),
        key=lambda item: item[1]['count'],
        reverse=True
    )
    return dict(house_map), sorted_houses


def get_pv_data(cursor, house_ids, day_str, month_str, year_str):
    """
    Fetch PV generation data for each house in house_ids on the given date.
    Returns dict mapping house_id to list of per-minute generation values.
    """
    pv_map = {}
    query = """
    SELECT house_id, watts_generated
    FROM PV
    WHERE house_id = ?
      AND strftime('%d', time) = ?
      AND strftime('%m', time) = ?
      AND strftime('%Y', time) = ?
    ORDER BY time;
    """
    for hid in house_ids:
        print(f"Fetching PV data for house {hid} and {house_ids}...")
        cursor.execute(query, (hid, day_str, month_str, year_str))
        # collect per-minute values
        pv_map[hid] = [row[1] for row in cursor.fetchall()]
    return pv_map


def is_within_time_window(current_time, windows):
    return any(start <= current_time < end for start, end in windows)


if __name__ == "__main__":
    # 1) gather date filters
    day_str, month_str, year_str = input_day_and_month(year="2023")

    # 2) open DB
    conn = sqlite3.connect('rawdata.db')
    cursor = conn.cursor()

    # 3) build & sort house map
    house_map, sorted_houses = build_and_sort_house_map(
        cursor, day_str, month_str, year_str, max_house_id=5
    )
    print("\nHouse map by active appliance count:")
    for h, info in sorted_houses:
        print(f"House {h}: {info['count']} -> {info['devices']}")

    # 4) get PV data for each house
    house_ids = list(house_map.keys())
    pv_data = get_pv_data(cursor, house_ids, day_str, month_str, year_str)
    print("\nPV Generation Data by House:")
    for h, values in pv_data.items():
        print(f"House {h}: {len(values)} minutes of data")

    # 5) fetch PV data for house 5 specifically for load shifting
    PVHouse5Day = pv_data.get(5, [])

    # 6) prepare device definitions
    devices = [
        ["DomesticHotWaterControllerBoiler", 1, datetime.time(hour=5), datetime.time(hour=9), datetime.time(hour=16), datetime.time(hour=21)],
        ["HeatPump", 2, datetime.time(hour=4), datetime.time(hour=8)],
        ["SmartMeter", 4],
        ["WashingMachine", 3],
        ["DishWasher",5]
    ]

    device_data = {}
    device_state = defaultdict(bool)
    device_counter = defaultdict(int)
    device_priority = {}
    device_time_windows = {}

    # 7) load device usage for the chosen date
    base_query = (
        "SELECT au.mean_energy_kwh "
        "FROM ApplianceUsage au "
        "JOIN Appliances a ON au.appliance_id = a.appliance_id "
        "WHERE a.appliance_name = ? "
        "AND a.house_id = 5 "
        "AND au.mean_energy_kwh > 0 "
        "AND strftime('%d', au.timestamp) = ? "
        "AND strftime('%m', au.timestamp) = ? "
        "AND strftime('%Y', au.timestamp) = ?;"
    )

    for entry in devices:
        name, prio, *times = entry
        device_priority[name] = prio
        device_state[name] = True
        device_counter[name] = 0

        # build time windows
        if len(times) >= 2:
            windows = []
            for i in range(0, len(times), 2):
                windows.append((times[i], times[i+1]))
            device_time_windows[name] = windows

        cursor.execute(base_query, (name, day_str, month_str, year_str))
        device_data[name] = [r[0] for r in cursor.fetchall()]

    conn.close()

    devices_sorted = sorted(devices, key=lambda x: x[1])

    # 8) simulate load shifting over 24h
    LOAD = 0.0
    LOADLIMIT = False
    load_values = []

    for minute in range(1440):
        LOAD = 0.0
        t = datetime.time(hour=minute//60, minute=minute%60)

        # enforce windows
        for dev in device_state:
            device_name = dev[0]
            if device_name in device_time_windows and not is_within_time_window(t, device_time_windows[dev]):
                device_state[dev] = False

        # load limiting
        if LOADLIMIT:
            for dev in devices_sorted:
                device_name = dev[0]
                if device_state[device_name]:
                    device_state[device_name] = False
                    break
        else:
            for dev in devices_sorted:
                device_name = dev[0]
                if not device_state[device_name]:
                    if dev in device_time_windows:
                        if is_within_time_window(t, device_time_windows[dev]):
                            device_state[device_name] = True
                            break
                    else:
                        device_state[device_name] = True
                        break

        # accumulate
        for dev, *_ in devices:
            device_name = dev[0]
            idx = device_counter[device_name]
            if device_state[device_name] and idx < len(device_data[device_name]):
                LOAD += device_data[device_name][idx]
                device_counter[dev] += 1

        # subtract PV
        if minute < len(PVHouse5Day):
            LOAD -= PVHouse5Day[minute]

        LOADLIMIT = LOAD > 200000
        load_values.append(LOAD)
        print(f"{t} -> Load: {LOAD:.2f} kWh")

    # 9) plot
    plt.plot(load_values)
    plt.title("Load Over Time")
    plt.xlabel("Time (minutes)")
    plt.ylabel("LOAD (kW)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
