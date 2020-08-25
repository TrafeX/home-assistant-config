Home Assistant configuration
============================
My Home Assistant configuration which connects to my Vera Edge to extend it's functionality.

Features
--------
Some of the things I've implemented:

* Alarm system which sends snapshots of the camera's when motion is detected
* Ability to disarm the alarm via Telegram actions
* Fully automated living lights
* Automated hallway lights which dim at night
* Notify when washing machine is finished
* Play speech messages via the Google Home
* Presence detection with home coming and leaving automation
* Night mode
* Integration with Vera Edge
* Modules with ESPHome communicating via MQTT
* Enable ventilation when CO2 level reaches a certain level
* Enable ventilation when the shower is used
* Automated Christmas lights (only during the holidays 😉)
* Notify when one of the smoke sensors detects smoke
* Ghost mode; turn on lights for a short period when away to pretend someone is home
* Notify when the vacuum cleaner is done
* Set security camera in privacy mode when at home
* Dim the lights when the TV is turned on
* Turn the heating down when night mode is activated
* Notify when you leave the frontdoor open
* Showing the health of my plants
* Make my vacuum cleaner come from under the couch to be able to empty it
* Have a 'guest presence' select input to override the presence detection
* Send a snapshot of the person ringing the doorbell
* DSMR integration, monitoring my energy and gas usage
* Notify when the wind conditions are bad and we need to close some windows
* Brighten the backyard lights when motion is detected
* Notify when the powerline voltage is fluctuation too much


![Home Assistant dashboard](https://www.trafex.nl/wp-content/uploads/2019/02/home-assistant-v2.png "Home Assistant dashboard")

Hardware
--------

The following hardware is integrated in this system.

| Quantity | Type | Brand | Protocol |
|----------|------|-------|----------|
| 1 | Controller | Vera Edge | zwave |
| 3 | Dimmer | Fibaro dimmer 500w (FGD-211) | zwave |
| 2 | Dimmer | Fibaro dimmer 2 250watt | zwave |
| 1 | Wallplug | Aeon Labs Inline Smart Energie | zwave |
| 2 | Wallplug | Greenwave Powernode-1 | zwave |
| 1 | Wallplug | TBK Home | zwave |
| 3 | Smoke sensor | Fibaro Smoke sensor (FGSS001) | zwave |
| 1 | Insertmodule | Philiotech 2x1,5kw (PAN04) | zwave |
| 1 | Insertmodule | Fibaro insertmodule 2x1,5kw (FGS-222) | zwave |
| 4 | Multisensor | Aeon Labs Multisensor 6 | zwave |
| 2 | Door sensor | Sensative Strips Guard | zwave |
| 1 | Motion sensor | Neo Coolcam motion sensor | zwave |
| 2 | Flower sensor | Xiaomi Flora | bluetooth |
| 1 | Assistant | Google Home Mini | wifi |
| 1 | Weather | Netatmo Weatherstation | wifi |
| 1 | Weather | Netatmo extension module | wifi |
| 1 | Thermostat | Nefit Easy | wifi |
| 6 | Camera | Foscam, D-Link, Xiaomi | wifi |
| 1 | Doorbell | Ring video doorbell | wifi |
| 1 | Google | Google Home Mini | wifi |
| 1 | Google | Google Nest Mini | wifi |
| 1 | Google | Google Nest Hub | wifi |
