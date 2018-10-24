from settings import *

from threading import Thread
from time import sleep

class passeRougeT(Thread):
    def __init__(self, feu):
        Thread.__init__(self)
        self.feu = feu
    
    def run(self):
        self.feu.etat = 'orange'
        sleep(dureeFeuOrange)
        self.feu.etat = 'rouge'

class Feu(object):
    def __init__(self, voie, coord, etat):
        self.voie = voie
        self.coord = coord
        self.etat = etat
    
    def passeVert(self):
        self.etat = 'vert'
    
    def passeRouge(self):
        passeRougeT(self).start()
    
    def changeEtat(self):
        if self.etat == 'vert':
            self.passeRouge()
        else:
            self.passeVert()
    
    def afficher(self):
        if self.etat == 'vert':
            fill(51, 255, 51)
        elif self.etat == 'orange':
            fill(255, 102, 0)
        else:
            fill(239, 32, 32)
        
        if self.voie.route.axe == 'x':
            if self.voie.id == 0:
                x = self.coord + 2*m2p(largeurVoie)
                y = self.voie.route.coord - 2*m2p(largeurVoie)
            else:
                x = self.coord - 2*m2p(largeurVoie)
                y = self.voie.route.coord + 2*m2p(largeurVoie)
        else:
            if self.voie.id == 0:
                x = self.voie.route.coord - 2*m2p(largeurVoie)
                y = self.coord - 2*m2p(largeurVoie)
            else:
                x = self.voie.route.coord + 2*m2p(largeurVoie)
                y = self.coord + 2*m2p(largeurVoie)
        
        ellipse(x, y, 2*m2p(largeurVoie), 2*m2p(largeurVoie))
