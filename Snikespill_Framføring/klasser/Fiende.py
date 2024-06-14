import pygame as py
from pygame.locals import *
from .Kinematisk_Kropp import Kinematisk_Kropp
from .SpriteHandler    import SpriteHandler


class Fiende(Kinematisk_Kropp):
    def __init__(self,  groups:list[py.sprite.Group],size:tuple[int,int], kollisjonsgruppe:py.sprite.Group, kart, assignment:str, spillerRef) -> None:


        self.fiendtlig:bool = True
        self.assignment:int = assignment
        sorterte_punkter = sorted(kart.patruljePunkter[assignment], key=lambda x: x.patrolIndex)
        #print(sorterte_punkter)
        self.patruljepunkter:list = [[punkt.rect.centerx, punkt.rect.centery] for punkt in sorterte_punkter]
        self.pointIndex:int=1 if len(self.patruljepunkter)>1 else 0



        self.currentState:str = "jag"
        self.statemachine:dict[str,classmethod] = {
            "patruljer":self.patruljer,
            "jag":self.jag

        }

        super().__init__(self.patruljepunkter[0], size,3.5, groups, kollisjonsgruppe, "./Sprites/Soldier/Soldier Walk-Sheet.png")

        self.current_position:py.Vector2 = py.Vector2(self.rect.center)
        self.target: py.Vector2 = py.Vector2(0,0)
        self.spillerRef = spillerRef


    #Beveger fiende mot et punkt spesifisert i self.target
    def move(self) -> None:

        self.current_position = py.Vector2(self.rect.centerx, self.rect.centery)
        self.retningsvektor = self.target - self.current_position
        self.distance_to_target:float = self.retningsvektor.length()

        try: self.retningsvektor = self.retningsvektor.normalize()
        except Exception: ...

        self.rect.centerx += self.retningsvektor.x * self.speed
        self.rect.centery += self.retningsvektor.y * self.speed

    def jag(self) -> None:
        self.target = py.Vector2(self.spillerRef.rect.center)
        self.move()

    def avstand_til_spiller(self) -> float:
        vektor_til_spiller:py.Vector2 = py.Vector2(self.spillerRef.rect.center)-self.current_position
        return vektor_til_spiller.length()


    def patruljer(self) -> None:

        self.target = py.Vector2(self.patruljepunkter[self.pointIndex])

        self.move()

        # Sjekker om fiende er nærme nok til å velge neste punkt

        if self.distance_to_target < self.speed*2:
            self.rect.center = self.target
            self.pointIndex = (self.pointIndex + 1) % len(self.patruljepunkter)
            #print(f"Fiende {self.assignment} has reached point {self.pointIndex}")


    def state_handler(self) -> None:
        if self.avstand_til_spiller()<200:
            self.currentState="jag"
        else:
            self.currentState = "patruljer"

        self.statemachine[self.currentState]()


    def update(self, surf:py.surface.Surface, *args, **kwargs) -> None:

        self.state_handler()
        self.spritehandler.animer(self)

        surf.blit(self.spritehandler.image, (self.rect.centerx-self.size[0]//2,self.rect.centery-self.size[0]//1.5))
        super().update(surf)

