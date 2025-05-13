#Old Code Storage

# import sqlite3
# import psycopg2
#
# sqlite_conn = sqlite3.connect('rawdata.db', detect_types=sqlite3.PARSE_DECLTYPES)
# sqlite_cur = sqlite_conn.cursor()
#
# sqlite_cur.execute("DROP TABLE IF EXISTS ApplianceUsage")
# sqlite_cur.execute("""
#     CREATE TABLE ApplianceUsage (
#         appliance_usage_id INTEGER PRIMARY KEY,
#         appliance_id INTEGER NOT NULL,
#         mean_energy_kwh REAL NOT NULL,
#         timestamp TEXT NOT NULL
#     )
# """)
#
# pg_conn = psycopg2.connect(
#     host="saxion-mmc.xyz",
#     database="mmc",
#     user="guest",
#     password="mypassword"
# )
# pg_cur = pg_conn.cursor()
#
# pg_cur.execute("""
#     SELECT
#         appliance_usage_id,
#         appliance_id,
#         mean_energy_kwh::FLOAT,
#         to_char(timestamp, 'YYYY-MM-DD HH24:MI:SS') as timestamp
#     FROM ApplianceUsage
# """)
#
# rows = pg_cur.fetchall()
#
# sqlite_cur.executemany("""
#     INSERT INTO ApplianceUsage (appliance_usage_id, appliance_id, mean_energy_kwh, timestamp)
#     VALUES (?, ?, ?, ?)
# """, rows)
#
# sqlite_conn.commit()
# pg_cur.close()
# pg_conn.close()
# sqlite_cur.close()
# sqlite_conn.close()


###########################################################################################################

#
#
#
# import psycopg2
#
# conn = psycopg2.connect(
#     host="saxion-mmc.xyz",
#     database="mmc",
#     user="guest",
#     password="mypassword"
# )
#
# cur = conn.cursor()
#
# cur.execute("""
#     SELECT mean_energy_kwh
#     FROM ApplianceUsage au
#     JOIN Appliances a ON au.appliance_id = a.appliance_id
#     JOIN Houses h ON a.house_id = h.house_id
#     WHERE h.house_id = 0 AND au.timestamp = '2023-01-01 11:08:00'
#     LIMIT 10;
# """)
# for row in cur.fetchall():
#     print(row)
#
# cur.close()
# conn.close()


# if (DomesticHotWaterControllerBoilerCount < 36):
#     LOAD =WashingMachineUsageHouse5Day1[x] + HeatPumpUsageHouse5Day1[x] + DomesticHotWaterControllerBoilerHouse5Day1[x] - PVHouse5Day1[x]
# elif (WashingMachineCount < 72):
#     LOAD =WashingMachineUsageHouse5Day1[x] + HeatPumpUsageHouse5Day1[x]  - PVHouse5Day1[x]
# elif (HeatPumpUsageCount < 1402):
#     LOAD =HeatPumpUsageHouse5Day1[x] - PVHouse5Day1[x]
# else:
#     print( - PVHouse5Day1[x])
# if(LOAD>1500):
#     print(x)
# WashingMachineCount += 1
# HeatPumpUsageCount += 1
# DomesticHotWaterControllerBoilerCount += 1






#
#
# for x in range(1440):
#     LOAD = 0.0
#     if(LOADLIMIT):
#         if DomesticHotWaterControllerBoilerState:
#             DomesticHotWaterControllerBoilerState = False
#     else:
#         if DomesticHotWaterControllerBoilerState == False:
#             DomesticHotWaterControllerBoilerState = True
#     if(DomesticHotWaterControllerBoilerState and DomesticHotWaterControllerBoilerCount < 36):
#         LOAD = LOAD + DomesticHotWaterControllerBoilerHouse5Day1[DomesticHotWaterControllerBoilerCount]
#         DomesticHotWaterControllerBoilerCount+=1
#     if (WashingMachineCount < 72):
#         LOAD = LOAD + WashingMachineUsageHouse5Day1[WashingMachineCount]
#         WashingMachineCount += 1
#     if (HeatPumpUsageCount < 1402):
#         LOAD = LOAD + HeatPumpUsageHouse5Day1[HeatPumpUsageCount]
#         HeatPumpUsageCount += 1
#     LOAD = LOAD - PVHouse5Day1[x]
#     if(LOAD>1500):
#         LOADLIMIT=False
#     else:
#         LOADLIMIT=True
#     print(LOAD)











# import sqlite3
#
# conn = sqlite3.connect('rawdata.db')
# cursor = conn.cursor()
#
# cursor.execute("select * from DomesticHotWaterControllerBoilerHouse5Day1 limit 100")
#
# for row in cursor.fetchall():
#     print(row[2])
#
# conn.close()
#


###########################################################################################################




import psycopg2

conn = psycopg2.connect(
    host="saxion-mmc.xyz",
    database="mmc",
    user="guest",
    password="mypassword"
)

cur = conn.cursor()

cur.execute("""
    SELECT *
    FROM ApplianceUsage
    JOIN Appliances ON ApplianceUsage.appliance_id = Appliances.appliance_id
    JOIN Houses ON Appliances.house_id = Houses.house_id
    WHERE Houses.house_id = 1
    and ApplianceUsage.timestamp=""
    LIMIT 50000;
""")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()




###########################################################################################################
#
# import sqlite3
# import psycopg2
#
# sqlite_conn = sqlite3.connect('rawdata.db', detect_types=sqlite3.PARSE_DECLTYPES)
# sqlite_cur = sqlite_conn.cursor()
#
# sqlite_cur.execute("DROP TABLE IF EXISTS ApplianceUsage")
# sqlite_cur.execute("""
#     CREATE TABLE ApplianceUsage (
#         appliance_usage_id INTEGER PRIMARY KEY,
#         appliance_id INTEGER NOT NULL,
#         mean_energy_kwh REAL NOT NULL,
#         timestamp TEXT NOT NULL
#     )
# """)
#
# pg_conn = psycopg2.connect(
#     host="saxion-mmc.xyz",
#     database="mmc",
#     user="guest",
#     password="mypassword"
# )
# pg_cur = pg_conn.cursor()
#
# # Use SQL to explicitly select and cast values in the right order
# pg_cur.execute("""
#     SELECT
#         appliance_usage_id,
#         appliance_id,
#         mean_energy_kwh::FLOAT,
#         to_char(timestamp, 'YYYY-MM-DD HH24:MI:SS') as timestamp
#     FROM ApplianceUsage
# """)
#
# rows = pg_cur.fetchall()
#
# # Insert into SQLite
# sqlite_cur.executemany("""
#     INSERT INTO ApplianceUsage (appliance_usage_id, appliance_id, mean_energy_kwh, timestamp)
#     VALUES (?, ?, ?, ?)
# """, rows)
#
# # Finalize
# sqlite_conn.commit()
# pg_cur.close()
# pg_conn.close()
# sqlite_cur.close()
# sqlite_conn.close()