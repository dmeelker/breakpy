import pygame
import os

import services
import images
import entity
import blocks
from ball import Ball
import datatypes as types
import levels

class game:
    leftButtonDown = False
    rightButtonDown = False
    running = True
    screen = None
    
    screenSize = (320, 240)
    
    lastFrameTime = pygame.time.get_ticks()
    lastUpdateTime = 0
    updatesPerSecond = 100
    
    clock = None
    
    entities = []
    blocks = set()
    paddle = None
    level = 1
    score = 0
    font = None

    def run(self):
        pygame.init()
        self.updateTitle()
        
        self.screen = pygame.display.set_mode(self.screenSize)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        
        self.loadImages()
        self.loadLevel(1)
        
        self.mainLoop()

    def updateTitle(self):
        pygame.display.set_caption("BreakPy! Score: " + str(self.score))
        
    def loadImages(self):
        images.load('ball.png', 'ball')
        images.load('paddle.png', 'paddle')
        images.load('block.png', 'block-green')
        images.load('block-gray1.png', 'block-gray1')
        images.load('block-gray2.png', 'block-gray2')

    def loadLevel(self, levelIndex):
        self.entities = []

        self.paddle = entity.paddle()
        self.paddle.location = types.vector((self.screenSize[0] / 2) - (self.paddle.size.x / 2), self.screenSize[1] - 20)
        self.entities.append(self.paddle)
        
        ball = Ball()
        ball.location = self.paddle.location.add(types.vector(ball.size.x / 2, -ball.size.y))
        self.entities.append(ball)

        blocks = levels.levels[levelIndex](self.screenSize)

        for block in blocks:
            self.blocks.add(block)
            self.entities.append(block)

    def nextLevel(self):
        self.level += 1
        self.loadLevel(self.level)

    def mainLoop(self):
        self.running = True
        
        while self.running:            
            self.update()
            self.render()
            self.clock.tick(60)
            
        pygame.quit()
    
    def update(self):
        time = pygame.time.get_ticks()
        timePassed = time - self.lastFrameTime
        
        self.handleEvents()
        
        self.updateEntities(time, timePassed)
        
        self.lastFrameTime = time
    
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
        
        # scoreText = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        # self.screen.blit(scoreText, (0, 0))
        
        pygame.display.flip()
        
    def findEntitiesInRectangle(self, rectangle, exclude = None):
        results = []
        for entity in self.entities:
            if entity.getBoundingBox().overlaps(rectangle) and entity != exclude:
                results.append(entity)
        
        return results

    def blockDestroyed(self, block):
        self.blocks.remove(block)
        self.increaseScore()

        if len(self.blocks) == 0:
            self.nextLevel()

    def increaseScore(self):
        self.score += 1
        self.updateTitle()
    
services.game = game()
services.game.run()
