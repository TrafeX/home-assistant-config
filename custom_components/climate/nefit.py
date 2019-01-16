"""
Nefit thermostat.
Tested with Junkers CT100

Based on nefit-client-python
https://github.com/patvdleer/nefit-client-python
"""

REQUIREMENTS = ['nefit-client']

import logging
from datetime import timedelta
import math
#import asyncio
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.components.climate import ( ClimateDevice, PLATFORM_SCHEMA,
    STATE_AUTO, STATE_HEAT, STATE_IDLE,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_OPERATION_MODE )
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
from homeassistant.const import STATE_UNKNOWN, EVENT_HOMEASSISTANT_STOP

from nefit import NefitClient

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE)

CONF_NAME = "name"
CONF_SERIAL = "serial"
CONF_ACCESSKEY = "accesskey"
CONF_PASSWORD = "password"

STATE_HOTWATER = "hot water"
STATE_MANUAL = "manual"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_SERIAL): cv.string,
    vol.Required(CONF_ACCESSKEY): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Nefit thermostat."""
    name = config.get(CONF_NAME)
    serial = config.get(CONF_SERIAL)
    accesskey = config.get(CONF_ACCESSKEY)
    password = config.get(CONF_PASSWORD)

    add_devices([NefitThermostat(
        hass, name, serial, accesskey, password)], True)


class NefitThermostat(ClimateDevice):
    """Representation of a NefitThermostat device."""

    def __init__(self, hass, name, serial, accesskey, password):
        """Initialize the thermostat."""
        self.hass = hass
        self._name = name
        self._serial = serial
        self._accesskey = accesskey
        self._password = password
        self._unit_of_measurement = TEMP_CELSIUS
        self._data = {}
        self._attributes = {}
        self._attributes["connection_error_count"] = 0
        self.override_target_temp = False
        self.new_target_temp = 0

        _LOGGER.debug("Constructor for {} called.".format(self._name))

        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP,
                             self._shutdown)

        self._client = NefitClient(serial_number=self._serial,
                             access_key=self._accesskey,
                             password=self._password)
        self._client.connect()



    @property
    def name(self):
        """Return the name of the ClimateDevice."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def operation_list(self):
        """List of available operation modes."""
        return [STATE_AUTO, STATE_MANUAL]

    def update(self):
        """Get latest data"""
        _LOGGER.debug("update called.")
        errors = []

        try:
            data = self._client.get_status()
            _LOGGER.debug("update finished. result={}".format(data))

            if type(data) is dict and "user mode" in data:
                self._attributes["connection_state"] = "ok"
            else:
                self._attributes["connection_state"] = "error"
                self._attributes["connection_error_count"] += self._attributes["connection_error_count"]

            if data:
                self._data = data

            self._attributes["boiler_indicator"] = self._data.get("boiler indicator")
            self._attributes["control"] = self._data.get("control")


            r = self._client.get_year_total()
            self._attributes["year_total"] = r.get("value")
            self._attributes["year_total_unit_of_measure"] = r.get("unitOfMeasure")

            r = self._client.get("/ecus/rrc/userprogram/activeprogram")
            self._attributes["active_program"] = r.get("value")

            r = self._client.get("/ecus/rrc/dayassunday/day10/active")
            self._attributes["today_as_sunday"] = (r.get("value") == "on")

            r = self._client.get("/ecus/rrc/dayassunday/day11/active")
            self._attributes["tomorrow_as_sunday"] = (r.get("value") == "on")

            r = self._client.get("/system/appliance/systemPressure")
            self._attributes["system_pressure"] = r.get("value")

            r = self._client.get("/heatingCircuits/hc1/actualSupplyTemperature")
            self._attributes["supply_temp"] = r.get("value")

            r = self._client.get("/system/sensors/temperatures/outdoor_t1")
            self._attributes["outside_temp"] = r.get("value")
        except:
            _LOGGER.warning('Nefit api returned invalid data')

    @property
    def current_temperature(self):
        """Return the current temperature."""
        _LOGGER.debug("current_temperature called.")

        return self._data.get('in house temp', None)

    @property
    def current_operation(self):
        state = self._data.get("boiler indicator")
        if state == 'central heating':
            return STATE_HEAT
        elif state == 'hot water':
            return STATE_HOTWATER
        elif state == 'off':
            return STATE_IDLE
        else:
            return None

    @property
    def target_temperature(self):

        #update happens too fast after setting new target, so value is not changed on server yet.
        #assume for this first update that the set target was succesful
        if self.override_target_temp:
            self._target_temperature = self.new_target_temp
            self.override_target_temp = False
        else:
            self._target_temperature = self._data.get('temp setpoint', None)

        return self._target_temperature

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        try:
            temperature = kwargs.get(ATTR_TEMPERATURE)
            _LOGGER.debug("set_temperature called (temperature={}).".format(temperature))

            if temperature is None:
                return None

            self._client.set_temperature(temperature)

            self.override_target_temp = True
            self.new_target_temp = temperature

        except:
            _LOGGER.error("Error setting target temperature")

    def set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        _LOGGER.debug("set_operation_mode called mode={}.".format(operation_mode))
        if operation_mode == "manual":
            self._client.put('/heatingCircuits/hc1/usermode', {'value': 'manual'})
        else:
            self._client.put('/heatingCircuits/hc1/usermode', {'value': 'clock'})

    @property
    def device_state_attributes(self):
        """Return the device specific state attributes."""

        return self._attributes

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    def _shutdown(self, event):
        _LOGGER.debug("shutdown")
        self._client.disconnect()
