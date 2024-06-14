import pygame as py
from pygame.locals import *
import json
from klasser.Kart import Kart

py.init()
py.mixer.init()

#Henter inn settings
with open("settings.json", "r") as file:
    settings = json.load(file)

#Henter og spiller av musikk
py.mixer.music.load("lyder/Soundtrack_bass.wav")
py.mixer.music.play(-1)
py.mixer.music.set_volume(settings["volume"]/100)


FPS:int = settings["FPS"]
clock:py.time.Clock = py.time.Clock()

surf:py.surface.Surface = py.display.set_mode(
    settings["resolution"],
    DOUBLEBUF | GL_DOUBLEBUFFER | SCALED | (FULLSCREEN if settings["fullscreen"] else 0),
    vsync=1
)

#Tegnegrupper
tegneGruppe:py.sprite.Group = py.sprite.Group()
toppGruppe:py.sprite.Group = py.sprite.Group()
kartKollisjon:py.sprite.Group = py.sprite.Group()


#Kart-instance
K:Kart = Kart(kartKollisjon, [tegneGruppe, toppGruppe])

#Gameloop
while 1:

    for e in py.event.get():
        if e.type == QUIT:
            py.quit()
            exit()

    K.update(surf)
    tegneGruppe.update(surf)
    toppGruppe.update(surf)

    py.display.flip()
    clock.tick(FPS)