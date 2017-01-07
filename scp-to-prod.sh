#!/usr/bin/env bash
scp -r configuration.yaml secrets.yaml configuration/ ha-server:/data/homeassistant
