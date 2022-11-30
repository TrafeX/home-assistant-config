Home Assistant configuration
============================

Features
--------
Some of the things I've implemented:

* Alarm system which sends snapshots of the camera's when motion is detected
* Ability to disarm the alarm via Telegram actions
* Fully automated living lights
* Automated hallway lights which dim at night
* Notify when washing machine or wash dryer is finished
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

![Home Assistant dashboard](https://timdepater.com/projects/home-assistant-1.png "Home Assistant dashboard")

Hardware
--------

The following hardware is integrated in this system.

| Quantity | Type          | Brand                                 | Protocol |
| -------- | ------------- | ------------------------------------- | -------- |
| 1        | Controller    | Aeon Labs z-stick gen5+               | zwave    |
| 5        | Dimmer        | Fibaro dimmer 500w (FGD-211)          | zwave    |
| 3        | Dimmer        | Fibaro dimmer 2 250watt (FGD-212)     | zwave    |
| 1        | Wallplug      | Aeon Labs Inline Smart Energy         | zwave    |
| 2        | Wallplug      | Greenwave Powernode-1                 | zwave    |
| 1        | Wallplug      | TBK Home                              | zwave    |
| 3        | Smoke sensor  | Fibaro Smoke sensor (FGSS001)         | zwave    |
| 1        | CO sensor     | Fibaro CO sensor (FGCD001)            | zwave    |
| 1        | Insertmodule  | Philiotech 2x1,5kw (PAN04)            | zwave    |
| 1        | Insertmodule  | Fibaro insertmodule 2x1,5kw (FGS-222) | zwave    |
| 5        | Multisensor   | Aeon Labs Multisensor 6               | zwave    |
| 2        | Door sensor   | Sensative Strips Guard                | zwave    |
| 1        | Motion sensor | Neo Coolcam motion sensor             | zwave    |
| 1        | Weather       | Netatmo Weatherstation                | wifi     |
| 2        | Weather       | Netatmo extension module              | wifi     |
| 1        | Thermostat    | Nefit Easy                            | wifi     |
| 6        | Camera        | Foscam, D-Link, Xiaomi                | wifi     |
| 1        | Doorbell      | Ring video doorbell                   | wifi     |
| 1        | Assistant     | Google Home Mini                      | wifi     |
| 1        | Assistant     | Google Nest Mini                      | wifi     |
| 2        | Assistant     | Google Nest Hub                       | wifi     |
| 1        | Led strip     | Homeylux led strip RGBWW 5 meter      | wifi     |
| 4        | Multisensor   | Tuya temperature & humidity sensors   | wifi     |
