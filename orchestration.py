#rasberry pi IO
import RPi.GPIO as GPIO
#MCP3008 IO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
#MCP3008 setting up
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


#setup LED
ledGPIOnum = 26 #pin number on PI
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledGPIOnum,GPIO.OUT)
LEDstate = 0
#setup MCP print
soundChannelPin = 4
gateChannelPin = 1
audioChannelPin = 3
#pin channels
#gate = 1
#light = 2
#audio = 3
#envelope = 4




import paho.mqtt.client as mqtt
import json as js
import time

#import nearby devices
import proximity as prox


#MQTT_SERVER = "localhost"
#MQTT_SERVER = "iot.eclipse.org"
#MQTT_SERVER = "100.80.241.236"
MQTT_SERVER = "192.168.137.110"
MQTT_PATH = "broadcast"

soundValue = 0
registry = {}
addressList = []
proxRegis = {}
current_3audioReadings = {}

info = {'device_id':'B8:27:EB:DF:DO:DD','sensors':['Temperature', 'Audio', 'Gate', 'Envelope', 'Humidity', 'Light']}


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and

    #-- Finds Broadcast and Sends Data to other devices on Broadcast --#
    #if (message_sent_State  == False):
    client.subscribe(MQTT_PATH)
    #client.publish(MQTT_PATH, js.dumps(info, sort_keys=True))
    message_sent_State = True
    #client.publish(MQTT_PATH, "HMM")
    #print(js.dumps(info, sort_keys=True))

    #-- Listens for response --#
    client.subscribe(info['device_id'])
    client.subscribe(info['device_id']+'/sound')
def on_disconnect(client, userdata, msg):
    message_sent_State = False

# Callback when message is recieved.
def on_message(client, userdata, msg):
    global registry,proxRegis
    print(msg.topic+" "+str(msg.payload))



    #parse and save
    #if (msg.topic != info['device_id']):
    try:
        input_data = js.loads(msg.payload)
    except:
        print("load failed")

    print(input_data)
    registry[input_data['device_id']] = input_data['sensors']
    print(input_data['device_id'])
    #publish directly to new id
    client.publish(input_data['device_id'],js.dumps(info))
    addressList = prox.proximity()
    if input_data['device_id'] in addressList:
        proxRegis[input_data['device_id']] = True

    else:
        proxRegis[input_data['device_id']] = False
    print("List if nearby devices \n")
    print(js.dumps(proxRegis, indent=4))


def on_message_Sound(client, userdata, msg):
    global registry,proxRegis,current_3audioReadings,LEDstate
    listVal = {}
    print("sound callback")
    try:
        input_data = js.loads(msg.payload)
    except:
        print("load failed")
    #give data to request portion
    if 'device_id' in input_data:
        print("DEVICE ID")
        #for sensor in input_data['sensors']:
        listVal['Envelope'] = soundValue
        client.publish(input_data['device_id']+'/sound', js.dumps(listVal))
    #take data and compare it to ourvalues
    else:
        print("Soundvalue on Callback" + str(current_3audioReadings['Envelope']))
        if int(input_data['Envelope']) > int(current_3audioReadings['Envelope']):
            print("DATA")
            if LEDstate == 1:
                GPIO.output(ledGPIOnum,GPIO.LOW)
                LEDstate = 0
            if LEDstate == 0:
                GPIO.output(ledGPIOnum,GPIO.HIGH)
                LEDstate = 1

#this portion is just a on_message_Sound(Request portion of Code used to
#Colaborate with Matt's Group)
def on_message_clap_detected(client,userdata,msg):
    #callback function takes request from specific pi with device_id and
    #gives back our sound data to clap_response+device_id

    #Assumes they give the device_id
    global current_3audioReadings,LEDstate
    listVal = {}
    print("clap_detected request callback")
    try:
        input_data = js.loads(msg.payload)
    except:
        print("load failed")
    #iterate through values needed, find if a list of sensors exists
    if 'sensors' in input_data:
        for sensors in input_data['sensors']:
            if sensors in current_3audioReadings:
                listVal[sensors] = current_3audioReadings[sensors]
    #if the sensor wanted is empty assume they want at least one sound value
    else:
        listVal['Envelope'] = current_3audioReadings['Envelope'] #envelope value
        listVal['Gate'] = current_3audioReadings['Gate'] #envelope value
        listVal['Audio'] = current_3audioReadings['Audio'] #envelope value

    client.publish('clap_response'+input_data['device_id'], js.dumps(listVal))



client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_disonnect = on_disconnect
client.message_callback_add("B8:27:EB:DF:D0:DD/sound", on_message_Sound)
client.message_callback_add("clap_detected", on_message_Sound)

client.connect(MQTT_SERVER, 1883, 60)

try:
    client.publish(MQTT_PATH, js.dumps(info, sort_keys=True))
except:
    print("Did not publish")


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
soundValue = 0
LEDstate = 0
prevsoundValue = 0
client.loop_start()
while True:

    soundValue = mcp.read_adc(soundChannelPin)#same as envelope
    gateValue = mcp.read_adc(gateChannelPin)
    auidoValue = mcp.read_adc(audioChannelPin)
    if gateValue >= 600:
        time.sleep(.2)
        print("made it")
        current_3audioReadings['Gate'] = gateValue
        current_3audioReadings['Audio'] = auidoValue
        current_3audioReadings['Envelope'] = soundValue #envelope value

        current_soundValue = soundValue

        if LEDstate == 1:
            GPIO.output(ledGPIOnum,GPIO.LOW)
            LEDstate = 0
        if LEDstate == 0:
            GPIO.output(ledGPIOnum,GPIO.HIGH)
            LEDstate = 1

        #send to all connected devices
        wanted_info = {'device_id':'B8:27:EB:DF:D0:DD','sensors':['Gate','Envelope','Audio']}
        if proxRegis:
            for pi in proxRegis:
                #print("this is the pi:" + pi)
                if ('Envelope' in registry[pi]) and (proxRegis[pi] == True):
                    #print("This is the registry:" + str(registry[pi]))
                    client.publish(pi+'/sound', js.dumps(wanted_info))


    time.sleep(0.2)

#LED pin setup
