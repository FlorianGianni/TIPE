from settings import *

class Carrefour(object):
    def __init__(self, feuxX, feuxY, tpsVert, tpsRouge):
        self.feuxX = feuxX # Liste des 2 feux sur l'axe x
        self.feuxY = feuxY # Liste des 2 feux sur l'axe y
        self.tpsVert = tpsVert # Duree de feu vert
        self.tpsRouge = tpsRouge # Duree de feu rouge
