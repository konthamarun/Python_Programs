import json
import requests
import logging
import time
import board
import adafruit_tmp117
from adafruit_tmp117 import TMP117, AlertMode, AverageCount, MeasurementDelay
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import gmtime, strftime

i2c = board.I2C()  # uses board.SCL and board.SDA
print("-" * 40)

tmp117 = TMP117(i2c)
print(type(tmp117.serial_number))
print("HEX :", hex(tmp117.serial_number))
print("-" * 40)
tmp117.initialize()
# tmp117 = adafruit_tmp117.TMP117(i2c)
tmp117.high_limit = 25
tmp117.low_limit = 10

print("\nHigh limit", tmp117.high_limit)
print("Low limit", tmp117.low_limit)

# Try changing `alert_mode`  to see how it modifies the behavior of the alerts.
# tmp117.alert_mode = AlertMode.WINDOW #default
tmp117.alert_mode = AlertMode.HYSTERESIS

# Configure logging
# logger.setLevel(logging.DEBUG)
# streamHandler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# streamHandler.setFormatter(formatter)
# logger.addHandler(streamHandler)
print("Alert mode:", AlertMode.string[tmp117.alert_mode])
# print("\n\n")

# uncomment different options below to see how it affects the reported temperature
# tmp117.averaged_measurements = AverageCount.AVERAGE_1X
# tmp117.averaged_measurements = AverageCount.AVERAGE_8X
tmp117.averaged_measurements = AverageCount.AVERAGE_32X
# tmp117.averaged_measurements = AverageCount.AVERAGE_64X

tmp117.measurement_delay = MeasurementDelay.DELAY_0_0015_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_0_125_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_0_250_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_0_500_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_1_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_4_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_8_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_16_S
print("Number of averaged samples per measurement:",
      AverageCount.string[tmp117.averaged_measurements],
      )

print(
    "Minimum time between measurements:",
    MeasurementDelay.string[tmp117.measurement_delay],
    "seconds",
)
print(
    "Reads should take approximately",
    AverageCount.string[tmp117.averaged_measurements] * 0.0155,
    "seconds",
)

print("Single measurement: %.2f degrees C" % tmp117.take_single_measurement())

# print("")
print("-" * 40)

myMQTTClient = AWSIoTMQTTClient(
    "Demo")  # random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("aqcelbe7q0lkr-ats.iot.ap-northeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/aws-raspberrypi-main/AmazonRootCA1.pem",
                                  "/home/pi/aws-raspberrypi-main/57a2ff6cec46d7d8bf139967f09a0157b2bc5dad1edc519a284aa914b5820bc8-private.pem.key",
                                  "/home/pi/aws-raspberrypi-main/57a2ff6cec46d7d8bf139967f09a0157b2bc5dad1edc519a284aa914b5820bc8-certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
print('Initiating Realtime Data Transfer From Raspberry Pi...')
connected = False
try:
    connected = myMQTTClient.connect()
    # logger.debug("MQTT client connected")
except connectTimeoutException:
    print("Error in connect!")
print("-" * 40)


# time.sleep(10)
def write_temp(temp):
    with open("/home/pi/aws-raspberrypi-main/temp.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"), temp))


def readTempF(temp):
    return (temp * 9 / 5) + 32


def readTempK(temp):
    return temp + 273.15


def loop():
    while connected:
        print("-" * 40)
        print("Temperature: %.2f degrees C" % tmp117.temperature)
        print("Single measurement: %.2f degrees C" % tmp117.averaged_measurements)
        print("Single measurement: %.2f degrees C" % tmp117.take_single_measurement())

        tempF = readTempF(tmp117.temperature)  # Farenheit
        tempK = readTempK(tmp117.temperature)  # Kelvin
        TempC = tmp117.temperature
        # fahrenheit = tmp117.temperature * 1.8 + 32
        print("Sending fahrenheit: ", tempF)
        print("Sending Kelvin: ", tempK)
        alert_status = tmp117.alert_status
        print("Sending alert_status: ", alert_status)
        # print("High alert:", alert_status.high_alert)
        # print("Low alert:", alert_status.low_alert)

        write_temp(TempC)
        # graph(temp)
        # plt.pause(1)
        # logger.debug('This is an info message')
        data = "{} [{}]".format("TempC", TempC)
        message = {"TempC": TempC}
        myMQTTClient.publish(topic="Raspberrypi",QoS=1,payload=json.dumps(message))


        # logger.debug("Sending Temperature: ".format(strftime("%Y-%m-%d %H:%M:%S"),str(TempC)))
        # myMQTTClient.publish(
        #   topic="Raspberrypi",
        #  QoS=1,
        # payload='{"tempF":"'+str(tempF)+'"}')
        # logger.debug("Sending Temperature: ".format(strftime("%Y-%m-%d %H:%M:%S"),str(tempF)))
        # myMQTTClient.publish(
        #   topic="Raspberrypi",
        #  QoS=1,
        # payload='{"tempK":"'+str(tempK)+'"}')
        # logger.debug("Sending Temperature: ".format(strftime("%Y-%m-%d %H:%M:%S"),str(tempK)))
        time.sleep(2)


if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        pass
