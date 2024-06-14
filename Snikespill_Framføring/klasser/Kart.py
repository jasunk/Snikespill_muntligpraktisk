import pygame as py
from pygame.locals import *
import json
from string import ascii_letters
from .Fiende import Fiende
from .Spiller import Spiller
from .SpinnendeHinder import SpinnendeHinder


#Klasse som håndterer rectsene som bygger opp hver "tile" på kartet
class Tile(py.sprite.Sprite):
    def __init__(self,x:int,y:int,størrelse:int|float, surf:py.surface.Surface,*, color:str="", kollisjonsgruppe: list | py.sprite.Group = [], patruljepunkt:int = None, sprite:str = "", levelTrigger:bool =False) -> None:

        #Lager rect
        self.rect:py.rect.Rect = py.rect.Rect(x*størrelse[0], y*størrelse[1], størrelse[0], størrelse[1])

        #Om ikke oppgitt en sprite, tegn seg selv som helfarget firkant
        if not sprite: py.draw.rect(surf,color,self.rect)

        #Om ikke, hent bildet og tegn det
        else:
            bilde:py.surface.Surface = py.image.load(sprite).convert_alpha()
            bilde = py.transform.scale(bilde, (størrelse[0], størrelse[1]))
            surf.blit(bilde, (x*størrelse[0], y*størrelse[1]))

        #Om denne påstanden er sann, vil kollisjon med Tilen laste neste brett
        self.leveltrigger = True if levelTrigger else False

       #Om tile er et patruljepunkt lagres koordinatene her
        if patruljepunkt: self.patrolIndex:int = (patruljepunkt)

        #Legger seg til i kollisjonsgruppen
        super().__init__(kollisjonsgruppe)




#Håndterer innlasting og tegning av enkelt-kart
class Kart:
    def __init__(self, kollisjons_gruppe:py.sprite.Group, tegnegruppe:py.sprite.Group, index:int = 0) -> None:

        #lagrer tegnegruppene
        self.kollisjonsgruppe:py.sprite.Group = kollisjons_gruppe
        self.tegnegruppe:py.sprite.Group = tegnegruppe

        #Bestemmer en kartindex å laste, og laster denne
        self.index:int = index
        self.last_kart(self.index)

        self.debug:bool = False



    #Setupet for å laste et kart gjøres her
    def last_kart(self, index: int) -> None:

        #Leser innstillingene for finne størrelsen på vinduet, og dermed kartet
        with open("settings.json", "r") as f:
            settings = json.load(f)

        self.kartStørrelse: tuple[int, int] = settings["resolution"]

        #Leser inn rå data fra json-fil
        self.rå_data: list[list[str]] = self.hent_kartdata(index)

        #Eget plan som kartet blir tegnet på, slik at bare ett bilde pr frame må tegnes
        self.tolket_kart: py.surface.Surface = py.surface.Surface(self.kartStørrelse).convert()

        #Oppbevarer patruljepunkter for fiende "a"/"b" osv, i en dict
        self.patruljePunkter: dict[str, list[Tile]] = {}

        #Holder styr på alle hindre på brettet
        self.hinder: list[SpinnendeHinder] = []

        #Tolker kartet
        self.tolk_kart()


    #Lasting av rådata
    def hent_kartdata(self, index:int) -> list[list[str]]:

        #Forsøker å laste kart nummer index. Håndterer feilmeldinger ved mislykket lasting
        try:
            with open('./kart.json', 'r') as file:
                data:list[list[str]] = json.load(file)
            return data[str(index)]

        except Exception as e:
            print(f"Følgende feil har oppstått: {e}. \nKart {index} er ikke lastet")
            py.quit()
            exit()

    #Tolker data i kartcellene
    def tolk_kart(self) -> None:

        rå_data: list[list[str]] = self.rå_data

        #Størrelsen på en enkelttile. Regnes utifra vindustørrelse og antall tiles
        størrelse:list[float, float] = [self.kartStørrelse[0]//len(rå_data[0]), self.kartStørrelse[1]//len(rå_data)]

        #Finner hver tile
        for y in range(len(rå_data)):
            for x in range(len(rå_data[y])):

                #Bestemmer utseende og funksjonalitet pr tile

                #0 = Gulv
                #1 = Vegg
                #2 = Spiller og Gulv
                #3 og 4 = Dør
                #5 og 6 = Spinnende hinder
                #Annet  = Fiende og Gulv
                tile = rå_data[y][x]
                match tile:
                    case 0: Tile(x,y,størrelse, self.tolket_kart, sprite="Sprites/gulv1.png")
                    case 1: Tile(x,y,størrelse,self.tolket_kart, sprite="Sprites/vegg.png", kollisjonsgruppe=self.kollisjonsgruppe)
                    case 2:
                        Tile(x,y,størrelse, self.tolket_kart, sprite="Sprites/gulv1.png")
                        spillerRef = Spiller((x*størrelse[0]+størrelse[0]//2,y*størrelse[1]+størrelse[1]//2),størrelse, self.tegnegruppe[1], self.kollisjonsgruppe, self)

                    case 3: Tile(x,y,størrelse,self.tolket_kart, sprite="Sprites/Dør_L.png", levelTrigger=True, kollisjonsgruppe=self.kollisjonsgruppe)
                    case 4: Tile(x,y,størrelse,self.tolket_kart, sprite="Sprites/Dør_R.png",levelTrigger=True, kollisjonsgruppe=self.kollisjonsgruppe)
                    case 5:
                        Tile(x,y,størrelse, self.tolket_kart, sprite="Sprites/gulv1.png")
                        self.hinder.append(SpinnendeHinder((x*størrelse[0]+størrelse[0]/2, y*størrelse[1]+størrelse[1]/2),
                                                           [self.tegnegruppe[0], self.kollisjonsgruppe], 5, 7, størrelse[0]*3, "right"))
                    case 6:
                        Tile(x,y,størrelse, self.tolket_kart, sprite="Sprites/gulv1.png")
                        self.hinder.append(SpinnendeHinder((x*størrelse[0]+størrelse[0]/2, y*størrelse[1]+størrelse[1]/2),
                                                           [self.tegnegruppe[0], self.kollisjonsgruppe], 5, 7, størrelse[0]*3, "left"))

                #Håndterer fiender. Disse defineres som en str med bokstav, og deretter et tall.
                if type(tile) in [str, list]:
                    if type(tile) ==str: tile = [tile]
                    for punkt in tile:
                        _ = Tile(x,y,størrelse,self.tolket_kart, sprite="Sprites/gulv1.png", patruljepunkt=int(punkt[1:]))
                        if (punkt[0]) in self.patruljePunkter: self.patruljePunkter[(punkt[0])].append(_)
                        else: self.patruljePunkter[(punkt[0])]= [_]

        #Spawner fiender
        [Fiende( [self.tegnegruppe[0], self.kollisjonsgruppe],størrelse, self.kollisjonsgruppe, self,assignment, spillerRef) for assignment in self.patruljePunkter.keys()]

    #Tegner kartet
    def update(self, surf) -> None:

        #Inputs for å skifte kart. Hodesaklig for debugging
        keys = py.key.get_pressed()

        if (keys[K_1]): self.neste_brett(presis_index=0)
        if (keys[K_2]): self.neste_brett(presis_index=1)
        if (keys[K_3]): self.neste_brett(presis_index=2)
        if (keys[K_4]): self.neste_brett(presis_index=3)
        if (keys[K_5]): self.neste_brett(presis_index=4)
        if (keys[K_6]): self.neste_brett(presis_index=5)
        if (keys[K_v]):self.debug=True
        if (keys[K_c]):self.debug=False


        #Tegner kart og hinder
        surf.blit(self.tolket_kart, (0,0))



        if self.debug:
            farger = ["red", "blue", "yellow", "orange", "white", "black", "magenta", "light blue", "dark green", "gray"]
            for tilhørighet, punktliste in self.patruljePunkter.items():
                farge = farger[ascii_letters.index(tilhørighet)]
                for punkt in punktliste:
                    py.draw.circle(surf, farge, punkt.rect.center, 5)


        for h in self.hinder:
            h.update(surf)

    #Tømmer alle spritegroups og laster
    def restart(self) -> None:
        self.kollisjonsgruppe.empty()
        self.tegnegruppe[0].empty()
        self.tegnegruppe[1].empty()
        self.last_kart(self.index)

    #Laster neste brett
    def neste_brett(self, hopp:int = 1,*, presis_index:int=None) -> None:

        if type(presis_index) == int: self.index = presis_index
        else: self.index+=hopp
        self.restart()