from settings import *
from Feu import *
from Voie import *
from Route import *
from Voiture import *

from threading import Thread
from time import sleep


def init():
    global routes
    
    routes = [
              Route('x', height//3), 
              Route('x', 2*height//3), 
              Route('y', width//3), 
              Route('y', 2*width//3)
              ]
    
    routes[0].voies[0].feux += [Feu(routes[0].voies[0], width//3 + m2p(largeurVoie), 'vert')]
    routes[0].voies[1].feux += [Feu(routes[0].voies[1], width//3 - m2p(largeurVoie), 'vert')]
    routes[2].voies[0].feux += [Feu(routes[2].voies[0], height//3 - m2p(largeurVoie), 'rouge')]
    routes[2].voies[1].feux += [Feu(routes[2].voies[1], height//3 + m2p(largeurVoie), 'rouge')]
    
    routes[0].voies[0].feux += [Feu(routes[0].voies[0], 2*width//3 + m2p(largeurVoie), 'vert')]
    routes[0].voies[1].feux += [Feu(routes[0].voies[1], 2*width//3 - m2p(largeurVoie), 'vert')]
    routes[3].voies[0].feux += [Feu(routes[3].voies[0], height//3 - m2p(largeurVoie), 'rouge')]
    routes[3].voies[1].feux += [Feu(routes[3].voies[1], height//3 + m2p(largeurVoie), 'rouge')]
    
    routes[1].voies[0].feux += [Feu(routes[1].voies[0], width//3 + m2p(largeurVoie), 'vert')]
    routes[1].voies[1].feux += [Feu(routes[1].voies[1], width//3 - m2p(largeurVoie), 'vert')]
    routes[2].voies[0].feux += [Feu(routes[2].voies[0], 2*height//3 - m2p(largeurVoie), 'rouge')]
    routes[2].voies[1].feux += [Feu(routes[2].voies[1], 2*height//3 + m2p(largeurVoie), 'rouge')]
    
    routes[1].voies[0].feux += [Feu(routes[1].voies[0], 2*width//3 + m2p(largeurVoie), 'vert')]
    routes[1].voies[1].feux += [Feu(routes[1].voies[1], 2*width//3 - m2p(largeurVoie), 'vert')]
    routes[3].voies[0].feux += [Feu(routes[3].voies[0], 2*height//3 - m2p(largeurVoie), 'rouge')]
    routes[3].voies[1].feux += [Feu(routes[3].voies[1], 2*height//3 + m2p(largeurVoie), 'rouge')]


def listeFeux():
    feux = []
    for route in routes:
        for voie in route.voies:
            for feu in voie.feux:
                feux.append(feu)
    return feux


def setup():
    size(900, 900)
    noStroke()
    rectMode(CENTER)
    
    init()
    
    global feux
    feux = listeFeux()
    
    if utiliserFeuxManuels:
        actualiserFeuxM().start()


def draw():
    background(100)
    afficherGrille()
    afficherRoutes()
    afficherFeux()
    
    sleep(dt)


def afficherGrille():
    stroke(120)
    for i in range(height//m2p(mgrid)+1):
        line(0, i*m2p(mgrid), width, i*m2p(mgrid))
    for j in range(width//m2p(mgrid)+1):
        line(j*m2p(mgrid), 0, j*m2p(mgrid), height)
    noStroke()


def afficherRoutes():
    for route in routes:
        route.afficher()


def afficherFeux():
    for feu in feux:
        feu.afficher()


class actualiserFeuxM(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            sleep(dureeFeuVertM)
            feuxVert = [feu for feu in feux if feu.etat == 'vert']
            for feu in feuxVert:
                feu.passeRouge()
            sleep(dureeFeuOrange + dureeRougeDeDepassement)
            for feu in feux:
                if not(feu in feuxVert):
                    feu.passeVert()
                
