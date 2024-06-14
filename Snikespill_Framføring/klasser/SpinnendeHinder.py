import pygame as py
from math import pi, sin, cos


#Ildkulene som spinner
class Ildkule(py.sprite.Sprite):
    def __init__(self, pos:tuple[int,int], size:tuple[int,int], grupper:list[py.sprite.Group]) -> None:
        self.rect:py.rect.Rect = py.rect.Rect(pos[0], pos[1], size[0]//3, size[1]//3)
        self.rect.center = pos

        super().__init__(grupper)
        self.fiendtlig:bool = True

    #Oppdaterer posisjon
    def update_pos(self, new_pos: tuple[int, int]) -> None:
        self.rect.center = new_pos

    #Tegner seg selv
    def update(self,surf:py.surface.Surface, *args, **kwargs) -> None:
        py.draw.circle(surf,"yellow",self.rect.center,10)
        py.draw.circle(surf,"orange",self.rect.center,7)
        py.draw.circle(surf,"red",self.rect.center,5)

class SpinnendeHinder:
    def __init__(self,  pos:tuple[int,int],grupper:list[py.sprite.Group], speed:int, ballAmount:int,length:int, direction:str) -> None:

        self.pos:tuple[int,int] = pos
        self.speed:int = speed
        self.ballAmount:int = ballAmount
        self.length:int = length
        self.direction:str = direction
        self.angle:float = 0.0
        self.kuler:list[Ildkule] = [Ildkule((-10,-10), [15,15], grupper) for i in range(ballAmount)]

    #Spinner rundt
    def spin(self,surf:py.surface.Surface) -> None:

        #Endrer vinkel konstant, retning basert på self.direction
        self.angle += self.speed/60 * (-1 if self.direction == "left" else 1)
        #Bestemmer retning med sin og cos
        retningsVektor:py.Vector2 = py.Vector2(sin(self.angle), cos(self.angle))

        #Finner distansen mellom hver ball
        distanse_mellom = self.length//self.ballAmount

        #Plasserer hver kule med økende distanse fra sentrum, men med samme retningsvektor
        for i in range(len(self.kuler)):

            x = self.pos[0]+retningsVektor.x*i*distanse_mellom
            y = self.pos[1]+retningsVektor.y*i*distanse_mellom
            self.kuler[i].update_pos((x,y))

    #spinner seg selv
    def update(self, surf) -> None:
        self.spin(surf)

