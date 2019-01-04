from settings import *

class Voiture(object):
    def __init__(self, voie, m, coord, v, a, amax, tsecu, distmin, longueur, largeur):
        self.voie = voie # Voie sur laquelle est la voiture
        self.m = m # Masse de la voiture (en kg)
        self.coord = coord # Coordonnee de la voiture sur la voie (en pixel)
        self.v = v # Vitesse (en pixel/s)
        self.a = a # Acceleration (en pixel/s2)
        self.amax = amax # Acceleration maximum (en pixel/s2)
        self.tsecu = tsecu # Temps de reaction (en s)
        self.distmin = distmin # Distance minimum avec le vehicule devant (utile notament a l'arret) (en pixel)
        self.longueur = longueur # (en pixel)
        self.largeur = largeur # (en pixel)
        self.distsecu = self.v * self.tsecu # Distance de securite avec le vehicule devant (en pixel)
        self.__feuDevant = -1 # Feu devant (-1 si aucun)
        self.__passe_orange = False # Variable indiquant si la voiture compte passer a l'orange
        self.__tcreation = -1 # Temps ou la voiture a ete creee (en s)
    
    def tsimu(self):
        return (millis()-self.__tcreation)//1000
    
    def __couleur(self):
        i = map(self.v, 0, kmph2pps(vmaxS), 0, 255)
        
        if i < 160:
            r = 255
            g = 255 * (i/160)
        elif i < 224:
            r = 255 * (1 - (i-160)/(224-160))
            g = 255
        else:
            r = 0
            g = 255
        
        if i < 100:
            b = 0
        elif i < 175:
            b = (i-100)*110/(175-100)
        else:
            b = 110 * (1 - (i-175)/(255-175))
        
        return r, g, b
    
    
    def __voitureDevantD(self): # Renvoie la voiture devant, et la distance entre le capot et l'arriere (en pixel)
        dmin = 0
        voitureDevant = self
        
        if self.voie.sens() == 'positif':
            for voiture in self.voie.voitures:
                d = voiture.coord - self.coord
                if 0 < d < dmin or (d > 0 and dmin == 0):
                    dmin = d
                    voitureDevant = voiture
        else:
            for voiture in self.voie.voitures:
                d = self.coord - voiture.coord
                if 0 < d < dmin or (d > 0 and dmin == 0):
                    dmin = d
                    voitureDevant = voiture
        
        return voitureDevant, dmin - self.longueur/2 - voitureDevant.longueur/2


    def __feuDevantD(self): # Renvoie le feu devant, et la distance entre le capot et le feu (en pixel)
        dmin = 0
        feuDevant = -1
        
        if self.voie.sens() == 'positif':
            for feu in self.voie.feux:
                d = feu.coord - self.coord
                if 0 < d < dmin or (d > 0 and dmin == 0):
                    dmin = d
                    feuDevant = feu
        else:
            for feu in self.voie.feux:
                d = self.coord - feu.coord
                if 0 < d < dmin or (d > 0 and dmin == 0):
                    dmin = d
                    feuDevant = feu
        
        return feuDevant, dmin - self.longueur/2


    def avancer(self):
        voitureDevantD = self.__voitureDevantD()
        feuDevantD = self.__feuDevantD()
        
        voitureDevant = voitureDevantD[0]
        distVoitureDevant = voitureDevantD[1]
        feuDevant = feuDevantD[0]
        distFeuDevant = feuDevantD[1]
        sens = 1
        
        if self.voie.sens() == 'negatif':
            sens = -1
        
        if self.v < kmph2pps(vmaxS): # Si la voiture ne roule pas a la vitesse max, elle accelere
            self.a = self.amax
        else: # Si elle est a la vitesse max, elle arrete d'accelerer
            self.a = 0
            self.v = kmph2pps(vmaxS)
    
        if 0 < self.distmin < distVoitureDevant < self.distsecu: # Si la voiture ne respecte pas les distances de securite, elle ralentie
            self.a = - self.v**2/(2*(distVoitureDevant - self.distmin))
        
        if 0 < distVoitureDevant <= self.distmin: # Si on est trop proche de la voiture de devant, on s'arrete
            self.a = 0
            self.v = 0

        if 0 < distFeuDevant and (distFeuDevant < distVoitureDevant or voitureDevant == self or voitureDevant.__passe_orange == True): # Si il y a un feu devant et qu'on est en tete de file ou que la voiture devant compte passer a l'orange
            if feuDevant != self.__feuDevant: # Si on depasse un feu, on remet la variable passe_orange a sa valeur par defaut
                self.__passe_orange = False
            
            if 0 < distFeuDevant < self.distsecu + self.v**2/(2*m2p(9.81)*0.8): # Des qu'on a plus la distance pour freiner (v**2/2gu)
                if feuDevant.etat == 'rouge': # Si le feu est rouge, on ralentit
                    self.a = - self.v**2/(2*(distFeuDevant - self.distmin))
                if feuDevant.etat == 'orange' and self.__passe_orange == False: # Si il est orange et qu'on s'arrete a l'orange, on ralentit
                    self.a = - self.v**2/(2*(distFeuDevant - self.distmin))
                if feuDevant.etat == 'vert': # Si il est vert, alors on passe la variable passe_orange a False puisqu'on aura alors pas le temps de freiner si le feu passe a l'orange
                    self.__passe_orange = True
            
            if 0 < distFeuDevant < self.distmin and feuDevant.etat == 'rouge': # Si le feu est rouge et qu'on est tres proche, on s'arrete
                self.a = 0
                self.v = 0
            
            if 0 < distFeuDevant < self.distmin and feuDevant.etat == 'orange' and self.__passe_orange == False: # Pareil si le feu est orange et que passe_orange est a False
                self.a = 0
                self.v = 0
        
        
        
        self.v += dt * self.a # Enfin on calcul vitesse et coordonnees en tenant compte de l'orientation
        if self.v < 0:
            self.v = 0
        self.coord += sens * dt * self.v
        self.distsecu = self.tsecu * self.v # On reactualise la distance de securite
        self.__feuDevant = feuDevant # On reactualise la variable __feuDevant
        if self.__tcreation == -1 and 0 < self.coord + self.longueur/2 < width + self.longueur:
            self.__tcreation = millis()
        
    
    def afficher(self):
        r, g, b = self.__couleur()
        fill(r, g, b)
        
        if self.voie.route.axe == 'x':
            rect(self.coord, self.voie.coord, self.longueur, self.largeur)
        else:
            rect(self.voie.coord, self.coord, self.largeur, self.longueur)
            
