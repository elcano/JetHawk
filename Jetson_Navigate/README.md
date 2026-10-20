# Jetson_Navigate

CAN waypoint-navigation node for the Jetson Nano. It reads the vehicle's
position and heading from CAN, steers toward each waypoint, and sends drive
commands to the [V5 Drive-by-Wire](https://github.com/elcano/V5_Drive-by-wire)
(DBW) firmware.

It was tested with the [Bridge](https://github.com/elcano/Bridge) closed-loop
simulator, where the Router board simulated the trike. The simulated trike
reached all four waypoints and stopped.

## How it works (10 Hz loop)

1. Converts the waypoints from latitude/longitude to a flat east/north frame
   in centimeters, with waypoint 0 as the origin.
2. Computes the distance and bearing to the active waypoint, then steers in
   proportion to the heading error, capped at ±30°.
3. Moves to the next waypoint within 300 cm; stops and brakes after the last one.
4. On Ctrl-C, sends brake on, speed 0, and e-stop before exiting.

Until the first position message arrives, it commands speed 0 with brakes on.

## CAN messages

| Direction | ID | Name | Content | Source in simulation |
|---|---|---|---|---|
| In  | `0x4C0` | VehiclePosition | east_cm, north_cm (int32 LE) | Router |
| In  | `0x4E0` | VehicleHeading  | heading_centiDeg (uint16 LE, 0 = N, +CW) | Router |
| In  | `0x4F0` | VehicleSpeed    | speed_cmPs (int16 LE) | Router |
| In  | `0x400` | Actual          | actual steering angle, DegX10 | DBW |
| Out | `0x350` | NavDrive        | speed_cmPs, brake, angle_DegX10 (int16 LE) | to DBW |
| Out | `0x100` | NavStatus       | 0x40 autonomous, 0x80 e-stop | to DBW |
| Out | `0x101` | GoalReached     | waypoint index; 0x80 when mission complete | to DBW |

## Setup

- Jetson Nano with JetPack 4.x (Python 3.6).
- USB-CAN adapter supported by SocketCAN, such as CANable or Innomaker USB2CAN,
  connected to the DBW CAN bus at 500 kbps.

```bash
sudo ip link set up can0 type can bitrate 500000
pip3 install -r requirements.txt
python3 jetson_navigate.py   # defaults: --channel can0 --bustype socketcan --bitrate 500000
```

Cruise speed, steering gain, capture radius, maximum steering angle, and
waypoints are set at the top of `jetson_navigate.py`.

## Running on the real trike

In simulation, the Router board sent the position, heading, and speed messages.
On the real trike, another source must send them. The Pixhawk already used in
JetHawk can provide this data.

### Input requirements

| Message | Requirement |
|---|---|
| `0x4C0` position | East/north in cm **relative to waypoint 0** (`WAYPOINTS[0]`), not relative to the starting position. Use the same conversion as `latlon_to_cm()`. Send only with a valid GPS fix. |
| `0x4E0` heading | Centidegrees, 0–35999, 0 = north, clockwise positive, referenced to true north. |
| `0x4F0` speed | cm/s. Currently used only for status messages. |
| Update rate | At least 10 Hz, matching the navigation loop. |

### Getting the inputs from the Pixhawk

The MAVLink `GLOBAL_POSITION_INT` message provides most of what is needed:

- `lat`, `lon`: degrees × 10⁷. Convert to east/north cm from waypoint 0.
- `hdg`: heading in centidegrees, 0–35999, or 65535 when unknown. This matches
  `0x4E0` directly.
- `vx`, `vy`: velocity in cm/s. Speed is `sqrt(vx² + vy²)`.

Check `GPS_RAW_INT.fix_type` for a 3D fix (3 or higher) before sending position.
Confirm the Pixhawk compass is calibrated so its heading is referenced to true
north.

The existing `Car_works_5_29_24.py` reads `ATTITUDE.yaw` (radians, −π to π) and
`GPS_RAW_INT`, and measures position from where it started. Those values need
converting before they can be sent as `0x4C0`/`0x4E0`.

There are two ways to connect them:

1. **Pixhawk-to-CAN publisher (recommended):** a separate script reads the
   Pixhawk and sends `0x4C0`, `0x4E0`, and `0x4F0`. `jetson_navigate.py` stays
   unchanged and can still be tested with the Bridge simulator. Do not run the
   Router simulator on the same bus.
2. **Read the Pixhawk directly:** change `jetson_navigate.py` to read MAVLink
   with `pymavlink` instead of the CAN position, heading, and speed messages.

### Gaps to address before driving the real trike

- **No stale-data timeout.** After the first position message, the script keeps
  driving on the last received position and heading, even if updates stop. It
  should brake when position or heading data is too old.
- **Heading defaults to north.** If position arrives before heading, the script
  steers as if facing north. It should wait for both.
- **Test waypoints.** The waypoints are a ~20 m test loop near UW Bothell.
  Replace them with the real course.
- **Tuning.** Steering is proportional to heading error only; gain, cruise speed,
  and capture radius need tuning on the real trike.
