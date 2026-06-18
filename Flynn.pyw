GameVersion = "1.00"

import settings, levels, pygame, math#, random
pygame.init()
SCREENWIDTH, SCREENHEIGHT = 1280, 720 # 1920x1080/1.5 (80x45) => Grid: 16x9
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
gameTitle = "Ender Flynnies"
pygame.display.set_caption(gameTitle)

pygame.display.set_icon(pygame.image.load("EnderPearl.png"))
pygame.mouse.set_visible(False)

Mfont = pygame.font.Font("Kidzone.ttf", 100)
window.blit(Mfont.render("Flynn is teleporting assets...", 1, (230, 230, 230)), (10, 10))
font = pygame.font.Font("Kidzone.ttf", 50)

settings.ReadConfigFile()

CursorFlick1 = pygame.transform.scale(pygame.image.load("CursorFlick1.png"), (settings.TileSize//2, settings.TileSize//2))
CursorFlick2 = pygame.transform.scale(pygame.image.load("CursorFlick2.png"), (settings.TileSize//2, settings.TileSize//2))

OptionalStatusMessage = font.render("", 0, (0, 0, 0)) # Set the default to nothing
OptionalStatusMessageOutline = font.render("", 0, (0, 0, 0)) # Set the default to nothing

OutlineOffset = settings.CaptionThiccness

def loadStatusMessage(text):
    global OptionalStatusMessage
    global OptionalStatusMessageOutline
    OptionalStatusMessage = font.render(text, 1, (20, 20, 20)) # 20 20 20 or 235 235 235
    OptionalStatusMessageOutline = font.render(text, 1, (235, 235, 235)) # 20 20 20 or 235 235 235

loadStatusMessage("Welcome to Ender Flynnies!")

PearlRange = 3
#MeowSynthSongs = ["CatsOnPogoSticks.mp3", "Decembruary.mp3", "MEOWTUNE.mp3"]
#MeowSynthSongID = random.randint(0, len(MeowSynthSongs)-1)

#pygame.mixer.music.load(MeowSynthSongs[MeowSynthSongID])
pygame.mixer.music.load("CatsonPogoSticks.mp3")

Muted = pygame.mixer.Sound("Mute.wav")
class Sounds:
    Teleport = pygame.mixer.Sound("Teleport.mp3") if not settings.MuteSFX else Muted
    Flag = pygame.mixer.Sound("tada.mp3") if not settings.MuteSFX else Muted
    PearlMove = pygame.mixer.Sound("PearlMove.wav") if not settings.MuteSFX else Muted
    Fail = pygame.mixer.Sound("Fail.mp3") if not settings.MuteSFX else Muted
    Click = pygame.mixer.Sound("Click.wav") if not settings.MuteSFX else Muted
    Collect = pygame.mixer.Sound("CoinCollect.mp3") if not settings.MuteSFX else Muted

FlynnFlick1 = pygame.transform.scale(pygame.image.load("FlynnFlick1.png"), (settings.TileSize, settings.TileSize))
FlynnFlick2 = pygame.transform.scale(pygame.image.load("FlynnFlick2.png"), (settings.TileSize, settings.TileSize))

MouseFlick1 = pygame.transform.scale(pygame.image.load("MouseFlick1.png"), (settings.TileSize, settings.TileSize))
MouseFlick2 = pygame.transform.scale(pygame.image.load("MouseFlick2.png"), (settings.TileSize, settings.TileSize))
MouseDir = 0

EndStone = pygame.transform.scale(pygame.image.load("endstone.png"), (settings.TileSize, settings.TileSize))
CryingObsidian = pygame.transform.scale(pygame.image.load("cryingobsidian.png"), (settings.TileSize, settings.TileSize))
Obsidian = pygame.transform.scale(pygame.image.load("obsidian.jpg"), (settings.TileSize, settings.TileSize))
EnderPearl = pygame.transform.scale(pygame.image.load("EnderPearl.png"), (settings.TileSize//2, settings.TileSize//2))
Bedrock = pygame.transform.scale(pygame.image.load("bedrock.png"), (settings.TileSize, settings.TileSize))
UpdateBlock = pygame.transform.scale(pygame.image.load("UnknownBlock.png"), (settings.TileSize, settings.TileSize))

Path = pygame.transform.scale(pygame.image.load("Path.png"), (settings.TileSize, settings.TileSize))

Lock = pygame.transform.scale(pygame.image.load("Lock.png"), (settings.TileSize, settings.TileSize))
MeowCoin = pygame.image.load("MeowCoin.png")

FlynnOutline = pygame.transform.scale(pygame.image.load("FlynnOutline.png"), (settings.TileSize, settings.TileSize))
FlynnOutlineActivated = pygame.transform.scale(pygame.image.load("FlynnOutlineActivated.png"), (settings.TileSize, settings.TileSize))

ButtonBar = pygame.image.load("ButtonBar.png")
ButtonBarScale = 0.5
ButtonBar = pygame.transform.scale(ButtonBar, (int(ButtonBar.get_width()*ButtonBarScale), int(ButtonBar.get_height()*ButtonBarScale)))
ButtonWidth, ButtonHeight = ButtonBar.get_width(), ButtonBar.get_height()

WallTexture = EndStone
BackgroundTexture = Obsidian
TelestopTexture = CryingObsidian
if settings.NewTelestopTextures:TelestopTexture = Bedrock

LeverOffTexture = pygame.transform.scale(pygame.image.load("LeverOff.png"), (settings.TileSize, settings.TileSize))
LeverOnTexture = pygame.transform.scale(pygame.image.load("LeverOn.png"), (settings.TileSize, settings.TileSize))

LockTexture = Lock
TeleStopCodes = [2]

Flag = pygame.transform.scale(pygame.image.load("Flag.png"), (settings.TileSize, settings.TileSize))
FlickFrame = 0
LeverFlipped = False
passable = [0, 3, 5, 7, 8]
LockCodes = [4]
ReverseLockCode = 6

pygame.mixer.music.set_volume(0.4)
#if not settings.MuteMusic:pygame.mixer.music.play()
if not settings.MuteMusic:pygame.mixer.music.play(-1)

MeowCoinXDisplay = SCREENWIDTH-200
MeowCoinTextXOffset = 40
MeowCoins = 0
MeowCoinX, MeowCoinY = 0,0
MeowCoinCollected = False
SelectedLevel = 0
levelDifficulty = "-"

def loadLevel(id):
    print("Initializing Global Variables")
    global SelectedLevel
    global FlynnPosX
    global FlynnPosY
    global FlagPosX
    global FlagPosY
    global EnderPearlOffsetX
    global EnderPearlOffsetY
    global MousePosX
    global MousePosY
    global MouseDir
    global leveldata
    global LeverFlipped
    global levelDifficulty
    global MeowCoinX
    global MeowCoinY
    global MeowCoinCollected
    print(f"Loading 'level{id}'...")
    OldLevelID = SelectedLevel
    SelectedLevel = id
    if SelectedLevel > levels.LastAccessibleLevel:
        levels.LastAccessibleLevel = SelectedLevel
        settings.UpdateConfigFile(LastLevelPlayed=levels.LastAccessibleLevel)
    Temp = False
    LeverFlipped = False
    try:
        leveldata = levels.levels[f"level{SelectedLevel}"]
    except:
        leveldata = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
        ]
        Temp = True
    print("ID Complete")
    try:
        FlynnPosX = levels.spawns[f"level{SelectedLevel}"][1]
        FlynnPosY = levels.spawns[f"level{SelectedLevel}"][0]
    except:
        FlynnPosX = 1
        FlynnPosY = 1
    print("Flynn Complete")
    try:
        MousePosX = levels.mouse[f"level{SelectedLevel}"][1]
        MousePosY = levels.mouse[f"level{SelectedLevel}"][0]
        MouseDir = levels.mouse[f"level{SelectedLevel}"][2]
    except:
        MousePosX = -1
        MousePosY = -1
        MouseDir = 0
    print("Mouse Complete")
    if not Temp:
        try:
            FlagPosX = levels.finishes[f"level{SelectedLevel}"][1]
            FlagPosY = levels.finishes[f"level{SelectedLevel}"][0]
        except:
            FlagPosX = -1
            FlagPosY = -1
    else:
        FlagPosX = 1
        FlagPosY = 1
    print("Flag Complete")
    EnderPearlOffsetX, EnderPearlOffsetY = 0, 0
    print("Pearl Complete")
    print("Loading Status Event Handler...")
    if not Temp:
        try:
            loadStatusMessage(levels.messages[f"level{SelectedLevel}"])
        except:
            loadStatusMessage("unknown")
    else:
        loadStatusMessage("ERROR: LEVEL_MISSING")
    print("Assigning Difficulty")
    if not Temp:
        try:
            levelDifficulty = levels.difficulties[f"level{SelectedLevel}"]
        except:
            levelDifficulty = "-"
    else:
        levelDifficulty = "-"
    print("Difficulty assigned")
    if not Temp:
        try:
            MeowCoinX = levels.coins[f"level{SelectedLevel}"][1]
            MeowCoinY = levels.coins[f"level{SelectedLevel}"][0]
        except:
            MeowCoinX = -1
            MeowCoinY = -1
    else:
        MeowCoinX = -1
        MeowCoinY = -1
    if OldLevelID != SelectedLevel:MeowCoinCollected = False
    print("MeowCoin Loaded")
    print("Load completed successfully")

loadLevel(levels.FirstLevel)

clock = pygame.time.Clock()

FPScap = 60

def Win():
    LocalGameVersion = GameVersion
    print("Game Complete!")
    print("initializing leveldata...")
    global leveldata
    print("switching audio track...")
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("Endscreen.mp3")
    if not settings.MuteMusic:pygame.mixer.music.play()
    print("loading fade surface...")
    fade = pygame.Surface((SCREENWIDTH, SCREENHEIGHT), pygame.SRCALPHA)
    print("applying fade...")
    for _ in range(255):
        clock.tick(FPScap)
        pygame.display.set_caption(f"{gameTitle} | {round(clock.get_fps())} FPS | 100%")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
        fade.fill((0, 0, 0, 1))
        window.blit(fade, (0, 0))
        pygame.display.update()
    print("starting text quick access functions...")
    
    SCROLLDISTANCE = 0
    leveldata = []
    EnderFlynniesText = Mfont.render("Ender Flynnies", 1, (255, 255, 255))
    SCROLLBASE = SCREENHEIGHT/2-EnderFlynniesText.get_height()/2

    def Text(text, distance):
        tempText = font.render(text, 1, (255, 255, 255))
        window.blit(tempText, (SCREENWIDTH/2-tempText.get_width()/2, SCROLLBASE-SCROLLDISTANCE+distance))
    def Header(text, distance):
        tempText = Mfont.render(text, 1, (255, 255, 255))
        window.blit(tempText, (SCREENWIDTH/2-tempText.get_width()/2, SCROLLBASE-SCROLLDISTANCE+distance))
    print("Loading credits")
    window.fill((0, 0, 0))
    window.blit(EnderFlynniesText, (SCREENWIDTH/2-EnderFlynniesText.get_width()/2, SCROLLBASE-SCROLLDISTANCE))
    Text(f"KyriWorks Inc. (R) Ender Flynnies (R) version {LocalGameVersion}", 100)
    pygame.display.update()
    print("Thanks for playing Ender Flynnies")
    pygame.time.wait(1000)
    lastTick = pygame.time.get_ticks()
    while True:
        clock.tick(FPScap)
        lateTick = pygame.time.get_ticks()
        deltatime = (lateTick - lastTick)/1000
        lastTick = pygame.time.get_ticks()
        if pygame.key.get_pressed()[pygame.K_SPACE]:SCROLLDISTANCE += 40*deltatime*2
        else: SCROLLDISTANCE += 40*deltatime
        pygame.display.set_caption(f"{gameTitle} | {round(clock.get_fps())} FPS | 100%")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
        if SCROLLDISTANCE >= 1550+350:
            return 0
        window.fill((0, 0, 0))
        window.blit(EnderFlynniesText, (SCREENWIDTH/2-EnderFlynniesText.get_width()/2, SCROLLBASE-SCROLLDISTANCE))
        Text(f"KyriWorks Inc. (R) Ender Flynnies (R) version {LocalGameVersion}", 100)
        Header("Credits:", 420)
        Text("LordAndiso - Cats on pogo sticks (Main music)", 520)
        #Text("NaonAB - Decembruary (Main Music)", 570)
        #Text("DIngusCola - MEOWTUNE (Main Music)", 620)
        Text("Father of Death - Jab Cross (Level Select Music)", 570)
        Text("Jonas Reijmer - Graphic Designer", 620)
        Text("Kyrian van Jaarsveld - Developer", 670)
        Header("Dedications:", 800)
        Text("Flynn", 900)
        Text("Jonas Reijmer", 950)
        Text("Niels Winkel", 1000)
        Text("Mitchel Grispen", 1050)
        Header("Programs:", 1200)
        Text("Visual Studio Code by Microsoft", 1300)
        Text("Python 3.13.7 by the Python Software Foundation", 1350)
        Text("Pygame 2.6.1", 1400)
        Text("Piskel", 1450)
        Text("THX TO ALL ENDER FLYNNIES <3", 1550)
        pygame.display.update()

running = True
PauseExitCode = 0

def Quit():
    global running
    global FlickFrame
    global cursorpos
    global PauseExitCode
    Temp = True
    while Temp:
        Temp = Mfont.render("Paused", 1, (20, 20, 20)) if not settings.DarkMode else Mfont.render("Paused", 1, (235, 235, 235))
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
        window.blit(ButtonBar, (SCREENWIDTH/2-ButtonBar.get_width()/2, SCREENHEIGHT/2-ButtonBar.get_height()/2+180))
        ExitResetRect = pygame.Rect(SCREENWIDTH/2-ButtonBar.get_width()/2, SCREENHEIGHT/2-ButtonBar.get_height()/2+180, ButtonWidth, ButtonHeight)
        Temp = font.render("Exit", 1, (235, 235, 235))
        window.blit(Temp, (SCREENWIDTH/2-Temp.get_width()/2, SCREENHEIGHT/2-Temp.get_height()/2-60))
        Temp = font.render("Continue", 1, (235, 235, 235))
        window.blit(Temp, (SCREENWIDTH/2-Temp.get_width()/2, SCREENHEIGHT/2-Temp.get_height()/2+60))
        Temp = font.render("Reset Level", 1, (235, 235, 235))
        window.blit(Temp, (SCREENWIDTH/2-Temp.get_width()/2, SCREENHEIGHT/2-Temp.get_height()/2+180))
        
        cursorpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Temp = False
                running = False
                PauseExitCode = 0
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not pygame.mouse.get_pressed()[0]:break
                mousepos = pygame.mouse.get_pos()
                if ExitYesRect.collidepoint(mousepos):
                    Temp = False
                    running = False
                    PauseExitCode = 0
                    break
                if ExitNoRect.collidepoint(mousepos):
                    Temp = False
                    PauseExitCode = 0
                    break
                if ExitResetRect.collidepoint(mousepos):
                    Temp = False
                    PauseExitCode = 1
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Temp = False
                    PauseExitCode = 0
                    break
            try:
                FlickFrame += 1/clock.get_fps()*12
            except:
                FlickFrame += 1/FPScap*12
            if FlickFrame > 1:
                FlickFrame = 0
        if pygame.mouse.get_focused():
            if round(FlickFrame) and not settings.DisableFlashes:
                window.blit(CursorFlick1, cursorpos)
            else:
                window.blit(CursorFlick2, cursorpos)
        pygame.display.update()

SPECIALCODE = 0
winstate = False
frames = 0
bobbingYoffsetStrength = 10

while running:
    cursorpos = pygame.mouse.get_pos()
    clock.tick(FPScap)
    frames += 1
    bobbingYoffset = math.sin(frames/10)*bobbingYoffsetStrength
    pygame.display.set_caption(f"{gameTitle} | {round(clock.get_fps())} FPS | {(SelectedLevel-1)*100//levels.LastLevel}% | Difficulty: {levelDifficulty}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.pause()
            Quit()
            if PauseExitCode == 1:
                Sounds.Fail.play()
                loadLevel(SelectedLevel)
            PauseExitCode = 0
            pygame.mixer.music.unpause()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                EnderPearlOffsetY -= 1
                if EnderPearlOffsetY < -PearlRange or FlynnPosY+EnderPearlOffsetY < 0 or leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] in TeleStopCodes or (leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] in LockCodes and not LeverFlipped) or (leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] == ReverseLockCode and LeverFlipped):
                    EnderPearlOffsetY += 1
                else:
                    Sounds.PearlMove.play()
            if event.key == pygame.K_DOWN:
                EnderPearlOffsetY += 1
                if EnderPearlOffsetY > PearlRange or FlynnPosY+EnderPearlOffsetY > 8 or leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] in TeleStopCodes or (leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] in LockCodes and not LeverFlipped) or (leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] == ReverseLockCode and LeverFlipped):
                    EnderPearlOffsetY -= 1
                else:
                    Sounds.PearlMove.play()
            if event.key == pygame.K_LEFT:
                EnderPearlOffsetX -= 1
                if EnderPearlOffsetX < -PearlRange or FlynnPosX+EnderPearlOffsetX < 0 or leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] in TeleStopCodes or (leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] in LockCodes and not LeverFlipped) or (leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] == ReverseLockCode and LeverFlipped):
                    EnderPearlOffsetX += 1
                else:
                    Sounds.PearlMove.play()
            if event.key == pygame.K_RIGHT:
                EnderPearlOffsetX += 1
                if EnderPearlOffsetX > PearlRange or FlynnPosX+EnderPearlOffsetX > 15 or leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] in TeleStopCodes or (leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] in LockCodes and not LeverFlipped) or (leveldata[FlynnPosY+EnderPearlOffsetY][FlynnPosX+EnderPearlOffsetX] == ReverseLockCode and LeverFlipped):
                    EnderPearlOffsetX -= 1
                else:
                    Sounds.PearlMove.play()
            if event.key == pygame.K_SPACE:
                try:
                    FlynnPosX += EnderPearlOffsetX
                    FlynnPosY += EnderPearlOffsetY
                    if (not leveldata[FlynnPosY][FlynnPosX] in passable or FlynnPosX < 0 or FlynnPosY < 0) and not (leveldata[FlynnPosY][FlynnPosX] in LockCodes and LeverFlipped) and not(leveldata[FlynnPosY][FlynnPosX] == ReverseLockCode and not LeverFlipped):
                        FlynnPosX -= EnderPearlOffsetX
                        FlynnPosY -= EnderPearlOffsetY
                    else:
                        if not EnderPearlOffsetX == 0 or not EnderPearlOffsetY == 0:
                            Sounds.Teleport.play()
                        if MouseDir == 0:
                            for _ in range(abs(EnderPearlOffsetX)+abs(EnderPearlOffsetY)):
                                MousePosX += 1
                                try:
                                    MouseHitWall = (leveldata[MousePosY][MousePosX] not in passable) and not (leveldata[MousePosY][MousePosX] in LockCodes and LeverFlipped) and not (leveldata[MousePosY][MousePosX] == ReverseLockCode and not LeverFlipped)
                                    if MouseHitWall or MousePosX > 15:
                                        MousePosX -= 1
                                        MouseDir = 2
                                        break
                                except:
                                    MousePosX -= 1
                                    MouseDir = 2
                                    break
                        elif MouseDir == 1:
                            for _ in range(abs(EnderPearlOffsetX)+abs(EnderPearlOffsetY)):
                                MousePosY -= 1
                                MouseHitWall = (leveldata[MousePosY][MousePosX] not in passable) and not (leveldata[MousePosY][MousePosX] in LockCodes and LeverFlipped) and not (leveldata[MousePosY][MousePosX] == ReverseLockCode and not LeverFlipped)
                                if MouseHitWall or MousePosY <= -1:
                                    MousePosY += 1
                                    MouseDir = 3
                                    break
                        elif MouseDir == 2:
                            for _ in range(abs(EnderPearlOffsetX)+abs(EnderPearlOffsetY)):
                                MousePosX -= 1
                                MouseHitWall = (leveldata[MousePosY][MousePosX] not in passable) and not (leveldata[MousePosY][MousePosX] in LockCodes and LeverFlipped) and not (leveldata[MousePosY][MousePosX] == ReverseLockCode and not LeverFlipped)
                                if MouseHitWall or MousePosX <= -1:
                                    MousePosX += 1
                                    MouseDir = 0
                                    break
                        elif MouseDir == 3:
                            for _ in range(abs(EnderPearlOffsetX)+abs(EnderPearlOffsetY)):
                                MousePosY += 1
                                try:
                                    MouseHitWall = (leveldata[MousePosY][MousePosX] not in passable) and not (leveldata[MousePosY][MousePosX] in LockCodes and LeverFlipped) and not (leveldata[MousePosY][MousePosX] == ReverseLockCode and not LeverFlipped)
                                    if MouseHitWall or MousePosY >= 9:
                                        MousePosY -= 1
                                        MouseDir = 1
                                        break
                                except:
                                    MousePosY -= 1
                                    MouseDir = 1
                                    break
                        EnderPearlOffsetX = 0
                        EnderPearlOffsetY = 0
                        if FlynnPosX == FlagPosX and FlynnPosY == FlagPosY:
                            if not SelectedLevel == levels.LastLevel:
                                Sounds.Flag.play()
                                SPECIALCODE = 2
                            else:
                                winstate = True
                                break
                        elif leveldata[FlynnPosY][FlynnPosX] == 5:
                            if LeverFlipped:
                                LeverFlipped = False
                                Sounds.Click.play()
                        elif leveldata[FlynnPosY][FlynnPosX] == 7:
                            if not LeverFlipped:
                                LeverFlipped = True
                                Sounds.Click.play()
                        elif abs(FlynnPosX-MousePosX) <= 1 and abs(FlynnPosY-MousePosY) <= 1:
                            Sounds.Fail.play()
                            SPECIALCODE = 1
                        if FlynnPosX == MeowCoinX and FlynnPosY == MeowCoinY:
                            if not MeowCoinCollected:
                                MeowCoins += 1
                                MeowCoinCollected = True
                                Sounds.Collect.play()
                except ValueError:
                    FlynnPosX -= EnderPearlOffsetX
                    FlynnPosY -= EnderPearlOffsetY
            if event.key == pygame.K_RETURN:
                if leveldata[FlynnPosY][FlynnPosX] == 3:
                    LeverFlipped = not LeverFlipped
                    Sounds.Click.play()
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.music.pause()
                Quit()
                if PauseExitCode == 1:
                    Sounds.Fail.play()
                    loadLevel(SelectedLevel)
                PauseExitCode = 0
                pygame.mixer.music.unpause()
            break
    # if not pygame.mixer.music.get_busy():
    #     pygame.mixer.music.unload()
    #     MeowSynthSongID += 1
    #     if MeowSynthSongID == len(MeowSynthSongs):
    #         MeowSynthSongID = 0
    #     pygame.mixer.music.load(MeowSynthSongs[MeowSynthSongID])
    #     pygame.mixer.music.play()
            
    window.fill((20, 20, 20))
    
    for y_idx, y in enumerate(leveldata):
        for x_idx, x in enumerate(y):
            blockstate = leveldata[y_idx][x_idx]
            if blockstate == 0:
                window.blit(BackgroundTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            elif blockstate == 1:
                window.blit(WallTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            elif blockstate == 2:
                window.blit(TelestopTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            elif blockstate == 3:
                window.blit(BackgroundTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
                if not LeverFlipped:window.blit(LeverOffTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
                else:window.blit(LeverOnTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            elif blockstate == 4:
                if not LeverFlipped:
                    window.blit(TelestopTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
                    window.blit(LockTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
                else: window.blit(BackgroundTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            elif blockstate == 5:
                window.blit(BackgroundTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
                window.blit(FlynnOutline if not LeverFlipped else FlynnOutlineActivated, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            elif blockstate == 6:
                if LeverFlipped:
                    window.blit(TelestopTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
                    window.blit(LockTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
                else: window.blit(BackgroundTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            elif blockstate == 7:
                window.blit(BackgroundTexture, (x_idx*settings.TileSize, y_idx*settings.TileSize))
                window.blit(FlynnOutline if LeverFlipped else FlynnOutlineActivated, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            elif blockstate == 8:
                window.blit(Path, (x_idx*settings.TileSize, y_idx*settings.TileSize))
            else:
                window.blit(UpdateBlock, (x_idx*settings.TileSize, y_idx*settings.TileSize))
    if not MeowCoinCollected: window.blit(MeowCoin, (settings.TileSize//2-MeowCoin.get_width()//2+MeowCoinX*settings.TileSize, settings.TileSize//2-MeowCoin.get_height()+MeowCoinY*settings.TileSize+bobbingYoffset+bobbingYoffsetStrength//2))
    window.blit(EnderPearl, (settings.TileSize//2-EnderPearl.get_width()//2+FlynnPosX*settings.TileSize+EnderPearlOffsetX*settings.TileSize, settings.TileSize//2-EnderPearl.get_height()//2+FlynnPosY*settings.TileSize+EnderPearlOffsetY*settings.TileSize))
    if round(FlickFrame) == 0 and not settings.DisableFlashes:
        window.blit(FlynnFlick1, (FlynnPosX*settings.TileSize, FlynnPosY*settings.TileSize))
        window.blit(pygame.transform.rotate(MouseFlick1, MouseDir*90), (MousePosX*settings.TileSize, MousePosY*settings.TileSize))
    else:
        window.blit(FlynnFlick2, (FlynnPosX*settings.TileSize, FlynnPosY*settings.TileSize))
        window.blit(pygame.transform.rotate(MouseFlick2, MouseDir*90), (MousePosX*settings.TileSize, MousePosY*settings.TileSize))
    try:
        FlickFrame += 1/clock.get_fps()*12
    except:
        FlickFrame += 1/FPScap*12
    if FlickFrame > 1:
        FlickFrame = 0
    window.blit(Flag, (FlagPosX*settings.TileSize, FlagPosY*settings.TileSize))
    # Outline
    if settings.CaptionThiccness > 0:
        window.blit(OptionalStatusMessageOutline, (-1*OutlineOffset, -1*OutlineOffset))
        window.blit(OptionalStatusMessageOutline, (1*OutlineOffset, -1*OutlineOffset))
        window.blit(OptionalStatusMessageOutline, (-1*OutlineOffset, 1*OutlineOffset))
        window.blit(OptionalStatusMessageOutline, (1*OutlineOffset, 1*OutlineOffset))
        window.blit(OptionalStatusMessageOutline, (-1*OutlineOffset, 0))
        window.blit(OptionalStatusMessageOutline, (1*OutlineOffset, 0))
        window.blit(OptionalStatusMessageOutline, (0, -1*OutlineOffset))
        window.blit(OptionalStatusMessageOutline, (0, 1*OutlineOffset))
    # Text (No outline)
    window.blit(OptionalStatusMessage, (0, 0))
    if MeowCoins > 0:
        window.blit(MeowCoin, (MeowCoinXDisplay, settings.TileSize//2-MeowCoin.get_height()//2))
        if settings.CaptionThiccness > 0:
            window.blit(font.render(f"x{MeowCoins:03}", 1, (235, 235, 235)), (-1*OutlineOffset+MeowCoinXDisplay+MeowCoinTextXOffset, -1*OutlineOffset))
            window.blit(font.render(f"x{MeowCoins:03}", 1, (235, 235, 235)), (1*OutlineOffset+MeowCoinXDisplay+MeowCoinTextXOffset, -1*OutlineOffset))
            window.blit(font.render(f"x{MeowCoins:03}", 1, (235, 235, 235)), (-1*OutlineOffset+MeowCoinXDisplay+MeowCoinTextXOffset, 1*OutlineOffset))
            window.blit(font.render(f"x{MeowCoins:03}", 1, (235, 235, 235)), (1*OutlineOffset+MeowCoinXDisplay+MeowCoinTextXOffset, 1*OutlineOffset))
            window.blit(font.render(f"x{MeowCoins:03}", 1, (235, 235, 235)), (-1*OutlineOffset+MeowCoinXDisplay+MeowCoinTextXOffset, 0))
            window.blit(font.render(f"x{MeowCoins:03}", 1, (235, 235, 235)), (1*OutlineOffset+MeowCoinXDisplay+MeowCoinTextXOffset, 0))
            window.blit(font.render(f"x{MeowCoins:03}", 1, (235, 235, 235)), (0+MeowCoinXDisplay+MeowCoinTextXOffset, -1*OutlineOffset))
            window.blit(font.render(f"x{MeowCoins:03}", 1, (235, 235, 235)), (0+MeowCoinXDisplay+MeowCoinTextXOffset, 1*OutlineOffset))
        window.blit(font.render(f"x{MeowCoins:03}", 1, (20, 20, 20)), (MeowCoinXDisplay+MeowCoinTextXOffset, 0))
    
    if pygame.mouse.get_focused():
        if round(FlickFrame) and not settings.DisableFlashes:
            window.blit(CursorFlick1, cursorpos)
        else:
            window.blit(CursorFlick2, cursorpos)
    pygame.display.update()
    if winstate:
        Win()
        running = False
    
    if SPECIALCODE == 1:
        for _ in range(60):
            clock.tick(60)
            if round(FlickFrame) == 0 and not settings.DisableFlashes:
                window.blit(FlynnFlick1, (FlynnPosX*settings.TileSize, FlynnPosY*settings.TileSize))
                window.blit(pygame.transform.rotate(MouseFlick1, MouseDir*90), (MousePosX*settings.TileSize, MousePosY*settings.TileSize))
            else:
                window.blit(FlynnFlick2, (FlynnPosX*settings.TileSize, FlynnPosY*settings.TileSize))
                window.blit(pygame.transform.rotate(MouseFlick2, MouseDir*90), (MousePosX*settings.TileSize, MousePosY*settings.TileSize))
            try:
                FlickFrame += 1/clock.get_fps()*12
            except:
                FlickFrame += 1/FPScap*12
            if FlickFrame > 1:
                FlickFrame = 0
            if pygame.mouse.get_focused():
                if round(FlickFrame) and not settings.DisableFlashes:
                    window.blit(CursorFlick1, cursorpos)
                else:
                    window.blit(CursorFlick2, cursorpos)
            pygame.display.update()
        loadLevel(SelectedLevel)
    elif SPECIALCODE == 2:
        for _ in range(60):
            clock.tick(60)
            if round(FlickFrame) == 0 and not settings.DisableFlashes:
                window.blit(FlynnFlick1, (FlynnPosX*settings.TileSize, FlynnPosY*settings.TileSize))
                window.blit(pygame.transform.rotate(MouseFlick1, MouseDir*90), (MousePosX*settings.TileSize, MousePosY*settings.TileSize))
            else:
                window.blit(FlynnFlick2, (FlynnPosX*settings.TileSize, FlynnPosY*settings.TileSize))
                window.blit(pygame.transform.rotate(MouseFlick2, MouseDir*90), (MousePosX*settings.TileSize, MousePosY*settings.TileSize))
            try:
                FlickFrame += 1/clock.get_fps()*12
            except:
                FlickFrame += 1/FPScap*12
            if FlickFrame > 1:
                FlickFrame = 0
            window.blit(Flag, (FlagPosX*settings.TileSize, FlagPosY*settings.TileSize))
            if pygame.mouse.get_focused():
                if round(FlickFrame) and not settings.DisableFlashes:
                    window.blit(CursorFlick1, cursorpos)
                else:
                    window.blit(CursorFlick2, cursorpos)
            pygame.display.update()
        loadLevel(SelectedLevel+1)
    if SPECIALCODE != 0:
        print(f"CODE_EXCEPTION: {SPECIALCODE}")
        SPECIALCODE = 0
# Unload the game to return to the launcher
window.fill((0, 0, 0))
pygame.display.update()
pygame.mixer.music.stop()
pygame.mixer.music.unload()
