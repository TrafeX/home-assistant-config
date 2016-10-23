docker run --name="home-assistant" -v "$PWD":/config -v /etc/localtime:/etc/localtime:ro --net=host homeassistant/home-assistant
