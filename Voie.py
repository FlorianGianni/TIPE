from settings import *

class Voie(object):
    def __init__(self, route, coord, id):
        self.route = route # Route associe a la voie
        self.coord = coord # Coordonnee de la route sur l'axe perpendiculaire a route.axe
        self.id = id # 0 si voie de haut/gauche, 1 sinon
        self.traffic = [] # Liste des voitures circulant sur la voie
        self.feux = [] # Liste des feux sur la voie
    
    def afficher(self):
        fill(40)
        if self.route.axe == 'x':
            rect(width//2, self.coord, width, m2p(largeurVoie))
        else:
            rect(self.coord, height//2, m2p(largeurVoie), height)
