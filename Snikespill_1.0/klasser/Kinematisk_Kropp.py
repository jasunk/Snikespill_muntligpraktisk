import pygame as py
from pygame.locals import K_v, K_c
from .SpriteHandler import SpriteHandler

class Kinematisk_Kropp(py.sprite.Sprite):
    def __init__(self, pos:tuple[int,int],size:tuple[int,int], speed:int, groups:list[py.sprite.Group], kollisjonsgruppe:list[py.sprite.Group], spritesheet:str) -> None:
        super().__init__(groups)
        self.rect:py.rect.Rect = py.rect.Rect(pos[0], pos[1], size[0]-size[0]//3,size[1]+(size[1])**(1/2)-size[1]//5)
        self.rect.center = pos
        self.speed:int = speed*size[0]/60
        self.size:tuple[int,int] = size

        #Bestemmer retningen figuren skal bevege seg i
        self.retningsvektor:py.Vector2 = py.Vector2(0,0.01)

        #Bestemmer hva figuren kolliderer med
        self.kollisjonsgruppe:py.sprite.Group = kollisjonsgruppe

        self.spritehandler:SpriteHandler = SpriteHandler(spritesheet, size)
        self.debug:bool = False

    def update(self, surf:py.surface.Surface, *args, **kwargs) -> None:
        k = py.key.get_pressed()
        if k[K_v]: self.debug=True
        if k[K_c]: self.debug=False
        if self.debug: py.draw.rect(surf, (255,0,0,100), self.rect,0,5)
