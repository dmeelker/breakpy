import pygame
import os

import services
import entity
from ball import Ball
import datatypes as types

class game:
    leftButtonDown = False
    rightButtonDown = False
    running = True
    screen = None
    
    screenSize = (320, 240);
    
    lastFrameTime = pygame.time.get_ticks()
    lastUpdateTime = 0
    updatesPerSecond = 100
    
    entities = []
    paddle = None

    def run(self):
        pygame.init()
        pygame.display.set_caption("BreakPy")
    
        self.screen = pygame.display.set_mode(self.screenSize)
        
        self.paddle = entity.paddle()
        self.paddle.setImage(pygame.image.load(os.path.join('images', 'paddle.png')))
        self.paddle.location = types.vector((self.screenSize[0] / 2) - (self.paddle.size.x / 2), self.screenSize[1] - 20)
        self.entities.append(self.paddle)
        
        ball = Ball()
        ball.setImage(pygame.image.load(os.path.join('images', 'ball.png')))
        ball.location = self.paddle.location.add(types.vector(ball.size.x / 2, -ball.size.y))
        self.entities.append(ball)
        
        self.placeBlocks()
        
        self.mainLoop()

    def placeBlocks(self):
        blockimage = pygame.image.load(os.path.join('images', 'block.png')) 
        spacing = 8;
        
        for y in range(2):
            for x in range(int((self.screenSize[0] - spacing) / (30 + spacing))):
                block = entity.block()
                block.setImage(blockimage)
                block.location = types.vector(spacing + (x * (30 + spacing)), spacing + (y * (15 + spacing)))
                self.entities.append(block)

    def mainLoop(self):
        self.running = True
        
        while self.running:            
            if pygame.time.get_ticks() - self.lastUpdateTime > 1000 / self.updatesPerSecond:
                self.update()
                self.lastUpdateTime = pygame.time.get_ticks()
            
            self.render()
            
        pygame.quit()
    
    def update(self):
        self.handleEvents()
        
        time = pygame.time.get_ticks()
        timePassed = time - self.lastFrameTime
        
        self.updateEntities(time, timePassed)
        
        self.lastFrameTime = time;
    
    def updateEntities(self, time, timePassed):
        disposables = []
        
        for entity in self.entities:
            entity.update(time, timePassed)
            if entity.disposable:
                disposables.append(entity)
        
        for entity in disposables:
            self.entities.remove(entity)
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.handleKeyEvent(event)
        
        self.paddle.speed = 0
        
        if self.leftButtonDown:
            self.paddle.location.x -= 2
            self.paddle.speed = -2
            if self.paddle.location.x < 0:
                self.paddle.location.x = 0
                self.paddle.speed = 0
        elif self.rightButtonDown:
            self.paddle.location.x += 2
            self.paddle.speed = 2
            if self.paddle.location.x + self.paddle.size.x > self.screenSize[0]:
                self.paddle.location.x = self.screenSize[0] - self.paddle.size.x
                self.paddle.speed = 0
                
    def handleKeyEvent(self, event):
        if event.key == pygame.K_LEFT:
            self.leftButtonDown = event.type == pygame.KEYDOWN
        elif event.key == pygame.K_RIGHT:
            self.rightButtonDown = event.type == pygame.KEYDOWN
    
    def render(self):
        self.screen.fill((0,0,0))
            
        for entity in self.entities:
            entity.draw(self.screen)
        
        pygame.display.flip()
        
    def findEntitiesInRectangle(self, rectangle, exclude = None):
        results = []
        for entity in self.entities:
            if entity.getBoundingBox().overlaps(rectangle) and entity != exclude:
                results.append(entity)
        
        return results

services.game = game()
services.game.run()
