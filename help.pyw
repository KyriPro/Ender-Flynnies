import pygame, ctypes, settings
settings.ReadConfigFile()
pygame.init()
APPID = 'KyriWorks.EnderFlynnies.com'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APPID)
SCREENWIDTH, SCREENHEIGHT = 700, 500
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_icon(pygame.image.load("EnderPearl.png"))
pygame.display.set_caption("Help")
BackgroundTile = pygame.transform.scale(pygame.image.load("endstone.png"), (settings.TileSize, settings.TileSize)) if not settings.DarkMode else pygame.transform.scale(pygame.image.load("OBSIDIAN.jpg"), (settings.TileSize, settings.TileSize))
font = pygame.font.Font("KidZone.ttf", 50)
fontcolor = (235, 235, 235) if settings.DarkMode else (20, 20, 20)
window.fill((0, 0, 0))
for ypos in range(SCREENHEIGHT//settings.TileSize+1):
    for xpos in range(SCREENWIDTH//settings.TileSize+1):
        window.blit(BackgroundTile, (xpos*settings.TileSize, ypos*settings.TileSize))
window.blit(font.render("[Arrow Keys] - Move pearl", 1, fontcolor), (10, 10))
window.blit(font.render("[Spacebar] - Teleport to pearl", 1, fontcolor), (10, 60))
window.blit(font.render("[Enter] - Interact", 1, fontcolor), (10, 110))
window.blit(font.render("[Return] - Interact", 1, fontcolor), (10, 160))
pygame.display.update()
srunning = True
while srunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            srunning = False
            break