from settings import *
from environnement import *
from Voiture import *
from random import randint

class Simulation(object):
    def __init__(self, adn):
        self.adn = adn
        self.voituresRestantes = n
        self.voituresCreees = 0
        self.listeVoitures = []
        self.fitness = 0
    
    
    def update(self):
        voitures = []
        feux = []
        for route in routes:
            for voie in route.voies:
                voies.append(voie)
                for voiture in voie.voitures:
                    voitures.append(voiture)
        self.listeVoitures = voitures
    
    
    def run(self):
        while self.voituresRestantes != 0:
            background(100)
            
            self.update()
            
            self.afficherGrille()
            self.afficherRoutes()
            self.afficherFeux()
            self.creerVoitures()
            self.afficherVoitures()
            self.supprimerVoitures()
            
            sleep(dt)
        
        return self.fitness
    
    
    def afficherGrille(self):
        stroke(120)
        for i in range(height//m2p(mgrid)+1):
            line(0, i*m2p(mgrid), width, i*m2p(mgrid))
        for j in range(width//m2p(mgrid)+1):
            line(j*m2p(mgrid), 0, j*m2p(mgrid), height)
        noStroke()
    
    
    def afficherRoutes(self):
        for route in routes:
            route.afficher()
    
    
    def afficherFeux(self):
        for feu in feux:
            feu.afficher()
    
    
    def afficherVoitures(self):
        for voiture in self.listeVoitures:
            voiture.avancer()
            voiture.afficher()
    
    
    def creerVoitures(self):
        if self.voituresCreees < n and randint(0, ceil(1/(vps*dt))) == 0:
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
                        self.voituresCreees += 1
                        ptot[i] += 1
                    elif (voie.voitures[-1].coord > coord + voie.voitures[-1].longueur/2 + longueur/2 + distmin and voie.sens() == 'positif') or (voie.voitures[-1].coord < coord - voie.voitures[-1].longueur/2 - longueur/2 - distmin and voie.sens() == 'negatif'):
                        voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))
                        self.voituresCreees += 1
                        ptot[i] += 1
                    else:
                        coord = voie.voitures[-1].coord - voie.voitures[-1].longueur/2 - longueur/2 - distmin
                        if voie.sens() == 'negatif':
                            coord = voie.voitures[-1].coord + voie.voitures[-1].longueur/2 + longueur/2 + distmin
                        voie.voitures.append(Voiture(voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur))
                        self.voituresCreees += 1
                        ptot[i] += 1
                    break
    
    
    def supprimerVoitures(self):
        for voiture in self.listeVoitures:
            if voiture.voie.sens() == 'positif' and voiture.coord > width + voiture.longueur/2:
                self.fitness += voiture.tsimu()
                voiture.voie.voitures.remove(voiture)
                self.voituresRestantes -= 1
            elif voiture.voie.sens() == 'negatif' and voiture.coord < 0 - voiture.longueur/2:
                self.fitness += voiture.tsimu()
                voiture.voie.voitures.remove(voiture)
                self.voituresRestantes -= 1
