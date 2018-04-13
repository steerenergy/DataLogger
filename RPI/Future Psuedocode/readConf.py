class Device:
    name = ""
    address = ""
    channels = [] # Array of instances of Channel
    instance = NULL

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.instance = Adafruit_ADS1x15.ADS1115(address=address, busnum=1)

    def getValues(self):
        values = []
        for channel in channels:
            values.append(channel.getValue())
        return values

#    def serialize(self):
#        print(f"{'address': {self.address}}")

class Channel:
    def __init__(self, name, pin, gain):
        self.name = name
        self.pin = pin
        self.gain = gain
        self.data_rate = -1

    def getValue(self, device):
        self.stupid_variable = 34;
        return device.read_adc(self.pin, self.gain, self.data_rate)


readInConfig = readConfig()

deviceList = []

for device in readInConfig['devices']:
  deviceList.append(Device())
