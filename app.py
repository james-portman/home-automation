import redis
from flask import Flask, render_template
import json
app = Flask(__name__)


r = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_devices():
    device_keys = r.keys('R*D*')
    devices = {}
    for device in device_keys:
        try:
            devices[device] = r.get(device)
        except:
            devices[device] = None
    return devices

@app.route('/devices.json')
def route_devices_json():
    return json.dumps(get_devices())

@app.route('/')
def route_slash():
    return render_template('slash.html', devices=get_devices())

app.run(debug=True)

# TODO: some way of storing device info in redis?
# if it's a dimmer, switch, radiator etc?
# friendly name rather than R1D2 etc
# then can decide what to show next to things in the UI
# could do with dragging it all in before returning from get_devices()
