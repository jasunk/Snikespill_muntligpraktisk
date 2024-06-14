import pygame as py


#Spritesheet karakterer:
#https://mikanimus.itch.io/pack-npc-32x32-topdown-rpg

class SpriteHandler:
    def __init__(self, spritesheet_path:str, size:tuple[int,int],*, frameDelay:int = 5, retning:str = "Down") -> None:

        #Lager et bilde og bestemmer colorkey
        self.image:py.surface.Surface = py.surface.Surface(size, py.SRCALPHA)
        self.image.set_colorkey((255,0,255))

        #Håndterer frames med delay
        self.frameDelay:  int = frameDelay
        self.frameCounter:int = 0
        self.frame:       int = 0

        #Standard-state
        self.animState:str = "Idle"
        self.retning:  str = retning

        self.lastSprite:py.surface.Surface = None

        self.sprites:list[py.surface.Surface] = self.klargjør_sprites(
            self.load_spritesheet(spritesheet_path, 6,5, size)
        )

    #Kategoriserer spritesene inn i animasjoner
    def klargjør_sprites(self, sprites:list[py.surface.Surface]) -> dict[str, list[py.surface.Surface]]:
        return {
            "DownWalk":sprites[0:5],
            "UpWalk":sprites[5:10],
            "RightWalk":sprites[10:15],
            "LeftWalk":sprites[15:20],
            "DownIdle":[sprites[20]],
            "UpIdle":[sprites[21]],
            "RightIdle":[sprites[22]],
            "LeftIdle":[sprites[23]]
        }

    #Animerer sprites
    def animer(self, actor) -> None:

        #Prioriterer vertikale animasjoner for fiender, og bestemmer retning utifra retningsvektor til "actor"

        if abs(actor.retningsvektor.y) > abs(actor.retningsvektor.x):
            if actor.retningsvektor.y>0: retning = "Down"
            if actor.retningsvektor.y<0: retning = "Up"
        else:
            if actor.retningsvektor.x>0: retning = "Right"
            if actor.retningsvektor.x<0: retning = "Left"

        #Om ingen bevegelse, gå inn i idle-state
        if actor.retningsvektor.length()<0.02:
            actor.spritehandler.animState="Idle"
            self.frame=0

        #Om ikke, gå inn i Walk-state og oppdater retning
        else:
            self.animState="Walk"
            self.retning= retning

        #Går til neste frame om counter tilsier det
        self.frameCounter += 1
        if self.frameCounter >= self.frameDelay:
            if self.frame >= len(self.sprites[f"{self.retning}{self.animState}"])-1:
                self.frame=0
            else: self.frame+=1
            self.frameCounter = 0


        #Tegn frame
        self.image.blit(self.sprites[f"{self.retning}{self.animState}"][self.frame], (0,0))


    #Laster inn spritesheet
    @staticmethod
    def load_spritesheet(filename:str, rows:int, columns:int, new_size:tuple[int,int]) -> list[py.surface.Surface]:

        spritesheet = py.image.load(filename).convert_alpha()
        sprites = []
        colorkey = (255,0,255)

        for row in range(rows):
            for col in range(columns):

                rect = py.Rect(col * 32, row * 32, 32, 32)

                sprite = py.Surface((32, 32), py.SRCALPHA, 32)

                sprite.fill(colorkey)
                sprite.blit(spritesheet, (0, 0), rect)

                resized_sprite = py.transform.scale(sprite, new_size)
                sprites.append(resized_sprite.convert_alpha())

        return sprites