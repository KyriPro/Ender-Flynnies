import subprocess
try:
    import pygame, settings, sys, os
    settings.ReadConfigFile()
except:
    subprocess.run(["python", "Crashpad.py", *["Ender Flynnies can not run on your device:", " - Pygame is missing", "Please install pygame 2.6.1 or higher", "Error code: 404 (ERR_FILE_NOT_FOUND) 0x194"]])

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

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

MINIMUM_PYTHON_VERSION = (3, 13)
REQUIRED_KERNEL_TYPE = 'nt'
SUPPORTED_WINDOWS_KERNELS = [10]

if sys.version_info < MINIMUM_PYTHON_VERSION:
    window = pygame.display.set_mode((750,200))
    pygame.display.set_icon(pygame.image.load(ROOT + "\\Images\\LoadingFlynn.png"))
    pygame.display.set_caption("CRITICAL ERROR")
    window.fill((0, 0, 0))
    font = pygame.font.Font(ROOT + "\\Fonts\\KonSystem.ttf", 30)
    window.blit(font.render("Ender Flynnies can not run on your device:", 1, (235, 235, 235)), (0, 0))
    window.blit(font.render(f" - Python 3.13 is required (Current version is {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})", 1, (235, 235, 235)), (0, 35))
    window.blit(font.render("Please upgrade Python to a newer version...", 1, (235, 235, 235)), (0, 70))
    window.blit(font.render("Error Code: 412 (ERR_VERSION_MISMATCH) 0x19C", 1, (235, 235, 235)), (0, 140))
    pygame.display.update()
    error = True
    while error:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
if os.name != REQUIRED_KERNEL_TYPE:
    window = pygame.display.set_mode((950,200))
    pygame.display.set_icon(pygame.image.load(ROOT + "\\Images\\LoadingFlynn.png"))
    pygame.display.set_caption("CRITICAL ERROR")
    window.fill((0, 0, 0))
    font = pygame.font.Font(ROOT + "\\Fonts\\KonSystem.ttf", 30)
    window.blit(font.render("Ender Flynnies can not run on your device:", 1, (235, 235, 235)), (0, 0))
    window.blit(font.render(f" - Unsupported Operating System", 1, (235, 235, 235)), (0, 35))
    window.blit(font.render("Windows 10 or 11 is required", 1, (235, 235, 235)), (0, 70))
    window.blit(font.render("Error Code: 415 (ERR_OPERATING_SYSTEM_MISMATCH) 0x19F", 1, (235, 235, 235)), (0, 140))
    pygame.display.update()
    error = True
    while error:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
if sys.getwindowsversion().major not in SUPPORTED_WINDOWS_KERNELS:
    window = pygame.display.set_mode((1050,200))
    pygame.display.set_icon(pygame.image.load(ROOT + "\\Images\\LoadingFlynn.png"))
    pygame.display.set_caption("CRITICAL ERROR")
    window.fill((0, 0, 0))
    font = pygame.font.Font(ROOT + "\\Fonts\\KonSystem.ttf", 30)
    window.blit(font.render("Ender Flynnies can not run on your device:", 1, (235, 235, 235)), (0, 0))
    window.blit(font.render(f" - Windows Version is too low", 1, (235, 235, 235)), (0, 35))
    window.blit(font.render("Windows 10 or 11 is required", 1, (235, 235, 235)), (0, 70))
    window.blit(font.render("Error Code: 417 (ERR_UNSUPPORTED_WINDOWS_VERSION) 0x1A1", 1, (235, 235, 235)), (0, 140))
    pygame.display.update()
    error = True
    while error:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

BackgroundTile = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\endstone.png"), (settings.TileSize, settings.TileSize)) if not settings.DarkMode else pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\OBSIDIAN.png"), (settings.TileSize, settings.TileSize))
Mfont = pygame.font.Font(ROOT + "\\Fonts\\Kidzone.ttf", 100)
font = pygame.font.Font(ROOT + "\\Fonts\\Kidzone.ttf", 65)

ButtonBar = pygame.image.load(ROOT + "\\Images\\ButtonBar.png")
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
ExitRect = pygame.Rect(PlayRect.x, PlayRect.y+ButtonSpacing*4, ButtonWidth, ButtonHeight)

HelpText = font.render("Help", 1, (230, 230, 230))
HelpTextX = SCREENWIDTH/2-HelpText.get_width()/2
HelpRect = pygame.Rect(PlayRect.x, PlayRect.y+ButtonSpacing*2, ButtonWidth, ButtonHeight)

ShopText = font.render("Shop", 1, (230, 230, 230))
ShopTextX = SCREENWIDTH/2-ShopText.get_width()/2
ShopRect = pygame.Rect(PlayRect.x, PlayRect.y+ButtonSpacing*3, ButtonWidth, ButtonHeight)

CursorFlick1 = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\CursorFlick1.png"), (settings.TileSize//2, settings.TileSize//2))
CursorFlick2 = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\CursorFlick2.png"), (settings.TileSize//2, settings.TileSize//2))

try:
    TITLESCREENLOGO = pygame.image.load(ROOT + "\\Images\\Logo.png")
    TITLESCREENLOGOSCALE = 5
    TITLESCREENLOGO = pygame.transform.scale(TITLESCREENLOGO, (int(TITLESCREENLOGO.get_width()*TITLESCREENLOGOSCALE), int(TITLESCREENLOGO.get_height()*TITLESCREENLOGOSCALE)))
    MISSINGTITLELOGO = False
except:
    MISSINGTITLELOGO = True

LOCALFLICKFRAME = 0
ScrollMenuOffsetY = 0
def loadDisplaySurface():
    global SCREENWIDTH
    global SCREENHEIGHT
    global window
    global gameTitle
    global BackgroundTile
    global Title
    global ScrollMenuOffsetY
    #pygame.init()
    #SCREENWIDTH, SCREENHEIGHT = LOCALSCREENWIDTH, LOCALSCREENHEIGHT
    #window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    gameTitle = localGameTitle
    pygame.display.set_caption(gameTitle)
    pygame.display.set_icon(pygame.image.load(ROOT + "\\Images\\EnderPearl.png"))
    pygame.mixer.music.load(ROOT + "\\Sounds\\LauncherTheme.wav")
    pygame.mixer.music.set_volume(0.4)
    if not settings.MuteMusic:pygame.mixer.music.play(-1)
    settings.ReadConfigFile()
    BackgroundTile = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\endstone.png"), (settings.TileSize, settings.TileSize)) if not settings.DarkMode else pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\OBSIDIAN.png"), (settings.TileSize, settings.TileSize))
    Title = Mfont.render("Ender Flynnies", 1, (235, 235, 235)) if settings.DarkMode else Mfont.render("Ender Flynnies", 1, (20, 20, 20))
    pygame.mouse.set_visible(False)
    ScrollMenuOffsetY = 0
loadDisplaySurface()
clock = pygame.time.Clock()

while True:
    PlayRect = pygame.Rect(PlayButtonX, PlayButtonY - ScrollMenuOffsetY, ButtonBar.get_width(), ButtonBar.get_height())
    SettingsRect = pygame.Rect(PlayButtonX, PlayButtonY + ButtonSpacing*1 - ScrollMenuOffsetY, ButtonBar.get_width(), ButtonBar.get_height())
    HelpRect = pygame.Rect(PlayButtonX, PlayButtonY + ButtonSpacing*2 - ScrollMenuOffsetY, ButtonBar.get_width(), ButtonBar.get_height())
    ExitRect = pygame.Rect(PlayButtonX, PlayButtonY + ButtonSpacing*4 - ScrollMenuOffsetY, ButtonBar.get_width(), ButtonBar.get_height())
    ShopRect = pygame.Rect(PlayButtonX, PlayButtonY + ButtonSpacing*3 - ScrollMenuOffsetY, ButtonBar.get_width(), ButtonBar.get_height())
    clock.tick(60)
    mousepos=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEWHEEL:
            ScrollMenuOffsetY -= 50*event.y
            ScrollMenuOffsetY = max(0, ScrollMenuOffsetY)
            ScrollMenuOffsetY = min(ScrollMenuOffsetY, 250)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not pygame.mouse.get_pressed()[0]:continue
            if ExitRect.collidepoint(mousepos): # I just figured this shit out but check exit first because of the mouse click combined with the order of operations is like combining electricity with water
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.quit()
                exit()
            elif PlayRect.collidepoint(mousepos):
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                with open("levelselect.pyw") as file:
                    game = file.read()
                    exec(game)
                #pygame.quit()
                loadDisplaySurface()
            elif SettingsRect.collidepoint(mousepos):
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                with open("ControlPanel.pyw") as file:
                    game = file.read()
                    exec(game)
                #pygame.quit()
                loadDisplaySurface()
                pygame.display.update()
            elif HelpRect.collidepoint(mousepos):
                subprocess.Popen(["pythonw", "help.pyw"])
            elif ShopRect.collidepoint(mousepos):
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                with open("shop.pyw") as file:
                    game = file.read()
                    exec(game)
                #pygame.quit()
                loadDisplaySurface()
                pygame.display.update()
    window.fill((0, 0, 0))
    for ypos in range(LOCALSCREENHEIGHT//settings.TileSize+1):
        for xpos in range(LOCALSCREENWIDTH//settings.TileSize):
            window.blit(BackgroundTile, (xpos*settings.TileSize, ypos*settings.TileSize-(ScrollMenuOffsetY//4)%settings.TileSize))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY-ScrollMenuOffsetY))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY+ButtonSpacing*1-ScrollMenuOffsetY))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY+ButtonSpacing*4-ScrollMenuOffsetY))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY+ButtonSpacing*2-ScrollMenuOffsetY))
    window.blit(ButtonBar, (PlayButtonX, PlayButtonY+ButtonSpacing*3-ScrollMenuOffsetY))
    window.blit(PlayText, (PlayTextX, PlayTextY-ScrollMenuOffsetY))
    window.blit(SettingsText, (SettingsTextX, PlayTextY+ButtonSpacing*1-ScrollMenuOffsetY))
    window.blit(ExitText, (ExitTextX, PlayTextY+ButtonSpacing*4-ScrollMenuOffsetY))
    window.blit(HelpText, (HelpTextX, PlayTextY+ButtonSpacing*2-ScrollMenuOffsetY))
    window.blit(ShopText, (ShopTextX, PlayTextY+ButtonSpacing*3-ScrollMenuOffsetY))
    if MISSINGTITLELOGO: window.blit(Title, (SCREENWIDTH/2-Title.get_width()/2, 30-ScrollMenuOffsetY))
    else: window.blit(TITLESCREENLOGO, (SCREENWIDTH/2-TITLESCREENLOGO.get_width()/2, 10-ScrollMenuOffsetY))
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