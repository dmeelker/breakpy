from enum import Enum

import entity
import services
import images

class Block(entity.entity):
    image = None
    hitpoints = 1
    
    def draw(self, screen):
        screen.blit(self.image, (self.location.x, self.location.y))
        
    def hitByBall(self, ball):
        self.hitpoints -= 1
        if self.hitpoints == 0:
            self.destroy()
            
    def destroy(self):
        services.game.blockDestroyed(self)
        self.dispose()

class GreenBlock(Block):
    def __init__(self):
        self.setImage(images.get('block-green'))
        self.hitpoints = 1

class GrayBlock(Block):
    def __init__(self):
        self.setImage(images.get('block-gray1'))
        self.hitpoints = 2

    def hitByBall(self, ball):
        Block.hitByBall(self, ball)
        if self.hitpoints == 1:
            self.setImage(images.get('block-gray2'))
