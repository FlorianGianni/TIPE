from settings import *
from Feu import *
from Carrefour import *
from Voie import *
from Route import *
from Voiture import *

from threading import Thread
from time import sleep
from random import randint


def init():
    global routes
    routes = [                                # Dans l'ordre : y de gauche a droite puis x de haut en bas
        Route('y', width//3), 
        Route('y', 2*width//3), 
        Route('x', height//3), 
        Route('x', 2*height//3)
        ]

    routes[2].voies[0].feux += [Feu(routes[2].voies[0], width//3 + m2p(largeurVoie), 'vert')]
    routes[2].voies[1].feux += [Feu(routes[2].voies[1], width//3 - m2p(largeurVoie), 'vert')]
    routes[0].voies[0].feux += [Feu(routes[0].voies[0], height//3 - m2p(largeurVoie), 'rouge')]
    routes[0].voies[1].feux += [Feu(routes[0].voies[1], height//3 + m2p(largeurVoie), 'rouge')]
    
    routes[2].voies[0].feux += [Feu(routes[2].voies[0], 2*width//3 + m2p(largeurVoie), 'vert')]
    routes[2].voies[1].feux += [Feu(routes[2].voies[1], 2*width//3 - m2p(largeurVoie), 'vert')]
    routes[1].voies[0].feux += [Feu(routes[1].voies[0], height//3 - m2p(largeurVoie), 'rouge')]
    routes[1].voies[1].feux += [Feu(routes[1].voies[1], height//3 + m2p(largeurVoie), 'rouge')]
    
    routes[3].voies[0].feux += [Feu(routes[3].voies[0], width//3 + m2p(largeurVoie), 'vert')]
    routes[3].voies[1].feux += [Feu(routes[3].voies[1], width//3 - m2p(largeurVoie), 'vert')]
    routes[0].voies[0].feux += [Feu(routes[0].voies[0], 2*height//3 - m2p(largeurVoie), 'rouge')]
    routes[0].voies[1].feux += [Feu(routes[0].voies[1], 2*height//3 + m2p(largeurVoie), 'rouge')]
    
    routes[3].voies[0].feux += [Feu(routes[3].voies[0], 2*width//3 + m2p(largeurVoie), 'vert')]
    routes[3].voies[1].feux += [Feu(routes[3].voies[1], 2*width//3 - m2p(largeurVoie), 'vert')]
    routes[1].voies[0].feux += [Feu(routes[1].voies[0], 2*height//3 - m2p(largeurVoie), 'rouge')]
    routes[1].voies[1].feux += [Feu(routes[1].voies[1], 2*height//3 + m2p(largeurVoie), 'rouge')]
    
    global carrefours
    carrefours = [Carrefour([routes[2].voies[0].feux[0], routes[2].voies[1].feux[0]], [routes[0].voies[0].feux[0], routes[0].voies[1].feux[0]], dureeFeuVertM, dureeFeuVertM),
                  Carrefour([routes[2].voies[0].feux[1], routes[2].voies[1].feux[1]], [routes[1].voies[0].feux[0], routes[1].voies[1].feux[0]], dureeFeuVertM, dureeFeuVertM),
                  Carrefour([routes[3].voies[0].feux[0], routes[3].voies[1].feux[0]], [routes[0].voies[0].feux[1], routes[0].voies[1].feux[1]], dureeFeuVertM, dureeFeuVertM),
                  Carrefour([routes[3].voies[0].feux[1], routes[3].voies[1].feux[1]], [routes[1].voies[0].feux[1], routes[1].voies[1].feux[1]], dureeFeuVertM, dureeFeuVertM)]
    
    global proba, ptot
    proba = [.5,.05,.1,.01,.1,.04,.19,0.01]
    ptot = [0,0,0,0,0,0,0,0]
    
    global feux, voies
    feux = listeFeux()
    voies = listeVoies()


def listeVoitures():
    voitures = []
    for route in routes:
        for voie in route.voies:
            for voiture in voie.voitures:
                voitures.append(voiture)
    return voitures

def listeFeux():
    feux = []
    for route in routes:
        for voie in route.voies:
            for feu in voie.feux:
                feux.append(feu)
    return feux

def listeVoies():
    voies = []
    for route in routes:
        for voie in route.voies:
            voies.append(voie)
    return voies


def setup():
    size(900, 900)
    noStroke()
    rectMode(CENTER)
    
    init()
    
    global nVoitures, voituresRestantes
    nVoitures = 0 # Nombre de voitures creees
    voituresRestantes = n
    
    if utiliserFeuxManuels:
        actualiserFeuxM().start()
    else:
        global pop, simu
        pop = [[randint(0, 120) for i in range(len(feux)/2)] for i in range(taillePop)]
        index = 0
        scores = [0] * len(pop)


def draw():
    background(100)
    
    global voitures
    voitures = listeVoitures()
    
    global simu, pop
    
    afficherGrille()
    afficherRoutes()
    afficherFeux()
    creerVoitures()
    afficherVoitures()
    supprimerVoitures()
    
    if voituresRestantes == 0:
        scores[index] = (1/scores[index])**2 # Fonction d'evaluation
        print([ceil((float(x)/n)*100) for x in ptot])
    
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
    global nVoitures
    if nVoitures < n and randint(0, ceil(1/(vps*dt))) == 0:
        p = random(1)
        for i in range(len(voies)):
            if p < sum(proba[:i+1]):
                voie = voies[i]
                m = mM
                v = kmph2pps(vmaxS)
                a = 0
                amax = m2p(amaxM)
                tsecu = float(randint(10, 21)) / 10
                distmin = m2p(float(randint(5, 16)) / 10)
                longueur = m2p(longueurVoitureM)
                largeur = m2p(largeurVoitureM)
                coord = - m2p(v*tsecu)
                if voie.sens() == 'negatif':
                    coord = width + m2p(v*tsecu)
                if len(voie.voitures) == 0:
                    voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))
                    nVoitures += 1
                    ptot[i] += 1
                elif (voie.voitures[-1].coord > coord + voie.voitures[-1].longueur/2 + longueur/2 + distmin and voie.sens() == 'positif') or (voie.voitures[-1].coord < coord - voie.voitures[-1].longueur/2 - longueur/2 - distmin and voie.sens() == 'negatif'):
                    voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))
                    nVoitures += 1
                    ptot[i] += 1
                else:
                    coord = voie.voitures[-1].coord - voie.voitures[-1].longueur/2 - longueur/2 - distmin
                    if voie.sens() == 'negatif':
                        coord = voie.voitures[-1].coord + voie.voitures[-1].longueur/2 + longueur/2 + distmin
                    voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))
                    nVoitures += 1
                    ptot[i] += 1
                break


def supprimerVoitures():
    global voituresRestantes
    for voiture in voitures:
        if voiture.voie.sens() == 'positif' and voiture.coord > width + voiture.longueur/2:
            scores[index] += voiture.tsimu()
            voiture.voie.voitures.remove(voiture)
            voituresRestantes -= 1
        elif voiture.voie.sens() == 'negatif' and voiture.coord < 0 - voiture.longueur/2:
            scores[index] += voiture.tsimu()
            voiture.voie.voitures.remove(voiture)
            voituresRestantes -= 1


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
