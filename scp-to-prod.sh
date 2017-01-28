#!/usr/bin/env bash
scp -r test-config.sh configuration.yaml secrets.yaml configuration/ ha-server:/data/homeassistant
