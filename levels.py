import blocks
import datatypes as types

def level1(screenSize):
    levelBlocks = []
    spacing = 1
    
    for y in range(3):
        for x in range(int((screenSize[0] - spacing) / (30 + spacing))):
            newBlock = blocks.GreenBlock()
            newBlock.location = types.vector(spacing + (x * (30 + spacing)), spacing + (y * (15 + spacing)))
            levelBlocks.append(newBlock)
    
    return levelBlocks

def level2(screenSize):
    levelBlocks = []
    spacing = 1
    
    for y in range(3):
        for x in range(int((screenSize[0] - spacing) / (30 + spacing))):
            newBlock = blocks.GrayBlock() if y == 2 else blocks.GreenBlock()
            newBlock.location = types.vector(spacing + (x * (30 + spacing)), spacing + (y * (15 + spacing)))
            levelBlocks.append(newBlock)
    
    return levelBlocks

levels = { 
    1: level1,
    2: level2
}
