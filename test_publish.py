import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

import json as js
client = mqtt.Client()
# Keep in mind the correct ip address
MQTT_SERVER = "192.168.137.110"
MQTT_PATH = "broadcast"
#MQTT_PATH = "clap_detected"
#MQTT_PATH = "b8:27:eb:20:2f:22"
#MQTT_PATH = "B8:27:EB:DF:D0:DD/sound"

info = {'device_id':'B8:27:EB:DF:D0:78','sensors':['Gate','Envelope','Audio']}
#info = {'device_id':'B8:27:EB:DF:D0:78','sensors':['Gate':'d','Envelope':'d','Audio':'d']}
#info = {'device_id':'b8:27:eb:20:2f:74','sensors':['Temperature', 'Audio', 'Gate', 'Envelope', 'Humidity', 'Light']}

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
    publish.single(MQTT_PATH, js.dumps(info), hostname=MQTT_SERVER)

def on_message_Sound(client, userdata, msg):
    listVal = {}
    print("sound callback")
    try:
        input_data = js.loads(msg.payload)
    except:
        print("load failed")

    #give data to request portion
    print(str(input_data))
    #for sensor in input_data['sensors']:
    listVal['Envelope'] = 400
    client.publish(input_data['device_id']+'/sound', js.dumps(listVal))
    


client.on_connect = on_connect

client.message_callback_add("B8:27:EB:DF:D0:DD/sound", on_message_Sound)
client.message_callback_add("clap_detected", on_message_Sound)
client.connect(MQTT_SERVER, 1883, 60)
try:
    client.publish(MQTT_PATH, js.dumps(info, sort_keys=True))
except:
    print("Did not publish")
client.loop_forever()
