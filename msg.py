import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json as js
import time
client = mqtt.Client()
# Keep in mind the correct ip address
MQTT_SERVER = "192.168.137.110"
MQTT_PATH = "broadcast"
#MQTT_PATH = "clap_detected"
#MQTT_PATH = "b8:27:eb:20:2f:22"
#MQTT_PATH = "B8:27:EB:DF:D0:DD/sound"

soundValue = 0
registry = {}
addressList = []
proxRegis = {}
current_3audioReadings = {}
info = {'device_id':'B8:27:EB:DF:D0:78','sensors':['Gate','Envelope','Audio']}
#info = {'device_id':'B8:27:EB:DF:D0:78','sensors':['Gate':'d','Envelope':'d','Audio':'d']}
#info = {'device_id':'b8:27:eb:20:2f:74','sensors':['Temperature', 'Audio', 'Gate', 'Envelope', 'Humidity', 'Light']}
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    client.subscribe(MQTT_PATH)
    
    message_sent_State = True
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

    soundValue = 34
    gateValue = 1
    auidoValue = 560
    

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

