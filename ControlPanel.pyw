import pygame, settings
settings.ReadConfigFile()
pygame.init()
SCREENWIDTH, SCREENHEIGHT = 1280, 720 # 1920x1080/1.5 (80x45) => Grid: 16x9
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
srunning = True
clock = pygame.time.Clock()

# Background Tile

BackgroundTile = pygame.transform.scale(pygame.image.load("OBSIDIAN.jpg"), (settings.TileSize, settings.TileSize))

# Config

SliderOn = pygame.transform.scale(pygame.image.load("SliderOn.png"), (50, 50))
SliderOff = pygame.transform.scale(pygame.image.load("SliderOff.png"), (50, 50))
SliderX = 600
DSliderDown = pygame.transform.scale(pygame.image.load("DynamicSliderDown.png"), (50, 50))
DSliderUp = pygame.transform.scale(pygame.image.load("DynamicSliderUp.png"), (50, 50))

LOCALFLICKFRAME = 0

# Rects

DarkModeRect = pygame.Rect(SliderX, 20, 50, 50)
NewTelestopRect = pygame.Rect(SliderX, 70, 50, 50)
CaptionThicknessUpRect = pygame.Rect(SliderX+50, 120, 50, 50)
CaptionThicknessDownRect = pygame.Rect(SliderX+110, 120, 50, 50)
MuteMusicRect = pygame.Rect(SliderX, 170, 50, 50)
MuteSFXRect = pygame.Rect(SliderX, 220, 50, 50)
NoFlashRect = pygame.Rect(SliderX, 270, 50, 50)

# Assets

ButtonBar = pygame.image.load("ButtonBar.png")
ButtonBarScale = 0.5
ButtonBar = pygame.transform.scale(ButtonBar, (int(ButtonBar.get_width()*ButtonBarScale), int(ButtonBar.get_height()*ButtonBarScale)))
ButtonWidth, ButtonHeight = ButtonBar.get_width(), ButtonBar.get_height()
BackButtonX = SCREENWIDTH/2-ButtonBar.get_width()/2
BackButtonY = SCREENHEIGHT-100-ButtonBar.get_height()/2

CursorFlick1 = pygame.transform.scale(pygame.image.load("CursorFlick1.png"), (settings.TileSize//2, settings.TileSize//2))
CursorFlick2 = pygame.transform.scale(pygame.image.load("CursorFlick2.png"), (settings.TileSize//2, settings.TileSize//2))

# Reset & Back

BackRect = pygame.Rect(BackButtonX, BackButtonY, ButtonWidth, ButtonHeight)
ResetRect = pygame.Rect(BackButtonX, BackButtonY-120, ButtonWidth, ButtonHeight)

# More assets

font = pygame.font.Font("KidZone.ttf", 50)
Bfont = pygame.font.Font("KidZone.ttf", 65)
Mfont = pygame.font.Font("KidZone.ttf", 100)

EndStone = pygame.transform.scale(pygame.image.load("endstone.png"), (settings.TileSize, settings.TileSize))
Obsidian = pygame.transform.scale(pygame.image.load("obsidian.jpg"), (settings.TileSize, settings.TileSize))

# GAME

pygame.mouse.set_visible(False)

def ResetSaveData():
    global LOCALFLICKFRAME
    global cursorpos
    Temp = True
    while Temp:
        Temp = Mfont.render("Reset Save Data? (Irreversible)", 1, (20, 20, 20)) if not settings.DarkMode else Mfont.render("Reset Save Data? (Irreversible)", 1, (235, 235, 235))
        if settings.DarkMode:
            for ypos in range(SCREENHEIGHT//settings.TileSize):
                for xpos in range(SCREENWIDTH//settings.TileSize):
                    window.blit(Obsidian, (xpos*settings.TileSize, ypos*settings.TileSize))
        else:
            for ypos in range(SCREENHEIGHT//settings.TileSize):
                for xpos in range(SCREENWIDTH//settings.TileSize):
                    window.blit(EndStone, (xpos*settings.TileSize, ypos*settings.TileSize))
        window.blit(Temp, (SCREENWIDTH/2-Temp.get_width()/2, (SCREENHEIGHT/2-ButtonBar.get_height()/2-60)/2-Temp.get_height()/2))
        window.blit(ButtonBar, (SCREENWIDTH/2-ButtonBar.get_width()/2, SCREENHEIGHT/2-ButtonBar.get_height()/2-60))
        ExitYesRect = pygame.Rect(SCREENWIDTH/2-ButtonBar.get_width()/2, SCREENHEIGHT/2-ButtonBar.get_height()/2-60, ButtonWidth, ButtonHeight)
        window.blit(ButtonBar, (SCREENWIDTH/2-ButtonBar.get_width()/2, SCREENHEIGHT/2-ButtonBar.get_height()/2+60))
        ExitNoRect = pygame.Rect(SCREENWIDTH/2-ButtonBar.get_width()/2, SCREENHEIGHT/2-ButtonBar.get_height()/2+60, ButtonWidth, ButtonHeight)
        Temp = font.render("Yes", 1, (235, 235, 235))
        window.blit(Temp, (SCREENWIDTH/2-Temp.get_width()/2, SCREENHEIGHT/2-Temp.get_height()/2-60))
        Temp = font.render("No", 1, (235, 235, 235))
        window.blit(Temp, (SCREENWIDTH/2-Temp.get_width()/2, SCREENHEIGHT/2-Temp.get_height()/2+60))
        
        cursorpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not pygame.mouse.get_pressed()[0]:break
                mousepos = pygame.mouse.get_pos()
                if ExitNoRect.collidepoint(mousepos):
                    Temp = False
                    break
                if ExitYesRect.collidepoint(mousepos):
                    settings.DeleteConfigFile()
                    settings.ReadConfigFile()
                    Temp = False
                    break
            try:
                LOCALFLICKFRAME += 1/clock.get_fps()*12
            except:
                LOCALFLICKFRAME += 1/60*12
            if LOCALFLICKFRAME > 1:
                LOCALFLICKFRAME = 0
        if pygame.mouse.get_focused():
            if round(LOCALFLICKFRAME) and not settings.DisableFlashes:
                window.blit(CursorFlick1, cursorpos)
            else:
                window.blit(CursorFlick2, cursorpos)
        pygame.display.update()

while srunning:
    clock.tick(60)
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            srunning = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not pygame.mouse.get_pressed()[0]:break
            mousepos = pygame.mouse.get_pos()
            if DarkModeRect.collidepoint(mousepos):
                if settings.DarkMode:settings.UpdateConfigFile(Dark=False)
                else:settings.UpdateConfigFile(Dark=True)
                settings.ReadConfigFile()
            elif NewTelestopRect.collidepoint(mousepos):
                if settings.NewTelestopTextures:settings.UpdateConfigFile(NewTelestopTexture=False)
                else:settings.UpdateConfigFile(NewTelestopTexture=True)
                settings.ReadConfigFile()
            elif CaptionThicknessUpRect.collidepoint(mousepos):
                if settings.CaptionThiccness < 5:
                    settings.UpdateConfigFile(CaptionThickness=settings.CaptionThiccness+1)
                    settings.ReadConfigFile()
            elif CaptionThicknessDownRect.collidepoint(mousepos):
                if settings.CaptionThiccness > 0:
                    settings.UpdateConfigFile(CaptionThickness=settings.CaptionThiccness-1)
                    settings.ReadConfigFile()
            elif MuteMusicRect.collidepoint(mousepos):
                if settings.MuteMusic:settings.UpdateConfigFile(MutedMusic=False)
                else:settings.UpdateConfigFile(MutedMusic=True)
                settings.ReadConfigFile()
            elif MuteSFXRect.collidepoint(mousepos):
                if settings.MuteSFX:settings.UpdateConfigFile(MutedSFX=False)
                else:settings.UpdateConfigFile(MutedSFX=True)
                settings.ReadConfigFile()
            elif NoFlashRect.collidepoint(mousepos):
                if settings.DisableFlashes:settings.UpdateConfigFile(FlashOff=False)
                else:settings.UpdateConfigFile(FlashOff=True)
                settings.ReadConfigFile()
            elif BackRect.collidepoint(mousepos):
                srunning = False
                break
            elif ResetRect.collidepoint(mousepos):
                ResetSaveData()
                settings.ReadConfigFile()
    
    # Background Rendering

    window.fill((0, 0, 0))
    for ypos in range(SCREENHEIGHT//settings.TileSize):
        for xpos in range(SCREENWIDTH//settings.TileSize):
            window.blit(BackgroundTile, (xpos*settings.TileSize, ypos*settings.TileSize))

    # DarkMode
    window.blit(font.render("Dark Mode: ", 1, (230, 230, 230)), (10, 10))
    if settings.DarkMode:window.blit(SliderOn, (SliderX, 20))
    else:window.blit(SliderOff, (SliderX, 20))
    # New TeleStop Textures
    window.blit(font.render("New TeleStop Textures: ", 1, (230, 230, 230)), (10, 60))
    if settings.NewTelestopTextures:window.blit(SliderOn, (SliderX, 70))
    else:window.blit(SliderOff, (SliderX, 70))
    # Text Outline Width
    window.blit(font.render("Text Outline Width (0-5): ", 1, (230, 230, 230)), (10, 110))
    window.blit(font.render(str(settings.CaptionThiccness), 1, (230, 230, 230)), (SliderX, 110))
    window.blit(DSliderUp, (SliderX+50, 120))
    window.blit(DSliderDown, (SliderX+110, 120))
    # MuteMusic
    window.blit(font.render("Mute Music: ", 1, (230, 230, 230)), (10, 160))
    if settings.MuteMusic:window.blit(SliderOn, (SliderX, 170))
    else:window.blit(SliderOff, (SliderX, 170))
    # MuteSFX
    window.blit(font.render("Mute SFX: ", 1, (230, 230, 230)), (10, 210))
    if settings.MuteSFX:window.blit(SliderOn, (SliderX, 220))
    else:window.blit(SliderOff, (SliderX, 220))
    # NoFlashes
    window.blit(font.render("Disable Flashes: ", 1, (230, 230, 230)), (10, 260))
    if settings.DisableFlashes:window.blit(SliderOn, (SliderX, 270))
    else:window.blit(SliderOff, (SliderX, 270))
    # Back & Reset
    window.blit(ButtonBar, (BackButtonX, BackButtonY))
    window.blit(ButtonBar, (BackButtonX, BackButtonY-120))
    window.blit(Bfont.render("Back", 1, (230, 230, 230)), (SCREENWIDTH/2-Bfont.render("Back", 1, (230, 230, 230)).get_width()/2, SCREENHEIGHT-100-Bfont.render("Back", 1, (230, 230, 230)).get_height()/2))
    window.blit(Bfont.render("Delete save data", 1, (230, 230, 230)), (SCREENWIDTH/2-Bfont.render("Delete save data", 1, (230, 230, 230)).get_width()/2, SCREENHEIGHT-220-Bfont.render("Delete save data", 1, (230, 230, 230)).get_height()/2))
    if pygame.mouse.get_focused() and not settings.DisableFlashes:
        if round(LOCALFLICKFRAME):
            window.blit(CursorFlick2, mousepos)
        else:
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