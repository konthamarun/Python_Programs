import time
import board
from adafruit_tmp117 import TMP117, AlertMode


import smbus
import time

address = 0x48
print("i2c connection Established ")
bus = smbus.SMBus(1)
print("i2c connection Established ")
while True:
    print("i2c connection Established ")
    bus.(address,0xEF)
    time.sleep(0.5)
    bus.write_byte(address,0xFF)
time.sleep(0.5)
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

tmp117 = TMP117(i2c, 0x48)

tmp117.high_limit = 25
tmp117.low_limit = 10
tmp117.

print("\nHigh limit", tmp117.high_limit)
print("Low limit", tmp117.low_limit)

# Try changing `alert_mode`  to see how it modifies the behavior of the alerts.
tmp117.alert_mode = AlertMode.WINDOW #default
tmp117.alert_mode = AlertMode.HYSTERESIS

print("Alert mode:", AlertMode.string[tmp117.alert_mode])
print("\n\n")
while True:
    print("Temperature: %.2f degrees C" % tmp117.temperature)
    alert_status = tmp117.alert_status
    print("High alert:", alert_status.high_alert)
    print("Low alert:", alert_status.low_alert)
    print("")
    time.sleep(1)
