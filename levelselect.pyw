import pygame, levels, settings, os
ROOT = os.path.dirname(os.path.abspath(__file__))
settings.ReadConfigFile()
pygame.init()
SCREENWIDTH, SCREENHEIGHT = 1280, 720 # 1920x1080/1.5 (80x45) => Grid: 16x9
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
gameTitle = "Ender Flynnies"
pygame.display.set_caption(f"{gameTitle} - Select Level")
pygame.display.set_icon(pygame.image.load(ROOT + "\\Images\\EnderPearl.png"))
pygame.mouse.set_visible(False)

LevelSelectFont = pygame.font.Font(ROOT + "\\Fonts\\Kidzone.ttf", 100)

BackgroundTile = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\endstone.png"), (settings.TileSize, settings.TileSize)) if not settings.DarkMode else pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\OBSIDIAN.png"), (settings.TileSize, settings.TileSize))

CursorFlick1 = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\CursorFlick1.png"), (settings.TileSize//2, settings.TileSize//2))
CursorFlick2 = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\CursorFlick2.png"), (settings.TileSize//2, settings.TileSize//2))

LevelSelectScale = (280,280)

BackButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\BackButton.png"), (100, 100))
BackButtonRect = pygame.Rect(10, 10, 100, 100)

ParallaxDistance = 4

BlueButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\levelSelectEasy.png"), LevelSelectScale)
GreenButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\levelSelectNormal.png"), LevelSelectScale)
YellowButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\levelSelectHard.png"), LevelSelectScale)
RedButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\levelSelectHarder.png"), LevelSelectScale)
PinkButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\levelSelectInsane.png"), LevelSelectScale)
BlackButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\levelSelectMaster.png"), LevelSelectScale)
GrayButton = pygame.transform.scale(pygame.image.load(ROOT + "\\Images\\levelSelectUnknown.png"), LevelSelectScale)

DifficultyEasyTexture = BlueButton
DifficultyNormalTexture = GreenButton
DifficultyHardTexture = YellowButton
DifficultyHarderTexture = RedButton
DifficultyInsaneTexture = PinkButton
DifficultyMasterTexture = BlackButton
DifficultyUnknownTexture = GrayButton
DifficultyLockedTexture = GrayButton

clock = pygame.time.Clock()

LevelselectorActive = True
FlickFrame = 0
ScrollOffset = 0

if not settings.MuteMusic:
    pygame.mixer.music.load(ROOT + "\\Sounds\\Level Select.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

while LevelselectorActive:
    cursorpos = pygame.mouse.get_pos()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            LevelselectorActive = False
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            break
        if event.type == pygame.MOUSEWHEEL:
            ScrollOffset -= 50*event.y
            ScrollOffset = max(ScrollOffset, 0)
            ScrollOffset = min(ScrollOffset, ((len(levels.levels)-1)//4)*320-SCREENHEIGHT+340)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if BackButtonRect.collidepoint(cursorpos):
                    LevelselectorActive = False
                    break
                else:
                    MouseX, MouseY = cursorpos
                    ClickedX = MouseX//320
                    ClickedY = (MouseY+ScrollOffset)//320
                    LevelIndex = (ClickedY*4)+ClickedX
                    if 0 <= LevelIndex < len(levels.levels)-1:
                        if LevelIndex < levels.LastAccessibleLevel:
                            OrigFirstLevel = levels.FirstLevel
                            levels.FirstLevel = LevelIndex+1
                            pygame.mixer.music.stop()
                            pygame.mixer.music.unload()
                            with open("Flynn.pyw") as file:
                                game = file.read()
                                exec(game)
                            pygame.display.set_caption(f"{gameTitle} - Select Level")
                            if not settings.MuteMusic:
                                pygame.mixer.music.load(ROOT + "\\Sounds\\Level Select.mp3")
                                pygame.mixer.music.set_volume(0.4)
                                pygame.mixer.music.play(-1)
                            levels.FirstLevel = OrigFirstLevel
    try:
        FlickFrame += 1/clock.get_fps()*12
    except:
        FlickFrame += 1/60*12
    if FlickFrame > 1:
        FlickFrame = 0
    window.fill((0,0,0))
    for ypos in range(SCREENHEIGHT//settings.TileSize+1):
        for xpos in range(SCREENWIDTH//settings.TileSize):
            window.blit(BackgroundTile, (xpos*settings.TileSize, ypos*settings.TileSize-(ScrollOffset//ParallaxDistance)%settings.TileSize))
    for level in range(len(levels.levels)-1):
        try:
            position = ((level%4*320)+(320-LevelSelectScale[0])//2, (level//4*320-ScrollOffset)+(320-LevelSelectScale[1])//2)
            LevelIDText = LevelSelectFont.render(str(level+1), 1, (235, 235, 235))
            if level < levels.LastAccessibleLevel:
                if levels.difficulties[f"level{level+1}"] == "Easy":
                    window.blit(DifficultyEasyTexture, position)
                elif levels.difficulties[f"level{level+1}"] == "Normal":
                    window.blit(DifficultyNormalTexture, position)
                elif levels.difficulties[f"level{level+1}"] == "Hard":
                    window.blit(DifficultyHardTexture, position)
                elif levels.difficulties[f"level{level+1}"] == "Harder":
                    window.blit(DifficultyHarderTexture, position)
                elif levels.difficulties[f"level{level+1}"] == "Insane":
                    window.blit(DifficultyInsaneTexture, position)
                elif levels.difficulties[f"level{level+1}"] == "Master":
                    window.blit(DifficultyMasterTexture, position)
                else:
                    window.blit(DifficultyUnknownTexture, position)
            else:
                window.blit(DifficultyLockedTexture, position)
            window.blit(LevelIDText, (position[0]+LevelSelectScale[0]//2-LevelIDText.get_width()/2, position[1]+LevelSelectScale[1]//2-LevelIDText.get_height()/2))
        except:
            window.blit(DifficultyUnknownTexture, position)
            window.blit(LevelIDText, (position[0]+LevelSelectScale[0]//2-LevelIDText.get_width()/2, position[1]+LevelSelectScale[1]//2-LevelIDText.get_height()/2))
    window.blit(BackButton, (10, 10))
    if pygame.mouse.get_focused():
        if round(FlickFrame) and not settings.DisableFlashes:
            window.blit(CursorFlick1, cursorpos)
        else:
            window.blit(CursorFlick2, cursorpos)
    pygame.display.update()