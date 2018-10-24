from settings import *
from Voie import *

class Route(object):
    def __init__(self, axe, coord):
        self.axe = axe # 'x' ou 'y'
        self.coord = coord # Coordonnee de la route sur l'axe perpendiculaire a axe
        self.voies = [Voie(self, coord - m2p(largeurVoie)//2, 0), Voie(self, coord + m2p(largeurVoie)//2, 1)]
    
    def afficher(self):
        for voie in self.voies:
            voie.afficher()
        
        if dessinerLignesContinues:
            stroke(255)
            fill(255)
            if self.axe == 'x':
                rect(width//2, self.coord, width, m2p(largeurLigneContinue)//1)
            else:
                rect(self.coord, height//2, m2p(largeurLigneContinue)//1, height)
            noStroke()
