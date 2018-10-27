from settings import *
from Feu import *
from Voie import *
from Route import *
from Voiture import *

from threading import Thread
from time import sleep
from random import randint


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


def listeVoitures():
    voitures = []
    for route in routes:
        for voie in route.voies:
            for voiture in voie.voitures:
                voitures.append(voiture)
    return voitures


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
    
    global voitures
    voitures = listeVoitures()
    
    afficherGrille()
    afficherRoutes()
    afficherFeux()
    creerVoitures()
    afficherVoitures()
    supprimerVoitures()
    
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


def afficherVoitures():
    for voiture in voitures:
        voiture.avancer()
        voiture.afficher()


def creerVoitures():
    for route in routes:
        for voie in route.voies:
            if randint(0, ceil(1/(vps*dt))) == 0:
                voie = voie
                m = mM
                v = kmph2pps(vmaxS)
                a = 0
                amax = m2p(amaxM)
                tsecu = float(randint(10, 21)) / 10
                distmin = m2p(float(randint(5, 16)) / 10)
                longueur = m2p(longueurVoitureM)
                largeur = m2p(largeurVoitureM)
                coord = - longueur/2
                if voie.sens() == 'negatif':
                    coord = width + longueur/2
                if len(voie.voitures) == 0 or (voie.voitures[-1].coord > voie.voitures[-1].longueur/2 + longueur/2 + distmin and voie.sens() == 'positif') or (voie.voitures[-1].coord < width - (voie.voitures[-1].longueur/2 + longueur/2 + distmin) and voie.sens() == 'negatif'):
                    voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))


def supprimerVoitures():
    for voiture in voitures:
        if voiture.voie.sens() == 'positif' and voiture.coord > width + voiture.longueur/2:
            voiture.voie.voitures.remove(voiture)
        elif voiture.voie.sens() == 'negatif' and voiture.coord < 0 - voiture.longueur/2:
            voiture.voie.voitures.remove(voiture)


class actualiserFeuxM(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            sleep(dureeFeuVertM)
            feuxVert = [feu for feu in feux if feu.etat == 'vert']
            feuxRouge = [feu for feu in feux if feu.etat == 'rouge']
            for feu in feuxVert:
                feu.passeRouge()
            sleep(dureeFeuOrange + dureeRougeDeDegagement)
            for feu in feuxRouge:
                feu.passeVert()
