#!/usr/bin/env bash
scp -r test-config.sh configuration.yaml secrets.yaml hass_sa.json ui-lovelace.yaml www/ configuration/ custom_components/ ha-server:/data/homeassistant
