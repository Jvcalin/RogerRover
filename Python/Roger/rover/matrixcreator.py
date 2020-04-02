from matrix_lite import led, sensors
from ...common import rovercollections as collections
import time
import statistics as stat
from math import pi, sin
import json

class Motion:

    arraysize = 25

    def __init__(self):
        self.sensors = {}
        self.sensors["xAccel"] = collections.RollingArray(arraysize)  
        self.sensors["yAccel"] = collections.RollingArray(arraysize)  
        self.sensors["zAccel"] = collections.RollingArray(arraysize)  
        self.sensors["xSpin"] = collections.RollingArray(arraysize)
        self.sensors["ySpin"] = collections.RollingArray(arraysize)
        self.sensors["zSpin"] = collections.RollingArray(arraysize)
        self.sensors["tilt"] = collections.RollingArray(arraysize)
        self.sensors["roll"] = collections.RollingArray(arraysize)
        self.sensors["yaw"] = collections.RollingArray(arraysize)
        self.sensors["orientation"] = collections.RollingArray(arraysize)

    def read(self):
        imu = sensors.imu.read()
        self.sensors["xAccel"].push(imu.accel_x)  
        self.sensors["yAccel"].push(imu.accel_y)
        self.sensors["zAccel"].push(imu.accel_z)
        self.sensors["xSpin"].push(imu.gyro_x)  
        self.sensors["xSpin"].push(imu.gyro_y)  
        self.sensors["xSpin"].push(imu.gyro_z)  
        self.sensors["tilt"].push(imu.tilt)  
        self.sensors["roll"].push(imu.roll)  
        self.sensors["yaw"].push(imu.yaw)  
        self.sensors["orientation"].push(getOrientationAngle())

    def getOrientationAngle(self):
        return self.yaw / 2 * pi * 360  #TODO: calculate angle from here

    def publishSensors(self, mqtt):
        content = json.dumps(self.sensors)
        mqtt.publish("roger/sensors/matrix/imu",content)


class LEDArray:
    MAXDISTANCE = 360

    def __init__(self):
        self.ledarray = []
        for i in range(35):
            self.ledarray.append({'r':0, 'g':0, 'b':0, 'w':0})

    def parseCommand(self, payload):
        args = payload.split(",")
        method = "apply" + args.pop(0)
        method(args)
        

    def applyProxArray(self, array):
        ratio = len(array) / len(self.ledarray)
        for i in range(0,len(self.ledarray)):
            low = round(i * ratio)
            high = round((i + 1) * ratio)
            if high > len(array):
                high = len(array)
            subarray = []
            for x in array[low:high]:
                subarray.append(x.getValue())
            intensity = round(stat.mean(subarray) / MAXDISTANCE * 255)
            self.ledarray[i] = {'r':intensity, 'g':0, 'b':0, 'w':0}  #red
        led.set(self.ledarray)

    def applyColor(self, color):
        led.set(color)

    def applyClear(self, nothing):
        led.set()

    def applyRoundinaCircle(self, args):
        everloop = ['black'] * led.length
        everloop[0] = args[0]
        for i in range(args[1]):
            everloop.append(everloop.pop(0))
            led.set(everloop)
            time.sleep(0.050)
        applyClear()

    def applyRainbow(self, times):
        everloop = ['black'] * led.length

        ledAdjust = 0.51 # MATRIX Creator

        frequency = 0.375
        counter = 0.0
        tick = len(everloop) - 1

        for i in range(times[0]):
        # Create rainbow
            for i in range(len(everloop)):
                r = round(max(0, (sin(frequency*counter+(pi/180*240))*155+100)/10))
                g = round(max(0, (sin(frequency*counter+(pi/180*120))*155+100)/10))
                b = round(max(0, (sin(frequency*counter)*155+100)/10))

                counter += ledAdjust

                everloop[i] = {'r':r, 'g':g, 'b':b}

            # Slowly show rainbow
            if tick != 0:
                for i in reversed(range(tick)):
                    everloop[i] = {}
                tick -= 1

            led.set(everloop)

            time.sleep(.035)

        applyClear()

    class Sensors:
        def __init__(self):
            pass
            #temp/pressure/hum
            #uv

    class Microphones:
        def __init__(self):
            pass
            #record sound
            #sound direction

    