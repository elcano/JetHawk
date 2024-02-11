from pymavlink import mavutil
import time
import math
import csv
from datetime import datetime

# Connect to the Pixhawk
port_name = '/dev/ttyACM0'
baud_rate = 57600
master = mavutil.mavlink_connection(port_name, baud_rate)

# CSV file setup
csv_filename = "pixhawk_data.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time (ms)", "Pitch", "Roll", "Yaw", "Latitude", "Longitude", "GPS Fix Type"])  # Write header

    while True:
        try:
            # Wait for a heartbeat to find the system ID and component ID
            master.wait_heartbeat()

            # Fetch and print rotatation/positional data
            attitude_message = master.recv_match(type='ATTITUDE', blocking=True, timeout=3)
            if attitude_message:
                pitch = math.degrees(attitude_message.pitch)  # Convert to degrees
                roll = math.degrees(attitude_message.roll)   # Convert to degrees
                yaw = math.degrees(attitude_message.yaw)     # Convert to degrees
                print(f"Pitch: {pitch:.2f}, Roll: {roll:.2f}, Yaw: {yaw:.2f}")

            # Fetch and print GPS data along with fix status
            gps_message = master.recv_match(type='GPS_RAW_INT', blocking=True, timeout=3)
            if gps_message:
                lat = gps_message.lat / 1e7  # Convert latitude to degrees
                lon = gps_message.lon / 1e7  # Convert longitude to degrees
                fix_type = gps_message.fix_type  # GPS fix type
                print(f"Latitude: {lat}, Longitude: {lon}, GPS Fix Type: {fix_type}")

                # Write data to CSV
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Time in milliseconds
                writer.writerow([current_time, pitch, roll, yaw, lat, lon, fix_type])

        except KeyboardInterrupt:
            print("Stopping data collection")
            break

        time.sleep(0.09)  # Add delay to reduce the rate of requests