import pygame, levels, settings
settings.ReadConfigFile()
pygame.init()
SCREENWIDTH, SCREENHEIGHT = 1280, 720 # 1920x1080/1.5 (80x45) => Grid: 16x9
window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
gameTitle = "Ender Flynnies"
pygame.display.set_caption(f"{gameTitle} - Select Level")
pygame.display.set_icon(pygame.image.load("EnderPearl.png"))
pygame.mouse.set_visible(False)

LevelSelectFont = pygame.font.Font("Kidzone.ttf", 100)

BackgroundTile = pygame.transform.scale(pygame.image.load("endstone.png"), (settings.TileSize, settings.TileSize)) if not settings.DarkMode else pygame.transform.scale(pygame.image.load("OBSIDIAN.jpg"), (settings.TileSize, settings.TileSize))

CursorFlick1 = pygame.transform.scale(pygame.image.load("CursorFlick1.png"), (settings.TileSize//2, settings.TileSize//2))
CursorFlick2 = pygame.transform.scale(pygame.image.load("CursorFlick2.png"), (settings.TileSize//2, settings.TileSize//2))

LevelSelectScale = (320,320)

BlueButton = pygame.transform.scale(pygame.image.load("levelSelectEasy.png"), LevelSelectScale)
GreenButton = pygame.transform.scale(pygame.image.load("levelSelectNormal.png"), LevelSelectScale)
YellowButton = pygame.transform.scale(pygame.image.load("levelSelectHard.png"), LevelSelectScale)
RedButton = pygame.transform.scale(pygame.image.load("levelSelectHarder.png"), LevelSelectScale)
PinkButton = pygame.transform.scale(pygame.image.load("levelSelectInsane.png"), LevelSelectScale)
BlackButton = pygame.transform.scale(pygame.image.load("levelSelectMaster.png"), LevelSelectScale)
GrayButton = pygame.transform.scale(pygame.image.load("levelSelectUnknown.png"), LevelSelectScale)

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
    pygame.mixer.music.load("Level Select.mp3")
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
                            pygame.mixer.music.load("Level Select.mp3")
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
            window.blit(BackgroundTile, (xpos*settings.TileSize, ypos*settings.TileSize-(ScrollOffset//2)%settings.TileSize))
    for level in range(len(levels.levels)-1):
        try:
            position = (level%4*320, level//4*320-ScrollOffset)
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
            window.blit(LevelIDText, (position[0]+160-LevelIDText.get_width()/2, position[1]+160-LevelIDText.get_height()/2))
        except:
            window.blit(DifficultyUnknownTexture, position)
            window.blit(LevelIDText, (position[0]+160-LevelIDText.get_width()/2, position[1]+160-LevelIDText.get_height()/2))
    if pygame.mouse.get_focused():
        if round(FlickFrame) and not settings.DisableFlashes:
            window.blit(CursorFlick1, cursorpos)
        else:
            window.blit(CursorFlick2, cursorpos)
    pygame.display.update()