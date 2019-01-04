from settings import *

from threading import Thread
from time import sleep

class Carrefour(object):
    def __init__(self, feuxX, feuxY, dureeFeuVertX, dureeFeuRougeX):
        self.feuxX = feuxX # Liste des 2 feux sur l'axe x
        self.feuxY = feuxY # Liste des 2 feux sur l'axe y
        self.dureeFeuVertX = dureeFeuVertX # Duree de feu vert axe x
        self.dureeFeuRougeX = dureeFeuRougeX # Duree de feu rouge axe x
