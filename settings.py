import os, levels

def UpdateConfigFile(NewTelestopTexture=None, Dark=None, CaptionThickness=None, MutedMusic=None, MutedSFX=None, FlashOff=None, LastLevelPlayed=None):
    if NewTelestopTexture==None:NewTelestopTexture=NewTelestopTextures
    if Dark==None:Dark=DarkMode
    if CaptionThickness==None:CaptionThickness=CaptionThiccness
    if MutedMusic==None:MutedMusic=MuteMusic
    if MutedSFX==None:MutedSFX=MuteSFX
    if FlashOff==None:FlashOff=DisableFlashes
    if LastLevelPlayed==None:LastLevelPlayed=levels.LastAccessibleLevel
    with open("config.txt","w") as config:
        config.write(f"{NewTelestopTexture}|{Dark}|{CaptionThickness}|{MutedMusic}|{MutedSFX}|{FlashOff}|{LastLevelPlayed}")
def STRTOBOOL(string):
    if string.lower() == "false":return False
    elif string.lower() == "true":return True
    if len(string) != 0:return True
    else:return False
def ReadConfigFile():
    global NewTelestopTextures
    global DarkMode
    global CaptionThiccness
    global MuteMusic
    global MuteSFX
    global DisableFlashes
    if os.path.exists("config.txt"):
        with open("config.txt","r") as config:
            data = config.read()
            data = data.split("|")
            NewTelestopTextures = STRTOBOOL(data[0])
            DarkMode = STRTOBOOL(data[1])
            CaptionThiccness = int(data[2])
            MuteMusic = STRTOBOOL(data[3])
            MuteSFX = STRTOBOOL(data[4])
            DisableFlashes = STRTOBOOL(data[5])
            levels.LastAccessibleLevel = int(data[6])
    else:
        UpdateConfigFile(True, False, 2, False, False, False, 1)
def DeleteConfigFile():
    if os.path.exists("config.txt"):
        os.remove("config.txt")
NewTelestopTextures = True # TRUE: Show Bedrock texture as TeleStop    FALSE: Show Crying Obsidian as TeleStop | DEFAULT = True
DarkMode = False # Enable Dark Launcher | DEFAULT = False
TileSize = 80 # Size of the Tiles | DEFAULT = 80
CaptionThiccness = 2 # Thickness of the text's outline | DEFAULT = 2
MuteMusic = False
MuteSFX = False
DisableFlashes = False
levels.LastAccessibleLevel = 1