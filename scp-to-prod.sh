#!/usr/bin/env bash
scp -r test-config.sh configuration.yaml ui-lovelace.yaml secrets.yaml hass_sa.json www/ configuration/ custom_components/ ha-server:/data/homeassistant
