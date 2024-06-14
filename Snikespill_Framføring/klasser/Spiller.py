import pygame as py
from pygame.locals import *
from .Kinematisk_Kropp import Kinematisk_Kropp
from typing import TYPE_CHECKING
from .SpriteHandler import SpriteHandler
from .Soundhandler import Soundhandler
from .Knapp import Knapp

#Spillerklasse
class Spiller(Kinematisk_Kropp):

    def __init__(self, pos:tuple[int,int], size:tuple[int,int], groups:list[py.sprite.Group], kollisjonsgruppe:py.sprite.Group, kart) -> None:


        #Lager en kinematisk kropp med oppgitt info
        super().__init__(pos, size,5, groups,kollisjonsgruppe, "./Sprites/Jester/Jester Walk-Sheet.png")

        #Behandler fottrinn
        self.soundhandler:Soundhandler = Soundhandler()
        self.rect.width*=0.8
        self.rect.height*=0.8
        self.surf:py.surface.Surface = None
        self.kart = kart


        self.levende:bool = True

        #Bilder som vises ved død-skjerm
        self.portrait:py.surface.Surface = py.image.load("Sprites/Jester/Jester low res portraitx3.png")
        self.soldierPortrait:py.surface.Surface = py.image.load("Sprites/Soldier/Soldier low res portraitx3.png")

        #Restart knapp
        self.restart_knapp:Knapp = Knapp((500,500), (300,100), "RESTART", kart.restart)



    #Metode som undersøker kollisjoner
    def sjekk_kollisjon(self, retning: str) -> None:

        #Finner alle kollisjoner i oppgitt kollisjonsgruppe
        hits: list[Tile] = py.sprite.spritecollide(self, self.kollisjonsgruppe, False)

        #Sjekker alle kollisjoner
        for kollisjon in hits:
            #https://stackoverflow.com/questions/610883/how-to-check-if-an-object-has-an-attribute
            if hasattr(hits[0], 'fiendtlig'):
                self.levende = False

            if hasattr(hits[0], 'leveltrigger'):
                if hits[0].leveltrigger: self.kart.neste_brett()
                break



            #Håndterer kollisjoner med kartet
            else:
                #Plasserer spiller riktig iforhold til retning
                if retning == "x":
                    if self.retningsvektor.x > 0:
                        self.rect.right = kollisjon.rect.left
                    elif self.retningsvektor.x < 0:
                        self.rect.left = kollisjon.rect.right
                elif retning == "y":
                    if self.retningsvektor.y > 0:
                        self.rect.bottom = kollisjon.rect.top
                    elif self.retningsvektor.y < 0:
                        self.rect.top = kollisjon.rect.bottom


        #Returnerer en boolean verdi på om vi traff noe eller ikke
        return len(hits) > 0

    #Står for bevegelsen
    def move(self) -> None:
        #henter input
        keys = py.key.get_pressed()

        #Nullstiller retningen
        retningsvektor = py.Vector2(0, 0)

        #Bestemmer retning
        if keys[K_UP] or keys[K_w]:
            retningsvektor.y = -1
        elif keys[K_DOWN] or keys[K_s]:
            retningsvektor.y = 1
        if keys[K_RIGHT] or keys[K_d]:
            retningsvektor.x = 1
        elif keys[K_LEFT] or keys[K_a]:
            retningsvektor.x = -1

        #Normaliserer retningen slik man beveger seg like kjapt langs diagonalene som ellers. Utgangspunkt i pythagoras, diagonalene ville vært lengre uten denne
        self.retningsvektor = retningsvektor.normalize() if retningsvektor.length() != 0 else py.Vector2(0, 0)

        #beveger seg langs x, og rykker tilbake ved treff av vegg
        self.rect.x += self.retningsvektor.x * self.speed
        if self.sjekk_kollisjon("x"):
            self.rect.x -= self.retningsvektor.x * self.speed

        #beveger seg langs y, og rykker tilbake ved treff av vegg
        self.rect.y += self.retningsvektor.y * self.speed
        if self.sjekk_kollisjon("y"):
            self.rect.y -= self.retningsvektor.y * self.speed

        #Animerer
        self.spritehandler.animer(self)

        if self.spritehandler.frame in [1,3,5] and self.spritehandler.frameCounter==0:

            self.soundhandler.play_footstep_with_random_pitch()

    #game over skjerm med mulighet for restart
    def game_over(self) -> None:

        py.draw.rect(self.surf, "gray", py.rect.Rect(0,0,1050,1050))
        self.surf.blit(self.portrait,(640,350))
        self.surf.blit(self.soldierPortrait,(50,350))
        self.restart_knapp.update(self.surf)



    #beveger og tegner
    def update(self, surf:py.surface.Surface, *args, **kwargs) -> None:
        if not self.surf: self.surf = surf

        #Tegner seg selv
        surf.blit(self.spritehandler.image, (self.rect.centerx-self.size[0]//2,self.rect.centery-self.size[0]//1.5))

        #Viser game over om død, beveger seg om ikke
        if not self.levende: self.game_over()
        else: self.move()
        super().update(surf)