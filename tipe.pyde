from settings import *
from Feu import *
from Carrefour import *
from Voie import *
from Route import *
from Voiture import *

from threading import Thread, active_count
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
    
    global proba
    proba = [.05, .1, .1, .2, .1, .3, .05, .1] # Dans l'ordre : gauche droite puis haut bas
    
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
    size(1000, 1000)
    noStroke()
    rectMode(CENTER)
    
    init()
    
    global nVoitures, voituresRestantes
    nVoitures = 0 # Nombre de voitures creees
    voituresRestantes = n
    
    if utiliserFeuxManuels:
        actualiserFeuxM().start()
    else:
        global generation, pop, scores, index
        generation = 0
        pop = [[(randint(1, dureeFeuRougeMax), randint(1, dureeFeuRougeMax), randint(0 ,1)) for i in range(len(feux)//4)] for i in range(taillePop)] # DureeFeuVert, dureeFeuRouge, 0 pour x vert en premier ou 1 pour y vert en premier
        scores = [0] * taillePop
        index = 0
        print('============================== GENERATION 0 ==============================')
        print(pop)
        dureeGeneration = millis()
        print('============================== Simulation 1 ==============================')
        print(pop[index])
        dureeSimulation = millis()
        for i in range(len(carrefours)):
            carrefours[i].dureeFeuVertX, carrefours[i].dureeFeuRougeX = pop[0][i][:2]
            actualiserFeux(carrefours[i], 0, pop[0][i][2]).start()


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
    
    # print(active_count())
    
    global scores, index, voituresRestantes, nVoitures, pop, generation, dureeSimulation
    if voituresRestantes == 0 and not(utiliserFeuxManuels):
        print('Duree de la simulation : ' + str((millis()-dureeSimulation)//(1000*60)) + ' minutes')
        print('Temps passe par les voitures dans la simulation : ' + str(scores[index]/n) + ' secondes en moyenne')
        scores[index] = (1000./(scores[index]/n))**4 # Fonction d'evaluation
        print('Score : ' + str(int(scores[index])))
        if index + 1 < taillePop: # S'il reste encore au moins une simulation a effectuer dans la population
            index += 1
            nVoitures = 0
            voituresRestantes = n
            print('============================== Simulation ' + str(index+1) + ' ==============================')
            print(pop[index])
            dureeSimulation = millis()
            for i in range(len(carrefours)):
                carrefours[i].dureeFeuVertX, carrefours[i].dureeFeuRougeX = pop[index][i][:2]
                actualiserFeux(carrefours[i], index, pop[index][i][2]).start()
        else: # Reproduction/Selection
            global dureeGeneration
            print('================================= Scores =================================')
            print(str((millis()-dureeGeneration)//(1000*60)) + ' minutes')
            print([int(score) for score in scores])
            generation += 1
            print('============================== GENERATION ' + str(generation) + ' ==============================')
            nouvellePop = []
            parents = []
            for j in range(taillePop):
                # Choix des parents (ici 2 parents et differents)
                parent1 = -1
                parent2 = -1
                p = random(1)
                for i in range(taillePop):
                    if p < sum(scores[:i+1])/sum(scores):
                        parent1 = i
                        break
                while parent2 == parent1 or parent2 == -1:
                    p = random(1)
                    for i in range(taillePop):
                        if p < sum(scores[:i+1])/sum(scores):
                            parent2 = i
                            break
                parents.append((parent1, parent2))
                
                fils = []
                # Reproduction (1 allele sur deux)
                for i in range(len(carrefours)):
                    if i % 2 == 0:
                        fils.append((pop[parent1][i][0], pop[parent2][i][1], pop[parent1][i][2]))
                    else:
                        fils.append((pop[parent2][i][0], pop[parent1][i][1], pop[parent2][i][2]))
                nouvellePop.append(fils)
            
            print([(a+1, b+1) for (a, b) in parents])
            
            # Mutation
            for fils in nouvellePop:
                for i in range(len(fils)):
                    for j in range(3):
                        if random(1) < mutation:
                            print('*mutation*')
                            carrefour = list(fils[i])
                            if j != 2:
                                carrefour[j] = randint(1, dureeFeuRougeMax)
                            else:
                                carrefour[j] = randint(0, 1)
                            fils[i] = tuple(carrefour)
            
            pop = nouvellePop
            scores = [0] * taillePop
            index = 0
            for i in range(len(carrefours)):
                carrefours[i].dureeFeuVertX, carrefours[i].dureeFeuRougeX = pop[index][i][:2]
                actualiserFeux(carrefours[i], index, pop[index][i][2]).start()
            nVoitures = 0
            voituresRestantes = n
            print(pop)
            dureeGeneration = millis()
            print('============================== Simulation ' + str(index+1) + ' ==============================')
            print(pop[index])
            dureeSimulation = millis()
    
    # print('a')
    # t = millis()
    # print(t)
    sleep(dt/vitesseSimu)
    # print(millis()-t)


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
    global nVoitures, vitesseSimu
    if nVoitures < n and randint(0, ceil(1/(vps*dt/vitesseSimu))) == 0:
        p = random(1)
        for i in range(len(voies)):
            if p < sum(proba[:i+1]):
                voie = voies[i]
                m = mM
                v = kmph2pps(vmaxS)
                a = 0
                amax = m2p(amaxM)
                tsecu = float(randint(15, 26)) / 10
                distmin = m2p(float(randint(5, 16)) / 10)
                longueur = m2p(longueurVoitureM)
                largeur = m2p(largeurVoitureM)
                coord = - m2p(v*tsecu)
                if voie.sens() == 'negatif':
                    coord = width + m2p(v*tsecu)
                if len(voie.voitures) == 0:
                    voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))
                    nVoitures += 1
                elif (voie.voitures[-1].coord > coord + voie.voitures[-1].longueur/2 + longueur/2 + distmin and voie.sens() == 'positif') or (voie.voitures[-1].coord < coord - voie.voitures[-1].longueur/2 - longueur/2 - distmin and voie.sens() == 'negatif'):
                    voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))
                    nVoitures += 1
                else:
                    coord = voie.voitures[-1].coord - voie.voitures[-1].longueur/2 - longueur/2 - distmin
                    if voie.sens() == 'negatif':
                        coord = voie.voitures[-1].coord + voie.voitures[-1].longueur/2 + longueur/2 + distmin
                    voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))
                    nVoitures += 1
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

class actualiserFeux(Thread):
    def __init__(self, carrefour, index, p):
        Thread.__init__(self)
        self.carrefour = carrefour
        self.index = index
        if p == 0:
            self.feuxP = self.carrefour.feuxX
            self.feuxD = self.carrefour.feuxY
            self.dureeFeuVertP = self.carrefour.dureeFeuVertX
            self.dureeFeuVertD = self.carrefour.dureeFeuRougeX
        else:
            self.feuxP = self.carrefour.feuxY
            self.feuxD = self.carrefour.feuxX
            self.dureeFeuVertP = self.carrefour.dureeFeuRougeX
            self.dureeFeuVertD = self.carrefour.dureeFeuVertX
        
    
    def run(self):
        global index
        while self.index == index:
            for feu in self.feuxD:
                feu.passeRouge()
            sleep((dureeFeuOrange + dureeRougeDeDegagement)/vitesseSimu)
            if self.index == index:
                for feu in self.feuxP:
                    feu.passeVert()
                sleep(self.dureeFeuVertP/vitesseSimu)
            if self.index == index:
                for feu in self.feuxP:
                    feu.passeRouge()
                sleep((dureeFeuOrange + dureeRougeDeDegagement)/vitesseSimu)
            if self.index == index:
                for feu in self.feuxD:
                    feu.passeVert()
                sleep(self.dureeFeuVertD/vitesseSimu)


class actualiserFeuxM(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            sleep(dureeFeuVertM/vitesseSimu)
            feuxVert = [feu for feu in feux if feu.etat == 'vert']
            feuxRouge = [feu for feu in feux if feu.etat == 'rouge']
            for feu in feuxVert:
                feu.passeRouge()
            sleep((dureeFeuOrange + dureeRougeDeDegagement)/vitesseSimu)
            for feu in feuxRouge:
                feu.passeVert()
