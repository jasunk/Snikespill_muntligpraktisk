import pygame as py

#Håndterer tegning og trykking av knapp
class Knapp(py.rect.Rect):
    def __init__(self,pos:tuple[int,int], size:tuple[int,int], text:str, metode:staticmethod) -> None:

        #Størrelsen på knappen
        self.rect:py.rect.Rect = py.rect.Rect(0,0,size[0],size[1])
        self.rect.center=pos

        #Hviklen metode som skal kjøres ved trykk. Oppgis i init
        self.metode:staticmethod = metode

        #https://www.geeksforgeeks.org/python-display-text-to-pygame-window/

        font:py.font.Font =            py.font.Font('freesansbold.ttf', 32)
        self.text:py.font.Font.render = font.render(text, True, "black")

        self.textRect = self.text.get_rect()
        self.textRect.center = pos

        self.knappfarge_hover:str    = "dark gray"
        self.knappfarge_standard:str = "light gray"
        self.knappfarge:str = self.knappfarge_standard


    def update(self,surf:py.surface.Surface) -> None:
        #Om mus innenfor rect, endre farge -> Om mus klikkes, kjør vedlagt metode
        if self.rect.collidepoint(py.mouse.get_pos()):
            self.knappfarge=self.knappfarge_hover
            if py.mouse.get_pressed()[0]: self.metode()

        else: self.knappfarge=self.knappfarge_standard

        #Tegner knapp med tekst
        py.draw.rect(surf, "black", py.rect.Rect(self.rect.x-2, self.rect.y-2, self.rect.width+4, self.rect.height+4))
        py.draw.rect(surf, self.knappfarge, self.rect)
        surf.blit(self.text, self.textRect)