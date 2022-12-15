import time
import paho.mqtt.client as mqtt
import ssl
import json
import thread


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem',
               certfile='./57a2ff6cec46d7d8bf139967f09a0157b2bc5dad1edc519a284aa914b5820bc8-certificate.pem.pem.crt',
               keyfile='./57a2ff6cec46d7d8bf139967f09a0157b2bc5dad1edc519a284aa914b5820bc8-private.pem.key',
               tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("aqcelbe7q0lkr-ats.iot.ap-northeast-1.amazonaws.com", 8883,
               60)  # Taken from REST API endpoint - Use your own.


def intrusionDetector(Dummy):
    while (1):
        print("Just Awesome")
        client.publish("device/data", payload="Hello TechnoHealth!!", qos=0, retain=False)
        time.sleep(5)

thread.start_new_thread(intrusionDetector, ("Create intrusion Thread",))
client.loop_forever()