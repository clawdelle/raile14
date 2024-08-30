# Datei Lok-mp-1.py
import network
from machine import Pin, PWM
import time
from umqtt.simple import MQTTClient

led_r = Pin(14, Pin.OUT)
led_g = Pin(12, Pin.OUT)
led_b = Pin(13, Pin.OUT)


#clear LED
led_r.value(1)
led_g.value(1)
led_b.value(1)

motor_a = PWM(Pin(4), freq=1000)
motor_b = PWM(Pin(5), freq=1000)

# Fill in your WiFi network name (ssid) and password here:
wifi_ssid = "ZentralWLAN"
wifi_password = "romanoffromanoff"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

# Fill in your  Authentication and Feed MQTT Topic details
mqtt_host = "192.168.178.79"
mqtt_username = "mqttuser"  # Your Adafruit IO username
mqtt_password = "hopess"  # Adafruit IO Key
mqtt_publish_topic = "railbrick"  # The MQTT topic for your Adafruit IO Feed
mqtt_receive_topic = "raile14/brick1"  # The MQTT topic for your Adafruit IO Feed
mqtt_port=1883

# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "brick1"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        port=mqtt_port,
        user=mqtt_username,
        password=mqtt_password)

# So that we can respond to messages on an MQTT topic, we need a callback
# function that will handle the messages.
def mqtt_subscription_callback(topic, message):
    print (f'Topic {topic} received message {message}')  # Debug print out of what was received over MQTT
    if message == b'on':
        print("LED ON")
        led.value(1)
    elif message == b'off':
        print("LED OFF")
        led.value(0)
    if message == b'stufe1':
        # turn on motor
        motor_b.duty_u16(0)
        motor_a.duty_u16(27000)  # speed(0-65535)
    if message == b'stufe2':
        # turn on motor
        motor_b.duty_u16(0)
        motor_a.duty_u16(30000)  # speed(0-65535)
    if message == b'stufe3':
        # turn on motor
        motor_b.duty_u16(0)
        motor_a.duty_u16(40000)  # speed(0-65535)
    if message == b'stufe4':
        # turn on motor
        motor_b.duty_u16(0)
        motor_a.duty_u16(65000)  # speed(0-65535)
        
    if message == b'rueckwaerts':
        rueckwaerts=True
        led_r.value(1)
        led_g.value(0)
        led_b.value(0)

# Before connecting, tell the MQTT client to use the callback
mqtt_client.set_callback(mqtt_subscription_callback)
mqtt_client.connect()

# Once connected, subscribe to the MQTT topic
mqtt_client.subscribe(mqtt_receive_topic)
print("Connected and subscribed")


rueckwaerts=False

try:
    while True:
        # Infinitely wait for messages on the topic.
        # Note wait_msg() is a blocking call, if you're doing multiple things
        # on the Pico you may want to look at putting this on another thread.
        print(f'Waiting for messages on {mqtt_receive_topic}')
        mqtt_client.wait_msg()      
                    
except Exception as e:
    print(f'Failed to wait for MQTT messages: {e}')
finally:
    mqtt_client.disconnect()
    # turn off motor
    motor_a.duty_u16(0)
    motor_b.duty_u16(0)



