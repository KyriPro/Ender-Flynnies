import subprocess
import pygame, settings
settings.ReadConfigFile()

pygame.init()

try:
    import ctypes
    APPID = 'KyriWorks.EnderFlynnies.com'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APPID)
except:
    pass

LOCALSCREENWIDTH, LOCALSCREENHEIGHT = 1280, 720 # 1920x1080/1.5 (80x45) => Grid: 16x9
SCREENWIDTH, SCREENHEIGHT = LOCALSCREENWIDTH, LOCALSCREENHEIGHT
localGameTitle = "Ender Flynnies"
gameTitle = localGameTitle

SCREENWIDTH, SCREENHEIGHT = LOCALSCREENWIDTH, LOCALSCREENHEIGHT
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

BackgroundTile = pygame.transform.scale(pygame.image.load("endstone.png"), (settings.TileSize, settings.TileSize)) if not settings.DarkMode else pygame.transform.scale(pygame.image.load("OBSIDIAN.jpg"), (settings.TileSize, settings.TileSize))
Mfont = pygame.font.Font("Kidzone.ttf", 100)
font = pygame.font.Font("Kidzone.ttf", 65)

ButtonBar = pygame.image.load("ButtonBar.png")
ButtonBarScale = 0.5
ButtonBar = pygame.transform.scale(ButtonBar, (int(ButtonBar.get_width()*ButtonBarScale), int(ButtonBar.get_height()*ButtonBarScale)))
ButtonWidth, ButtonHeight = ButtonBar.get_width(), ButtonBar.get_height()

ButtonSpacing = ButtonHeight*1.1

PlayText = font.render("Play", 1, (230, 230, 230))
PLAYDIVISIONOFFSET = 3
PlayButtonX, PlayButtonY = SCREENWIDTH/2-ButtonBar.get_width()/2, SCREENHEIGHT/PLAYDIVISIONOFFSET-ButtonBar.get_height()/2
PlayTextX, PlayTextY = SCREENWIDTH/2-PlayText.get_width()/2, SCREENHEIGHT/PLAYDIVISIONOFFSET-PlayText.get_height()/2
PlayRect = pygame.Rect(PlayButtonX, PlayButtonY, ButtonWidth, ButtonHeight)

SettingsText = font.render("Settings", 1, (230, 230, 230))
SettingsTextX = SCREENWIDTH/2-SettingsText.get_width()/2
SettingsRect = pygame.Rect(PlayRect.x, PlayRect.y+ButtonSpacing*1, ButtonWidth, ButtonHeight)

ExitText = font.render("Exit", 1, (230, 230, 230))
ExitTextX = SCREENWIDTH/2-ExitText.get_width()/2
ExitRect = pygame.Rect(PlayRect.x, PlayRect.y+ButtonSpacing*3, ButtonWidth, ButtonHeight)

HelpText = font.render("Help", 1, (230, 230, 230))
HelpTextX = SCREENWIDTH/2-HelpText.get_width()/2
HelpRect = pygame.Rect(PlayRect.x, PlayRect.y+ButtonSpacing*2, ButtonWidth, ButtonHeight)

CursorFlick1 = pygame.transform.scale(pygame.image.load("CursorFlick1.png"), (settings.TileSize//2, settings.TileSize//2))
CursorFlick2 = pygame.transform.scale(pygame.image.load("CursorFlick2.png"), (settings.TileSize//2, settings.TileSize//2))

try:
    TITLESCREENLOGO = pygame.image.load("Logo.png")
    TITLESCREENLOGOSCALE = 5
    TITLESCREENLOGO = pygame.transform.scale(TITLESCREENLOGO, (int(TITLESCREENLOGO.get_width()*TITLESCREENLOGOSCALE), int(TITLESCREENLOGO.get_height()*TITLESCREENLOGOSCALE)))
    MISSINGTITLELOGO = False
except:
    MISSINGTITLELOGO = True

LOCALFLICKFRAME = 0

def loadDisplaySurface():
    global SCREENWIDTH
    global SCREENHEIGHT
    global window
    global gameTitle
    global BackgroundTile
    global Title
    #pygame.init()
    #SCREENWIDTH, SCREENHEIGHT = LOCALSCREENWIDTH, LOCALSCREENHEIGHT
    #window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    gameTitle = localGameTitle
    pygame.display.set_caption(gameTitle)
    pygame.display.set_icon(pygame.image.load("EnderPearl.png"))
    pygame.mixer.music.load("LauncherTheme.wav")
    pygame.mixer.music.set_volume(0.4)
    if not settings.MuteMusic:pygame.mixer.music.play(-1)
    settings.ReadConfigFile()
    BackgroundTile = pygame.transform.scale(pygame.image.load("endstone.png"), (settings.TileSize, settings.TileSize)) if not settings.DarkMode else pygame.transform.scale(pygame.image.load("OBSIDIAN.jpg"), (settings.TileSize, settings.TileSize))
    Title = Mfont.render("Ender Flynnies", 1, (235, 235, 235)) if settings.DarkMode else Mfont.render("Ender Flynnies", 1, (20, 20, 20))
    pygame.mouse.set_visible(False)
loadDisplaySurface()
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    mousepos=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not pygame.mouse.get_pressed()[0]:break
            if ExitRect.collidepoint(mousepos): # I just figured this shit out but check exit first because of the mouse click combined with the order of operations is like combining electricity with water
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.quit()
                exit()
            if PlayRect.collidepoint(mousepos):
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                with open("levelselect.pyw") as file:
                    game = file.read()
                    exec(game)
                #pygame.quit()
                loadDisplaySurface()
            if SettingsRect.collidepoint(mousepos):
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                with open("ControlPanel.pyw") as file:
                    game = file.read()
                    exec(game)
                #pygame.quit()
                loadDisplaySurface()
                pygame.display.update()
            if HelpRect.collidepoint(mousepos):
                subprocess.Popen(["pythonw", "help.pyw"])
    window.fill((0, 0, 0))
    for ypos in range(LOCALSCREENHEIGHT//settings.TileSize):
        for xpos in range(LOCALSCREENWIDTH//settings.TileSize):
            window.blit(BackgroundTile, (xpos*settings.TileSize, ypos*settings.TileSize))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY+ButtonSpacing*1))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY+ButtonSpacing*3))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY+ButtonSpacing*2))
    window.blit(PlayText, (PlayTextX, PlayTextY))
    window.blit(SettingsText, (SettingsTextX, PlayTextY+ButtonSpacing*1))
    window.blit(ExitText, (ExitTextX, PlayTextY+ButtonSpacing*3))
    window.blit(HelpText, (HelpTextX, PlayTextY+ButtonSpacing*2))
    if MISSINGTITLELOGO: window.blit(Title, (SCREENWIDTH/2-Title.get_width()/2, 30))
    else: window.blit(TITLESCREENLOGO, (SCREENWIDTH/2-TITLESCREENLOGO.get_width()/2, 10))
    if pygame.mouse.get_focused():
        if round(LOCALFLICKFRAME) and not settings.DisableFlashes:
            window.blit(CursorFlick1, mousepos)
        else:
            window.blit(CursorFlick2, mousepos)
    pygame.display.update()
    try:
        LOCALFLICKFRAME += 1/clock.get_fps()*12
    except:
        LOCALFLICKFRAME += 1/60
    if LOCALFLICKFRAME > 1:
        LOCALFLICKFRAME = 0