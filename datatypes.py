import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def radiansToDegrees(radians):
    return radians * (180/math.pi)

def degreesToRadians(degrees):
    return degrees * (math.pi / 180)

def vectorFromDegrees(degrees):
    radians = degreesToRadians(degrees)
    return vector(math.cos(radians), math.sin(radians))

class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str(self.x) + "," + str(self.y)
    
    def add(self, otherVector):
        return vector(self.x + otherVector.x, self.y + otherVector.y)
    
    def subtract(self, otherVector):
        return vector(self.x - otherVector.x, self.y - otherVector.y)
    
    def multiplyScalar(self, scalar):
        return vector(self.x * scalar, self.y * scalar)
        
    def toUnit(self):
        length = self.length()
        return vector(self.x / length, self.y / length)
    
    def length(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))
    
    def angleInDegrees(self):
        return radiansToDegrees(math.atan2(self.y, self.x))
        
    def limitLength(self, maxLength):
        length = self.length()
        return self.toUnit().multiplyScalar(min(length, maxLength))
    
class rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def containsPoint(self, point):
        return point.x >= self.x and \
               point.x < self.x + self.width and \
               point.y >= self.y and \
               point.y < self.y + self.height
    
    def overlaps(self, other):
        if other.y + other.height <= self.y or self.y + self.height <= other.y:
            return False;
    
        if other.x + other.width <= self.x or self.x + self.width <= other.x:
            return False;
        return True;
