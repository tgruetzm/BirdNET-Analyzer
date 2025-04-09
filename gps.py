import pandas as pd

# Constants for conversion
FEET_TO_LAT = 0.00000274  # 1 foot ≈ 0.00000274 degrees latitude
FEET_TO_LON = 0.00000355  # 1 foot ≈ 0.00000355 degrees longitude at given latitude

# Starting coordinates
start_lat = 46.75686
start_lon = -114.0659

# Newest set of offsets (North in feet, East in feet)
latest_offsets = [
    (122.5, 108.5),
    (120.5, 82),
    (164, 78),
    (166.5, 105),
    (197.5, 102),
    (200.5, 139),
    (136, 144.5),
    (132.5, 108),
    (50,50)
]

# Compute new waypoints
latest_waypoints = []
for north_ft, east_ft in latest_offsets:
    new_lat = start_lat + (north_ft * FEET_TO_LAT)
    new_lon = start_lon + (east_ft * FEET_TO_LON)
    print(f"{new_lat:.6f},{new_lon:.6f}")

# Create DataFrame and save as CSV
df_latest = pd.DataFrame(latest_waypoints, columns=["Latitude", "Longitude"])
#csv_latest_filename = "C:\Users\Troy\Downloads\gps_waypoints_latest.csv"
#df_latest.to_csv(csv_latest_filename, index=False)

#csv_latest_filename