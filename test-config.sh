docker exec -ti home-assistant bash -c 'pip3 install --no-cache-dir pyaes ; pip3 install --no-cache-dir nefit-client ; python -m homeassistant --script check_config -c /config'
