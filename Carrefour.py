from settings import *

from threading import Thread
from time import sleep

class Carrefour(object):
    def __init__(self, feuxX, feuxY, dureeFeuVert, dureeFeuRouge):
        self.feuxX = feuxX # Liste des 2 feux sur l'axe x
        self.feuxY = feuxY # Liste des 2 feux sur l'axe y
        self.dureeFeuVert = dureeFeuVert # Duree de feu vert axe x
        self.dureeFeuRouge = dureeFeuRouge # Duree de feu rouge axe x


class actualiserFeux(Thread):
    def __init__(self, carrefour):
        Thread.__init__(self)
        self.feuxX = carrefour.feuxX
        self.feuxY = carrefour.feuxY
    
    def start(self):
        while True:
            for feu in feuxY:
                feu.passeRouge()
            sleep(dureeFeuOrange + dureeRougeDeDegagement)
            for feu in feuxX:
                feu.passeVert()
            sleep(dureeFeuVert)
            for feu in feuxX:
                feu.passeRouge()
            sleep(dureeFeuOrange + dureeRougeDeDegagement)
            for feu in feuxY:
                feu.passeVert()
            sleep(dureeFeuRouge)
