import paho.mqtt.publish as publish

# Keep in mind the correct ip address
MQTT_SERVER = "192.168.137.124"
MQTT_PATH = "test_channel"


publish.single(MQTT_PATH, "LED on", hostname=MQTT_SERVER)