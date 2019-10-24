import math

import services
import entity
import images
import datatypes as types

class Ball(entity.entity):
    vector = types.vector(2, -2).toUnit()
    velocity = 6
    suspended = False
    
    def __init__(self):
        self.setImage(images.get('ball'))

    def update(self, time, timePassed):
		if self.suspended == False:
			velocityToApply = self.vector.multiplyScalar(self.velocity * (timePassed * 0.02))
			self.handleVerticalCollisions(velocityToApply)
			self.handleHorizontalCollisions(velocityToApply)
    
    def handleVerticalCollisions(self, velocityToApply):
        if velocityToApply.y != 0:
            self.location.y += velocityToApply.y
            
            if self.handleVerticalEntityCollisions(velocityToApply):
                return
            else:
                self.handleVerticalViewCollisions()
    
    def handleVerticalEntityCollisions(self, velocity):
        collidingEntities = services.game.findEntitiesInRectangle(self.getBoundingBox(), self)
        if len(collidingEntities) > 0:
            collidingEntity = collidingEntities[0]
            if velocity.y > 0:
                self.location.y = collidingEntity.location.y - self.size.y
            elif velocity.y < 0:
                self.location.y = collidingEntity.location.y + collidingEntity.size.y
                
            self.vector.y = self.vector.y * -1    
            
            if isinstance(collidingEntity, entity.paddle):
                self.vector.x += collidingEntity.speed / 3.0
                self.vector = self.vector.limitLength(5)

            collidingEntity.hitByBall(self)
            return True
        else:
            return False
        
    def handleVerticalViewCollisions(self):
        if self.location.y < 0:
            self.location.y = 0
            self.vector.y = self.vector.y * -1
            return True
        elif self.location.y + self.size.y > services.game.screenSize[1]:
            self.location.y = services.game.screenSize[1] - self.size.y
            self.vector.y = self.vector.y * -1
            return True
        else:
            return False
    
    def handleHorizontalCollisions(self, velocityToApply):
         if velocityToApply.x != 0:
            self.location.x += velocityToApply.x
            
            if self.handleHorizontalEntityCollisions(velocityToApply):
                return
            
            if self.location.x < 0:
                self.location.x = 0
                self.vector.x = self.vector.x * -1
            elif self.location.x + self.size.y > services.game.screenSize[0]:
                self.location.x = services.game.screenSize[0] - self.size.x
                self.vector.x = self.vector.x * -1
                
    def handleHorizontalEntityCollisions(self, velocity):
        collidingEntities = services.game.findEntitiesInRectangle(self.getBoundingBox(), self)
        if len(collidingEntities) > 0:
            collidingEntity = collidingEntities[0]
            if velocity.x > 0:
                self.location.x = collidingEntity.location.x - self.size.x
                self.vector.x = self.vector.x * -1
            elif velocity.x < 0:
                self.location.x = collidingEntity.location.x + collidingEntity.size.x
                self.vector.x = self.vector.x * -1
            
            collidingEntity.hitByBall(self) 
            return True
        else:
            return False
                
    def draw(self, screen):
        screen.blit(self.image, (self.location.x, self.location.y))
