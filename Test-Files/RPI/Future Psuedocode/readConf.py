import json

class Device:
    def __init__(self, name, address, channels):
        self.name = name
        self.address = address
        self.instance = Adafruit_ADS1x15.ADS1115(address=address, busnum=1)
        for channel in channels:
          self.channels.append(Channel(channel['name'], channel['pin'], channel['gain']))

    def getValues(self):
        values = []
        for channel in self.channels:
            values.append(channel.getValue())
        return values

    def serialize(self):
        print(f"{'address': {self.address}}")

class Channel:
    def __init__(self, name, pin, gain):
        self.name = name
        self.pin = pin
        self.gain = gain
        self.data_rate = -1

    def getValue(self, device):
        return device.read_adc(self.pin, self.gain, self.data_rate)


# The below is a shortcut for thie experiment
readInConfig = json.load(open('config.json'))

for device in readInConfig['devices']:
  deviceArray.append(Device(device['name'], device['address']))

# When you want to read values:
values = []

for device in deviceArray:
  values += device.getValues()

for value in values:
  print(value + ",")
