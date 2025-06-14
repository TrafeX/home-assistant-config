Home Assistant configuration
============================

Features
--------
Some of the things I've implemented:

* Alarm system which sends snapshots of the camera's when motion is detected
* Have home modes to control lighting and heating based on the alarm state
* Ability to disarm the alarm via Telegram actions
* Fully automated living lights
* Automated hallway lights which dim at night
* Notify when washing machine or wash dryer is finished, including the duration and energy usage
* Play speech messages via the Google Mini's
* Presence detection with home coming and leaving automation
* Night mode; turn the ground floor lights off and dim the hallway lights
* Integration with ZwaveJS
* Modules with ESPHome communicating via MQTT
* Enable ventilation when CO2 level reaches a certain level
* Enable ventilation when the shower is used
* Automated Christmas lights (only during the holidays 😉)
* Notify when one of the smoke sensors detects smoke
* Ghost mode; turn on lights for a short period when away to pretend someone is home
* Start the vacuum cleaner based on a schedule with the option to override per day
* Notify when the vacuum cleaner is done
* Dim the lights when the TV is turned on
* Turn the heating down when night mode is activated or leaving home
* Notify when you leave the frontdoor open
* Make my vacuum cleaner come from under the couch to be able to empty it
* Have a 'guest presence' option to override the presence detection
* Send a snapshot of the person ringing the doorbell and announce it on the Google Mini's
* DSMR integration, monitoring my energy and gas usage
* Brighten the backyard lights when motion is detected
* Notify when the powerline voltage fluctuates too much
* Cast a dashboard view of Home Assistant to Google Nest Hub
* Notify when the external IP changes
* Shutdown NAS when the UPS is running on battery for too long
* Notify when one the battery powered sensors is running low on battery
* Notify when it's time to water the plants and turn on the irrigation system
* A dashboard with graphs of all temperature, humidity and energy usage sensors
* An energy dashboard with the solar production, grid usage and house consumption
* Turn off the heating in the office when the workday is over 
* Blink the kids bedroom light when it's time to get up or go to sleep 

![Home Assistant dashboard](https://timdepater.com/projects/home-assistant-1.png "Home Assistant dashboard")

Hardware
--------

The following hardware is integrated in this system.

| Quantity | Type           | Brand                                 | Protocol |
| -------- | -------------- | ------------------------------------- | -------- |
| 1        | Controller     | Aeon Labs z-stick gen5+               | zwave    |
| 1        | Controller     | Sonoff Zigbee USB Dongle Plus         | zigbee   |
| 5        | Dimmer         | Fibaro dimmer 500w (FGD-211)          | zwave    |
| 3        | Dimmer         | Fibaro dimmer 2 250watt (FGD-212)     | zwave    |
| 1        | Wallplug       | Aeon Labs Inline Smart Energy         | zwave    |
| 2        | Wallplug       | Greenwave Powernode-1                 | zwave    |
| 1        | Wallplug       | TBK Home                              | zwave    |
| 3        | Smoke sensor   | Fibaro Smoke sensor (FGSS001)         | zwave    |
| 1        | CO sensor      | Fibaro CO sensor (FGCD001)            | zwave    |
| 1        | Insertmodule   | Philiotech 2x1,5kw (PAN04)            | zwave    |
| 1        | Insertmodule   | Fibaro insertmodule 2x1,5kw (FGS-222) | zwave    |
| 5        | Multisensor    | Aeon Labs Multisensor 6               | zwave    |
| 1        | Motion sensor  | Neo Coolcam motion sensor             | zwave    |
| 2        | Wallplug       | Qubino Smart Plug 16A                 | zwave    |
| 1        | Weather        | Netatmo Weatherstation                | wifi     |
| 2        | Weather        | Netatmo extension module              | wifi     |
| 1        | Thermostat     | Nefit Easy                            | wifi     |
| 6        | Camera         | Foscam, D-Link, Xiaomi                | wifi     |
| 1        | Doorbell       | Reolink doorbell                      | lan      |
| 1        | Assistant      | Google Home Mini                      | wifi     |
| 1        | Assistant      | Google Nest Mini                      | wifi     |
| 3        | Assistant      | Google Nest Hub                       | wifi     |
| 1        | Led strip      | Homeylux led strip RGBWW 5 meter      | wifi     |
| 4        | Multisensor    | Tuya temperature & humidity sensors   | wifi     |
| 2        | Wallplug       | Shelly Plug S                         | wifi     |
| 1        | Wallplug       | Shelly Plus Plug                      | wifi     |
| 3        | Light          | Philips Hue Lily garden spots         | zigbee   |
| 1        | Irrigation     | Woox R7060 Irrigation Control         | zigbee   |
| 4        | Wallplug       | Third Reality Smart Plug              | zigbee   |
| 1        | Insertmodule   | Shelly 2PM                            | zwave    |
| 1        | Motion sensor  | Aqara Motion Sensor P1                | zigbee   |
| 2        | Door sensor    | Aqara Door and Window sensor          | zigbee   |
| 1        | Solar Inverter | SolarEdge SE2200H                     | wifi     |
