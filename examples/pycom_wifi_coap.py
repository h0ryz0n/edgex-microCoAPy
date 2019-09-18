from network import WLAN
import machine
import microcoapy.microcoapy as microcoapy

wlan = WLAN(mode=WLAN.STA)

_MY_SSID = 'myssid'
_MY_PASS = 'mypass'
_SERVER_IP = '192.168.1.2'
_SERVER_PORT = 5683  # default CoAP port
_COAP_URL = 'to/a/path'


def connectToWiFi():
    nets = wlan.scan()
    for net in nets:
        if net.ssid == _MY_SSID:
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, _MY_PASS), timeout=5000)
            while not wlan.isconnected():
                machine.idle()  # save power while waiting
            print('WLAN connection succeeded!')
            break

    return wlan.isconnected()


def receivedMessageCallback(packet, sender):
        print('Message received:', packet, ', from: ', sender)


connectToWiFi()

client = microcoapy.Coap()
# setup callback for incoming respose to a request
client.resposeCallback = receivedMessageCallback

# Starting CoAP...
client.start()

# About to post message...
bytesTransferred = client.post(_SERVER_IP, _SERVER_PORT, _COAP_URL, "test",
                               None, microcoapy.COAP_CONTENT_TYPE.COAP_TEXT_PLAIN)
print("Sent bytes: ", bytesTransferred)

# wait for respose to our request for 2 seconds
client.poll(2000)

# stop CoAP
client.stop()
