from settings import *

class Voie(object):
    def __init__(self, route, coord, id):
        self.route = route # Route associe a la voie
        self.coord = coord # Coordonnee de la route sur l'axe perpendiculaire a route.axe
        self.id = id # 0 si voie de haut/gauche, 1 sinon
        self.voitures = [] # Liste des voitures circulant sur la voie
        self.feux = [] # Liste des feux sur la voie
    
    def sens(self):
        if (self.route.axe == 'x' and self.id == 1) or (self.route.axe == 'y' and self.id == 0):
            return 'positif'
        else:
            return 'negatif'
    
    def afficher(self):
        fill(40)
        if self.route.axe == 'x':
            rect(width//2, self.coord, width, m2p(largeurVoie))
        else:
            rect(self.coord, height//2, m2p(largeurVoie), height)
