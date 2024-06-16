# 6/15/2024 Car_works_5_29_24.py
# Version: Python 3.6; run in terminal of Jet-nano(code python3 Car.py; depend on the file path)

# Import necessary libraries: pymavlink for MAVLink communication, time for delays, math for mathematical operations
from pymavlink import mavutil
import time
import math


def setup_connection():
    # Inform the user that the script is attempting to connect to the Pixhawk
    print("Connecting to Pixhawk...")

    # Establish a connection to the Pixhawk on a specific ACMO port with a set baud rate
    # Update this line with the correct ACMO port from Jetnano (change to different USB port, might be change code)
    connection = mavutil.mavlink_connection('COM4', baud=9600)

    # Inform the user that the script is waiting for a heartbeat message to confirm the connection
    print("Waiting for heartbeat...")

    # Wait for the first heartbeat
    # This ensures the connection is established and communication is active
    connection.wait_heartbeat()

    # Inform the user that a heartbeat has been received and the connection is successfully established
    print("Heartbeat received. Pixhawk is connected.")

    # Request that the Pixhawk send all available data streams at a rate of 10 Hz
    connection.mav.request_data_stream_send(
        connection.target_system,  # The system ID of the Pixhawk
        connection.target_component,  # The component ID of the Pixhawk
        mavutil.mavlink.MAV_DATA_STREAM_ALL,  # Request all possible data streams
        10,  # Frequency of 10 Hz
        1  # Start sending data
    )

    # Return the connection object to be used for data fetching
    return connection

# Function to convert the latitude and longitude to x and y in meters
def convert_lat_long(latitudeOrigin, longitudeOrigin, latitudeDest, longitudeDest):
    EarthRadius = 6378
    x = EarthRadius * (longitudeDest - longitudeOrigin) * math.pi / (180 * math.cos(latitudeOrigin * math.pi / 180))
    y = EarthRadius * (latitudeDest - latitudeOrigin) * math.pi / 180

    return x, y

def main():
    # Initialize the connection and assign it to a variable
    master = setup_connection()

    # Variables to store the initial and current GPS coordinates
    initial_lat = None
    initial_lon = None

    # Main loop to continuously fetch data
    while True:
        try:
            # Attempt to receive attitude data from the Pixhawk
            attitude_message = master.recv_match(type='ATTITUDE', blocking=True, timeout=3)

            # Check if attitude data was received
            if attitude_message:
                # Convert the pitch, roll, and yaw data from radians to degrees
                pitch = math.degrees(attitude_message.pitch)
                roll = math.degrees(attitude_message.roll)
                yaw = math.degrees(attitude_message.yaw)

                # Print the formatted attitude data
                print(f"Pitch: {pitch:.2f}, Roll: {roll:.2f}, Yaw: {yaw:.2f}")
            else:
                # Notify if no attitude data was received
                print("No attitude data received.")

            # Attempt to receive GPS data from the Pixhawk
            gps_message = master.recv_match(type='GPS_RAW_INT', blocking=True, timeout=3)

            # Check if GPS data was received and it has a valid fix
            if gps_message and gps_message.fix_type >= 2:
                # Convert the latitude and longitude from 1E7 scaled integers to float degrees
                current_lat = gps_message.lat
                current_lon = gps_message.lon

                 # Set the initial coordinates if they are not already set
                if initial_lat is None and initial_lon is None:
                    initial_lat = current_lat
                    initial_lon = current_lon

                # Print the formatted GPS data
                print(f"Latitude: {current_lat / 1e7}, Longitude: {current_lon / 1e7}, GPS Fix Type: {gps_message.fix_type}")

                # Calculate and print distance traveled from the initial coordinates
                if initial_lat is not None and initial_lon is not None:
                    x, y = convert_lat_long(initial_lat / 1e7, initial_lon / 1e7, current_lat / 1e7, current_lon / 1e7)
                    print(f"Distance from origin: x = {x:.2f} meters, y = {y:.2f} meters")
                

            else:
                # Notify if no GPS data was received or the fix was invalid
                print("No GPS data received or no valid fix.")

        # Handle keyboard interrupt (Ctrl+C) to stop the script gracefully
        except KeyboardInterrupt:
            print("Stopping data collection.")
            break

        # Handle other exceptions that may occur
        except Exception as e:
            print(f"An error occurred: {e}. Attempting to reconnect...")
            # Re-establish connection if an error occurs
            master = setup_connection()

        # Insert a short delay to reduce the load on the CPU and prevent flooding with data
        time.sleep(3)


# Ensure the script runs only if it is executed directly, not when imported as a module
if __name__ == "__main__":
    main()
