#!/usr/bin/env bash
scp -r test-config.sh configuration.yaml ui-lovelace.yaml secrets.yaml www/ configuration/ custom_components/ ha-server:/data/homeassistant
