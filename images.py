import pygame
import os

images = {}

def load(fileName, key):
    global images
    image = pygame.image.load(os.path.join('images', fileName))
    images[key] = image

def get(key):
    global images
    return images[key]
