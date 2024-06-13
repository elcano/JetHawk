# JetHawk
Code on Jetson Nano and Pixhawk to direct vehicle to waypoints

June 12th, 2024

The Jetson Nano computes the course to the next waypoint and communicates that information over a CAN link to the Drive-By-Wire computer.
https://www.elcanoproject.org/wiki/Communication

# Overview
Jetson Nano: The Jetson Nano is a small, powerful computer made by Nvidia designed for artificial intelligence (AI) and embedded applications at the edge of a network. In simpler terms, it's a tiny computer with a lot of processing power specifically suited for running AI tasks on devices, rather than relying on a connection to the cloud for processing.

Pixhawk: Pixhawk is an open-source hardware project that designs and produces flight controllers for drones and other unmanned aerial vehicles (UAVs). It provides the hardware and software needed to control and navigate these devices, integrating sensors, communication modules, and processors to ensure stable flight and autonomous operations.

In this project, the Pixhawk serves as a device that retrieves data to be processed by the Jetson Nano. The specific data obtained includes:
1. Pitch: Pitch refers to the rotation around the lateral (side-to-side) axis of the vehicle.
2. Roll: Roll refers to the rotation around the longitudinal (front-to-back) axis of the vehicle.
3. Yaw: Yaw refers to the rotation around the vertical (up-and-down) axis of the vehicle.
4. Longitude
5. Latitude

To execute this project, you'll need several Python libraries, including:
pymavlink: Install this on your computer if you haven't already by running `pip install pymavlink`
