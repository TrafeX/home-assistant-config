#!/usr/bin/env bash
kubectx raspberry01

tar cf - configuration.yaml secrets.yaml hass_sa.json ui-lovelace.yaml www/ configuration/ custom_components/ \
    | kubectl exec -i -n homeassistant homeassistant-0 -- tar xf - -C /config
echo "Done."