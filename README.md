# JetHawk
Code on Jetson Nano and Pixhawk to direct vehicle to waypoints

June 12th, 2024

The Jetson Nano computes the course to the next waypoint and communicates that information over a CAN link to the Drive-By-Wire computer.
https://www.elcanoproject.org/wiki/Communication

# Overview
Jetson Nano: The Jetson Nano is a small, powerful computer made by Nvidia designed for artificial intelligence (AI) and embedded applications as edge computing. In simpler terms, it's a tiny computer with a lot of processing power specifically suited for running AI tasks on devices, rather than relying on a connection to the cloud for processing.

Pixhawk: Pixhawk is an open-source hardware and software project that designs and produces flight controllers for drones, other unmanned aerial vehicles (UAVs) as well as rovers on land and water. It provides the hardware and software needed to control and navigate these devices, integrating sensors, communication modules, and processors to ensure stable flight and autonomous operations. It depends on an external GNSS reciever.

In this project, the Pixhawk serves as a device that retrieves data to be processed by the Jetson Nano. The specific data obtained includes:
1. Pitch: Pitch refers to the rotation around the lateral (side-to-side) axis of the vehicle.
2. Roll: Roll refers to the rotation around the longitudinal (front-to-back) axis of the vehicle.
3. Yaw: Yaw refers to the rotation around the vertical (up-and-down) axis of the vehicle.
4. Longitude
5. Latitude
6. Velocity

To execute this project, you'll need several Python libraries, including:
1. pymavlink: Install this on your computer if you haven't already by running `pip install pymavlink`

# Running the files
## Steps to Clone the Repository
1. Navigate to Your Desired Directory:
  1. Change to the directory where you want to clone the repository
  2. `cd path/to/your/desired/directory`
2. Clone the Repository:
   1. Use the git clone command to clone the repository.
   2. `git clone https://github.com/yourusername/yourrepository.git`

## Running with Jetson Nano
1. Connect the Jetson Nano and Pixhawk:
  1. Use the USB cable to connect the Jetson Nano to the Pixhawk.
  2. By default, the listening port is set to TTYACM0.
  3. Connect cable from Pixhawk GPS port to GNSS device.
  4. Connect cable from Pixhawk I2C port to GNSS device.
2. Navigate to the repository:
  1. `cd path/to/your/desired/directory`
3. Execute the Script: `python3 Car_works_5_29_24.py`

## Running without Jetson Nano
1. Connect the Pixhawk: Use the USB cable to connect the Pixhawk to your computer.
2. Find the Connected Port:
  1. On a Windows operating system: Go to Control Panels -> Devices and Printers -> Device Manager -> Ports (COM & LPT).
  2. Locate the port name (e.g., COM3).
3. Update the Script:
  1. Open the Car_works_5_29_24.py script in a text editor.
  2. Find the following line of code: connection = mavutil.mavlink_connection('TTYACM0', baud=9600)
  3. Replace 'TTYACM0' with the identified port name (e.g., COM3)
4. Navigate to the repository:
  1. `cd path/to/your/desired/directory`
5. Execute the Script: `python3 Car_works_5_29_24.py`



