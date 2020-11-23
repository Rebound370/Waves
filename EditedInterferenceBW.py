#Colton Swartwoudt
#Interfering Waves GIF Generator

import numpy as np
from PIL import Image

WIDTH = 500
HEIGHT = 500

#Point Class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, otherPoint):
        dx = self.x - otherPoint.x
        dy = self.y - otherPoint.y
        return np.sqrt(dx**2 + dy**2)

    def str(self):
        return f'({self.x:6.2f}, {self.y:6.2f})'

#Wave Class
class Wave:
    def __init__(self, center, amplitude, wavelength, phase):
        self.center = center
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.phase = phase

    #Calculates the height of any given point along the wave
    def height(self,point):
        r = point.distance(self.center)
        angle = 2.0 * np.pi * r / self.wavelength + self.phase
        return self.amplitude * np.sin(angle)

#Interfering Waves Class
#Holds multiple waves. When height is calculated,
#adds the heights of each wave together to create
#a combined amplitude
class InterferingWaves:
    def __init__(self):
        self.waves = list()

    def addWave(self, wave):
        self.waves.append(wave)

    def height(self,point):
        sum = 0.0
        for wave in self.waves:
            sum += wave.height(point)
        return sum

#Coordinate System
class CoordinateSystem:

    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax

    def normalize(self, point):
        x = (point.x - self.xMin) / (self.xMax - self.xMin)
        y = (point.y - self.yMin) / (self.yMax - self.yMin)
        return Point(x,y)

    def scaleAndTranslate(self, point):
        x = self.xMin + point.x * (self.xMax - self.xMin)
        y = self.yMin + point.y * (self.yMax - self.yMin)
        return Point(x,y)

#Transform Class
#Transforms points from one coordinate system to another
class Transform:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def map(self, point):
        n = self.source.normalize(point)
        return self.destination.scaleAndTranslate(n)

#Normalizes values between 0 and 255
def normalize(values):
    minimum = values.min()
    maximum = values.max()
    fun = lambda x : 256 * ( x - minimum) / (maximum - minimum)
    return fun(values)

def main():

    #Initialization
    print("Beginning Process")
    frameCount = 30
    time = 2
    #fps = frameCount / time
    i = 0
    frameList = []

    #Loops the wave generating code to generate
    #each individual frame of the gif
    while i < frameCount:

        amplitudes = np.zeros( (WIDTH, HEIGHT) )

        #Creates two coordinate systems, allowing for
        #the ability to work in a consistent space
        #and then later transform to whatever
        #size we need.
        world = CoordinateSystem(-1.0, -1.0, +1.0, +1.0)
        device = CoordinateSystem(0, 0, WIDTH, HEIGHT)
        device2world = Transform(device, world)

        #Variables to be changed for changing the appearance of the wave
        pattern = InterferingWaves()
        numberOfWaves = 3
        radius = 0.4
        cx = 0.0
        cy = 0.0

        #Creates each wave and adds them to the Interfering Waves list
        for k in range(numberOfWaves):
            angle = 2.0 * np.pi * k / numberOfWaves
            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            center = Point(x, y)

            #TODO: Create RGB Spawning waves
            #number of wave % 2 for a dedicated red, blue, or green wave
            #if 3 waves, one r one g one b; if 5 waves, two r two g one b
            wave = Wave(center, 1.0, 0.2, i * ( (2 * np.pi) / frameCount) )
            pattern.addWave(wave)

            # (2 * np.pi) / frameCount) is a formula that
            #shifts the phase of the generated wave according to the
            #total amount of frames needed to be generated for one singular loop

        #Transforms the -1, 1 coordinate system to
        #the desired pixel dimensions of the output
        for row in range(HEIGHT):
            for column in range(WIDTH):
                u = Point(column, row)
                v = device2world.map(u)
                h = pattern.height(v)
                amplitudes[row, column] = h

        #Normalizes the amplitudes then appends
        #the list of frames
        #TODO: Change mode to RGB
        normalizedAmplitudes = normalize(amplitudes).astype(np.uint8)
        frameList.append( Image.fromarray(normalizedAmplitudes, "L") )
        #print(normalizedAmplitudes.dtype)
        i += 1
        print("Frame " + str(i) + " / " + str(frameCount) + " completed")

    #Compiles the list of frames into a gif, saves as out.gif in the 
    print("Frames generated, compiling into gif")
    image = frameList[0]
    image.save("out.gif", save_all = True, append_images = frameList, duration = (time / frameCount), loop = 0)
    print("Gif created")

if __name__ == '__main__':
    main()
