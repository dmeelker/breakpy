import math

import services
import datatypes as types

class entity:
    location = types.vector(0,0)
    size = types.vector(0,0)
    disposable = False
    disposed = False
    
    def update(self, time, timePassed):
        0
    
    def draw(self, screen):
        0
        
    def getBoundingBox(self):
        return types.rectangle(self.location.x, self.location.y, self.size.x, self.size.y)
    
    def getCenterLocation(self):
        return self.location.add(self.size.multiplyScalar(0.5))
    
    def dispose(self):
        self.disposable = True
    
    def doDispose(self):
        self.disposed = True
        
    def hitByBall(self, ball):
        0
        
    def setImage(self, image):
        self.image = image
        self.size = types.vector(image.get_width(), image.get_height())
    
class paddle(entity):
    image = None
    speed = 0
    
    def draw(self, screen):
        screen.blit(self.image, (self.location.x, self.location.y))
        
class block(entity):
    image = None
    hitpoints = 1
    
    def draw(self, screen):
        screen.blit(self.image, (self.location.x, self.location.y))
        
    def hitByBall(self, ball):
        self.hitpoints -= 1
        if self.hitpoints == 0:
            self.destroy()
            
    def destroy(self):
        services.game.increaseScore()
        self.dispose()
