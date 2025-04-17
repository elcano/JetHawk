##########DEPENDENCIES#############
# https://dronekit.io/

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
import argparse


#########FUNCTIONS#################

def connectMyCopter():
    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect')
    args = parser.parse_args()

    connection_string = args.connect

    vehicle = connect(connection_string, baud=57600, wait_ready=True)

    return vehicle


def get_direction_to_target(targetLocation, currentLocation):
    dLat = targetLocation.lat - currentLocation.lat
    dLon = targetLocation.lon - currentLocation.lon

    # Calculate angle in radians and convert to degrees
    angle = math.atan2(dLon, dLat) * (180 / math.pi)
    if angle < 0:
        angle += 360  # Normalize angle to 0-360 degrees

    # Determine compass direction
    if 337.5 <= angle < 360 or 0 <= angle < 22.5:
        direction = "N"
    elif 22.5 <= angle < 67.5:
        direction = "NE"
    elif 67.5 <= angle < 112.5:
        direction = "E"
    elif 112.5 <= angle < 157.5:
        direction = "SE"
    elif 157.5 <= angle < 202.5:
        direction = "S"
    elif 202.5 <= angle < 247.5:
        direction = "SW"
    elif 247.5 <= angle < 292.5:
        direction = "W"
    elif 292.5 <= angle < 337.5:
        direction = "NW"

    return f"{direction} ({angle:.1f}°)"


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in meters


def calculate_direction(targetLocation, vehicle):
    while True:
        currentLocation = vehicle.location.global_relative_frame

        if currentLocation and currentLocation.lat and currentLocation.lon:
            direction = get_direction_to_target(targetLocation, currentLocation)
            distance = haversine_distance(
                currentLocation.lat, currentLocation.lon, targetLocation.lat, targetLocation.lon
            )

            print(f"Current Location: ({currentLocation.lat}, {currentLocation.lon})")
            print(f"Destination: ({targetLocation.lat}, {targetLocation.lon})")
            print(f"Direction to target: {direction}")
            print(f"Distance to target: {distance:.2f} meters\n")

            # Check if we've reached the destination (within 5 meters)
            if distance < 5:
                print("Congrats! You reached your destination!")
                break

            time.sleep(1)
        else:
            print("Waiting for valid location data...")
            time.sleep(1)


##########MAIN EXECUTABLE STUFF###########

destination = LocationGlobalRelative(47.63195438872842, -122.0527076386417, 2)

vehicle = connectMyCopter()

try:
    print("Navigating to destination...")
    calculate_direction(destination, vehicle)
finally:
    vehicle.close()