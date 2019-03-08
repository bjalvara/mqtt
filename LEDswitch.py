#import the paho module
import paho.mqtt.client as mqtt
#rasberry pi IO
import RPi.GPIO as GPIO
# define our server and Channel name:
MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"

#setup LED
ledGPIOnum = 26 #pin number on PI
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledGPIOnum,GPIO.OUT)
client = mqtt.Client()

# The callback for when the client receives a CONNACK
# response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))

    # Subscribing in on_connect() means that if we lose connection and
    # reconnect then subscription will be renewed
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is recived form the server
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if str(msg.payload) == "LED on":
        GPIO.output(ledGPIOnum,GPIO.HIGH)
    elif str(msg.payload) == "LED off":
        GPIO.output(ledGPIOnum,GPIO.low)

client.on_connect = on_connect
client.subscribe(MQTT_PATH)
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

