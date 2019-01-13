"""
ORIGINAL: https://github.com/marconfus/ha-nefit-ng/blob/master/nefit.py

Support for Bosch home thermostats.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/xxxxxx/
"""

REQUIREMENTS = ['aionefit==0.1']

import logging
from datetime import timedelta
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import asyncio
import concurrent

from homeassistant.components.climate import (ClimateDevice, PLATFORM_SCHEMA,
    STATE_AUTO, STATE_MANUAL,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_OPERATION_MODE)
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
from homeassistant.const import STATE_UNKNOWN, EVENT_HOMEASSISTANT_STOP

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE)

OPERATION_MANUAL = "manual"
OPERATION_AUTO = "auto"

CONF_NAME = "name"
CONF_SERIAL = "serial"
CONF_ACCESSKEY = "accesskey"
CONF_PASSWORD = "password"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_SERIAL): cv.string,
    vol.Required(CONF_ACCESSKEY): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):

    name = config.get(CONF_NAME)
    serial = config.get(CONF_SERIAL)
    accesskey = config.get(CONF_ACCESSKEY)
    password = config.get(CONF_PASSWORD)

    _LOGGER.debug("Creating device")
    device = NefitThermostat(hass, name, serial, accesskey, password)
    _LOGGER.debug("Waiting for connected event")

    try:
        await device._client.xmppclient.connected_event.wait()
    except concurrent.futures._base.TimeoutError:
        hass.services.call("persistent_notification", "create",
                           {'message': 'Could not connect to Bosch cloud.',
                           'title': 'Nefit error',
                           'notification_id': 'nefit_logon_error'})

    _LOGGER.debug("Device is ready")
    async_add_entities([device], True)

class NefitThermostat(ClimateDevice):
    """Representation of a NefitThermostat device."""

    def __init__(self, hass, name, serial, accesskey, password):
        from aionefit import NefitCore
        """Initialize the thermostat."""
        self.hass = hass
        self._name = name

        self._online = False
        self._unit_of_measurement = TEMP_CELSIUS
        self._uistatus = None
        self._attributes = {}
        self._operation_list = [OPERATION_MANUAL, OPERATION_AUTO]

        self._client = NefitCore(serial_number=serial,
                       access_key=accesskey,
                       password=password,
                       message_callback=self.parse_message)

        _LOGGER.debug("adding stop listener")
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP,
                                   self._shutdown)

    @property
    def supported_features(self):
        """Return the list of supported features.
        """
        return SUPPORT_FLAGS

    def parse_message(self, data):
        """Message received callback function for the XMPP client.
        """
        _LOGGER.debug("parse_message callback called")
        if not 'id' in data:
            _LOGGER.error("Unknown response received.")
            return

        if data['id'] == '/ecus/rrc/uiStatus':
            _LOGGER.debug('Message type uiStatus')
            self._uistatus = data['value']

    async def async_update(self):
        """Get latest data
        """
        _LOGGER.debug("async_update called")
        self._client.get('/ecus/rrc/uiStatus')

        await asyncio.wait_for(self._client.xmppclient.message_event.wait(), timeout=10.0)
        self._client.xmppclient.message_event.clear()
        _LOGGER.debug("async_update finished")

    @property
    def name(self):
        """Return the name of the ClimateDevice.
        """
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement.
        """
        return self._unit_of_measurement

    @property
    def current_temperature(self):
        """Return the current temperature.
        """
        if not self._uistatus:
            return STATE_UNKNOWN

        iht = float(self._uistatus.get('IHT'))
        _LOGGER.debug('current_temperature=%s', iht)
        return iht

    @property
    def target_temperature(self):
        if not self._uistatus:
            return STATE_UNKNOWN

        tot = float(self._uistatus.get('TOT'))
        _LOGGER.debug('target_temperature=%s', tot)
        return tot

    @property
    def operation_list(self):
        """List of available operation modes."""
        return [STATE_AUTO, STATE_MANUAL]

    @property
    def current_operation(self):
        if not self._uistatus:
            return None

        if self._uistatus['UMD'] == 'manual':
            return OPERATION_MANUAL
        elif self._uistatus['UMD'] == 'clock':
            return OPERATION_AUTO

    @property
    def device_state_attributes(self):
        """Return the device specific state attributes."""

        return self._uistatus

    async def async_set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        _LOGGER.debug("set_operation_mode called mode={}.".format(operation_mode))
        if operation_mode == "manual":
            new_mode = "manual"
        else:
            new_mode = "clock"

        self._client.set_usermode(new_mode)
        await asyncio.wait_for(self._client.xmppclient.message_event.wait(), timeout=10.0)
        self._client.xmppclient.message_event.clear()
        self._uistatus['UMD'] = new_mode

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        _LOGGER.debug("set_temperature called (temperature={}).".format(temperature))
        self._client.set_temperature(temperature)
        await asyncio.wait_for(self._client.xmppclient.message_event.wait(), timeout=10.0)
        self._client.xmppclient.message_event.clear()
        self._uistatus['TOT'] = temperature

    def _shutdown(self, event):
        _LOGGER.debug("shutdown")
        self._client.disconnect()
