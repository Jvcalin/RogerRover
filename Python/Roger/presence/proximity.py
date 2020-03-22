from common import mycollections as coll

_nodesize = 100


class ProximityNode:

    def __init__(self, size):
        self.Distance = coll.RollingArray(size)

    def push(self, value):
        self.Distance.push(value)

    def getValue(self):
        return self.Distance.getAvg()



class ProximityArray(coll.CircularArray):
    #Magnetic north is at 0
    #Orientation is which way the rover is pointing 
    def __init__(self):
        coll.CircularArray.__init__(self, 360, self.factory)
        self.orientation = 0

    def factory(self):
        return ProximityNode(_nodesize)

    def register(self, angle, value):
        #angle is with respect to orientation
        item = self.GetItem(self.orientation, angle)
        item.push(value)




prox = ProximityArray()
item = prox.GetItem(0,100)
item.push(23)
item.push(33)
item.push(12)
item.push(34)
item.push(25)
item.push(27)
item.push(34)
item.push(24)
item.push(14)
item.push(56)
item.push(24)
item.push(22)
item.push(23)
item.push(24)
item.push(12)
item.push(24)
item.push(14)
item.push(33)
item.push(24)
item.push(13)
item.push(14)
item.push(23)

print(item.getValue())
print(item.Distance.get())
print(item.Distance.getAvg())
print(item.Distance.getRange())
print(item.Distance.getStdDev())
print(item.Distance.getMedian())
print(item.Distance.getVariance())
print(item.Distance.getPVariance())
print(item.Distance.getTrend(10))


"""
TODO:
event handlers... when trends spike suddenly
nerves get triggered

"""