import settings, pygame, math, random, os
ROOT = os.path.dirname(os.path.abspath(__file__))
settings.ReadConfigFile()
try:
    with open("skinconfig.txt", "r") as f:
        file = f.read()
        file = list(file)
        temp = []
        for item in file:
            temp.append(int(item))
        file = temp
        unlockedskins = file
except Exception as e:
    print(e)
    settings.ResetSkins()
    with open("skinconfig.txt", "r") as f:
        file = f.read()
        file = list(file)
        temp = []
        for item in file:
            temp.append(int(item))
        file = temp
        unlockedskins = file
pygame.init()
SCREENWIDTH, SCREENHEIGHT = 1280, 720 # 1920x1080/1.5 (80x45) => Grid: 16x9
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

BackgroundTile = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\endstone.png"), (settings.TileSize, settings.TileSize)) if not settings.DarkMode else pygame.transform.scale(pygame.image.load(ROOT + "/Images/OBSIDIAN.png"), (settings.TileSize, settings.TileSize))
font = pygame.font.Font(ROOT + "\\Fonts\\Kidzone.ttf", 50)
Pfont = pygame.font.Font(ROOT + "\\Fonts\\Kidzone.ttf", 16)
Mfont = pygame.font.Font(ROOT + "\\Fonts\\KidZone.ttf", 100)

CursorFlick1 = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\CursorFlick1.png"), (settings.TileSize//2, settings.TileSize//2))
CursorFlick2 = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\CursorFlick2.png"), (settings.TileSize//2, settings.TileSize//2))

FlickFrame = 0
Frame = pygame.image.load(ROOT + "\\Images\\CostumeFrame.png")
FrameWidth, FrameHeight = Frame.get_width(), Frame.get_height()

BackButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\BackButton.png"), (100, 100))
BackButtonRect = pygame.Rect(10, 10, 100, 100)

SelectedScale = (200, 200)

AngryFlynn = pygame.image.load(ROOT + "\\Images\\AngryFlynnFlick2.png")
AngryFlynnSelected = pygame.transform.scale(AngryFlynn, SelectedScale)

BirthdayFlynn = pygame.image.load(ROOT + "\\Images\\BirthdayFlynnFlick2.png")
BirthdayFlynnSelected = pygame.transform.scale(BirthdayFlynn, SelectedScale)

CoolFlynn = pygame.image.load(ROOT + "\\Images\\CoolFlynnFlicks.png")
CoolFlynnSelected = pygame.transform.scale(CoolFlynn, SelectedScale)

FlipFlynn = pygame.image.load(ROOT + "\\Images\\FlipFlynnFlick2.png")
FlipFlynnSelected = pygame.transform.scale(FlipFlynn, SelectedScale)

Flynn = pygame.image.load(ROOT + "\\Images\\FlynnFlick2.png")
FlynnSelected = pygame.transform.scale(Flynn, SelectedScale)

Glungus = pygame.image.load(ROOT + "\\Images\\Glungus.png")
GlungusSelected = pygame.transform.scale(Glungus, SelectedScale)

RealFlynn = pygame.image.load(ROOT + "/Images/RealFlynnFlicks.png")
RealFlynnSelected = pygame.transform.scale(RealFlynn, SelectedScale)

SockFlynn = pygame.image.load(ROOT + "\\Images\\SockFlynnFlick2.png")
SockFlynnSelected = pygame.transform.scale(SockFlynn, SelectedScale)

AllSkins = [Flynn  , FlipFlynn      , AngryFlynn   , CoolFlynn   , BirthdayFlynn   , SockFlynn   , RealFlynn        , Glungus  ]
AllPrice = [0      , 50             , 75           , 120         , 500             , 150         , 750              , 1000     ]
AllNames = ["Flynn", "Flipped Flynn", "Angry Flynn", "Cool Flynn", "Birthday Flynn", "Sock Flynn", "Realistic Flynn", "Glungus"]

SkinsX = 7
SkinsY = math.ceil(len(AllSkins)/SkinsX)

padding = 1.1

ButtonBar = pygame.image.load(ROOT + "\\Images\\ButtonBar.png")
ButtonBarScale = 0.5
ButtonBar = pygame.transform.scale(ButtonBar, (int(ButtonBar.get_width()*ButtonBarScale), int(ButtonBar.get_height()*ButtonBarScale)))
ButtonWidth, ButtonHeight = ButtonBar.get_width(), ButtonBar.get_height()

pygame.mouse.set_visible(False)
OutlineOffset = settings.CaptionThiccness
MeowCoin1 = pygame.image.load(ROOT + "\\Images\\MeowCoin.png")
MeowCoinXDisplay = SCREENWIDTH-200
MeowCoinTextXOffset = 40
MeowCoins = settings.MeowXP

locksize = 40

lock = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\Lock.png"), (locksize, locksize))


Muted = pygame.mixer.Sound(ROOT + "\\Sounds\\Mute.wav")
class ShopSoundPack:
    Error = pygame.mixer.Sound(ROOT + "\\Sounds\\Fail.mp3") if not settings.MuteSFX else Muted
    Success = pygame.mixer.Sound(ROOT + "\\Sounds\\CoinCollect.mp3") if not settings.MuteSFX else Muted
    Wear1 = pygame.mixer.Sound(ROOT + "\\Sounds\\Wear1.wav") if not settings.MuteSFX else Muted
    Wear2 = pygame.mixer.Sound(ROOT + "\\Sounds\\Wear2.wav") if not settings.MuteSFX else Muted
    Wear3 = pygame.mixer.Sound(ROOT + "\\Sounds\\Wear3.wav") if not settings.MuteSFX else Muted
    Wear4 = pygame.mixer.Sound(ROOT + "\\Sounds\\Wear4.wav") if not settings.MuteSFX else Muted
    Wear5 = pygame.mixer.Sound(ROOT + "\\Sounds\\Wear5.wav") if not settings.MuteSFX else Muted
    Wear6 = pygame.mixer.Sound(ROOT + "\\Sounds\\Wear6.wav") if not settings.MuteSFX else Muted
    SelectSelected = pygame.mixer.Sound(ROOT + "\\Sounds\\Click.wav") if not settings.MuteSFX else Muted

def WearItemSFX(id):
    if id == 1:ShopSoundPack.Wear1.play()
    if id == 2:ShopSoundPack.Wear2.play()
    if id == 3:ShopSoundPack.Wear3.play()
    if id == 4:ShopSoundPack.Wear4.play()
    if id == 5:ShopSoundPack.Wear5.play()
    if id == 6:ShopSoundPack.Wear6.play()

def PurchaseItem(id):
    global FlickFrame
    global cursorpos
    Temp = True
    while Temp:
        clock.tick(60)
        Temp = Mfont.render(f"Purchase {AllNames[id]}?", 1, (20, 20, 20)) if not settings.DarkMode else Mfont.render(f"Purchase {AllNames[id]}?", 1, (235, 235, 235))
        for ypos in range(SCREENHEIGHT//settings.TileSize):
            for xpos in range(SCREENWIDTH//settings.TileSize):
                window.blit(BackgroundTile, (xpos*settings.TileSize, ypos*settings.TileSize))
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
                    return False
                if ExitYesRect.collidepoint(mousepos):
                    return True
            try:
                FlickFrame += 1/clock.get_fps()*12
            except:
                FlickFrame += 1/60*12
            if FlickFrame > 1:
                FlickFrame = 0
        if pygame.mouse.get_focused():
            if round(FlickFrame) and not settings.DisableFlashes:
                window.blit(CursorFlick1, cursorpos)
            else:
                window.blit(CursorFlick2, cursorpos)
        pygame.display.update()

pygame.mixer.music.load(ROOT + "\\Sounds\\Kitty Brain.wav")
pygame.mixer.music.set_volume(0.4)
if not settings.MuteMusic:
    pygame.mixer.music.play(-1)
IconScale = 60
FPScap = 60
clock = pygame.time.Clock()
running = True
while running:
    mousedown = False
    mousepos = pygame.mouse.get_pos()
    clock.tick(FPScap)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousedown = True
                if BackButtonRect.collidepoint(mousepos):
                    running = False
                    break
    for ypos in range(SCREENHEIGHT//settings.TileSize):
        for xpos in range(SCREENWIDTH//settings.TileSize):
            window.blit(BackgroundTile, (xpos*settings.TileSize, ypos*settings.TileSize))

    for id, skin in enumerate(AllSkins):
        FrameX, FrameY = SCREENWIDTH//2-SkinsX*Frame.get_width()*padding//2+id%SkinsX*Frame.get_width()*padding, SCREENHEIGHT//2-SkinsY*Frame.get_height()*padding//2+id//SkinsX*Frame.get_width()*padding
        if mousedown:
            if pygame.Rect(FrameX, FrameY, FrameWidth, FrameHeight).collidepoint(mousepos):
                if unlockedskins[id]:
                    if settings.Skin != id:
                        settings.Skin = id
                        settings.UpdateConfigFile()
                        WearItemSFX(random.randint(1,6))
                    else:
                        ShopSoundPack.SelectSelected.play()
                else:
                    if MeowCoins >= AllPrice[id]:
                        if PurchaseItem(id):
                            MeowCoins -= AllPrice[id]
                            settings.MeowXP = MeowCoins
                            settings.UpdateConfigFile()
                            unlockedskins[id] = 1
                            savestr = []
                            for _ in unlockedskins:
                                savestr.append(str(_))
                            savestr = "".join(savestr)
                            with open("skinconfig.txt", "w") as skinconfig:
                                skinconfig.write(savestr)
                            ShopSoundPack.Success.play()
                        else:
                            ShopSoundPack.Error.play()
                    else:    
                        print("Locked")
                        ShopSoundPack.Error.play()
        window.blit(Frame, (FrameX, FrameY))
        window.blit(pygame.transform.scale(skin, (IconScale, IconScale)), ((SCREENWIDTH//2-SkinsX*Frame.get_width()*padding//2+id%SkinsX*Frame.get_width()*padding)+(Frame.get_width()-IconScale)//2, (SCREENHEIGHT//2-SkinsY*Frame.get_height()*padding//2+id//SkinsX*Frame.get_width()*padding)+(Frame.get_height()-IconScale)//2))
        if not unlockedskins[id]:
            window.blit(lock, ((SCREENWIDTH//2-SkinsX*Frame.get_width()*padding//2+id%SkinsX*Frame.get_width()*padding)+(Frame.get_width()-locksize)//2, (SCREENHEIGHT//2-SkinsY*Frame.get_height()*padding//2+id//SkinsX*Frame.get_width()*padding)+(Frame.get_height()-locksize)//2))
            Temp = Pfont.render(str(AllPrice[id]), 1, (230, 230, 230))
            window.blit(Temp, ((FrameX+FrameWidth//2)-Temp.get_width()//2, FrameY+FrameHeight-Temp.get_height()))

    if settings.Skin == 0:
        window.blit(FlynnSelected, (SCREENWIDTH-SelectedScale[0]-50, 50))
    elif settings.Skin == 1:
        window.blit(FlipFlynnSelected, (SCREENWIDTH-SelectedScale[0]-50, 50))
    elif settings.Skin == 2:
        window.blit(AngryFlynnSelected, (SCREENWIDTH-SelectedScale[0]-50, 50))
    elif settings.Skin == 3:
        window.blit(CoolFlynnSelected, (SCREENWIDTH-SelectedScale[0]-50, 50))
    elif settings.Skin == 4:
        window.blit(BirthdayFlynnSelected, (SCREENWIDTH-SelectedScale[0]-50, 50))
    elif settings.Skin == 5:
        window.blit(SockFlynnSelected, (SCREENWIDTH-SelectedScale[0]-50, 50))
    elif settings.Skin == 6:
        window.blit(RealFlynnSelected, (SCREENWIDTH-SelectedScale[0]-50, 50))
    elif settings.Skin == 7:
        window.blit(GlungusSelected, (SCREENWIDTH-SelectedScale[0]-50, 50))
    
    window.blit(BackButton, (10, 10))

    window.blit(MeowCoin1, (MeowCoinXDisplay, settings.TileSize//2-MeowCoin1.get_height()//2))
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
            window.blit(CursorFlick1, mousepos)
        else:
            window.blit(CursorFlick2, mousepos)
    try:
        FlickFrame += 1/clock.get_fps()*12
    except:
        FlickFrame += 1/FPScap*12
    if FlickFrame > 1:
        FlickFrame = 0
    pygame.display.update()