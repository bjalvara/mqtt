#path
Documents\GitHub\mqtt
.\.venvs\ECE140_venv\Scripts\activate

#MQTT https://www.eclipse.org/paho/clients/python/docs/

#subscribe
mosquitto_sub -h localhost -v -t test_channel

#publish
mosquitto_pub -h localhost -t test_channeln-m ""

#Callbacks will be called to allow the application to prosses
events as necessary

#Constructor/reinitialise
Client(client_id="", clean_session=True, userdata=None, protocol=MQTTV311, transport="tcp"
)
#client_id: the unique client id string used when connecting to the broker. If client_id is zero lenght or none, then one will be randomly generated. In this case the clean_session parameter must be True

#clean_session: a boolean that determines the client type. If Ture, the broker will remove all information about this client when it disconnects. If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.

#userdata: user defined data of any type that is passed as the userdata parameter to callbacks. It may be updated at a later point with the user_data_set() funtion.

#protocol: the version of the MQTT protocol to use for this client. Can be either MQTTv31 or MQTTv311

#transport set to "websocks" to send MQTT over WebSockets. Leave at the default of "tcp" to use raw TCP

#constructor example
import paho.mqtt.client as mqtt
mqttc = mqtt.Client()

#reinitialise()
reinitialise(client_id="", clean_session=True, userdata=None)
#the reinitialise() function resets the client to its starting state as if it had just been created.

#option functions
#These fucntions represent options that can be set on the client to modify its behavior. In the majority of cases this must be done BEFORE connecting to a broker

max_inflight_messages_set(self, inflight)
#set the maximum number of messages with QoS>0 that can be part way through thier network flow at once
#Defaults to 20. Increasing this value will consume more memory but can increase throughput/

max_queued_messages_set(self, queue_size)
#set the maximum number of outgoing messages with QoS>0 that can be pending in the outgoing message queue.
# Defaults to 0.0 means unlimited. When the queue is full, any further outgoing messages woild be dropped

message_retry_set(retry)
#set the time in seconds before a message with QoS>0 is retried, if the broker does not respond.
#This is set to 5 seconds b default and should not normally need changing.

ws_set_options(self, path="/mqtt", headers=None)
#set the websockets connection option. These options will only be used if transport="websockets" was passed into the Client() constructor.

tls_set(ca_certs=None, cerfile=None, keyfile=None, cert=reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
#Configure network encryption and authentication options. Enables SSL/TLS support

username_pw_set(suername, password=None)
#Set a username and optionally a password for broker authentication. Must be called before connect*()

user_data_set(userdata)
#set the private user data that will be passed to callbacks when events are generated. Use this for your own purpose to support your application

will_set(topic, paload=None, qos=0, retain=False)
#set a Will to be sent to the broker. If the client disconnects without calling disconnect(), the broker will publish the message on its behalf
#topic: the topic that the will messgae should be published on
#payload: the massage to send as a will. If not given or set to None a zero lenght message will be used as the will. Passing an int of float will result in the payload being converted to a string representing that number. If you wish to send a true int/float, use struct.pack() to create the payload your require
#qos: the quality of service level to use for the will.
#retain:if set to True, the will message will be set as the "last known good"/retained message for the topic.
#Raises a ValueError if qos is not 0, 1 or 2, or if topic is None or has zero string length

reconnect_delay_set(min_delay=1, max_delay=120)
#The client will automatically retry connection. Between each attempt it will wait a number of seconds between min_delay and max_delay.

#Connect/reconnect/disconnect
connect(host, port=1883, keepalive=60, bind_address="")
#The connect() function connects the client to a broker. This is a blocking function. It takes the following arguments:
#host: the hostname or IP address of the remote broker
#port: the network port of the server host to connect to. Defaults to 1883.
# keepalive: maximum period in seconds allowed between communications with the broker. If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker
#blind_address: the IP address of a local network interface to bind this client to, assuming multiple interfaces exist

#callback