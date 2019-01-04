ppm = 2 # Taille d'un metre en pixel (en pixel/m)
largeurVoie = 3 # Largeur d'une voie en France (3.50 normalement) (en m)
largeurLigneContinue = 0.15 # Largeur d'une ligne continue en France (en m)
dessinerLignesContinues = False # Dessiner les lignes continues ?
largeurLigneEffetDeFeux = 0.15 # Largeur d'une ligne d'effet de feux en France (en m)
longueurLigneEffetDeFeux = .50 # Longueur d'une ligne d'effet de feux en France (en m)
dessinerLignesEffetsDeFeux = False # Dessiner les lignes d'effet de feux ?
dureeFeuOrange = 3 # Duree du feu orange (entre 3 et 5 s)
mgrid = 10 # Longueur du cote d'un carre de l'echelle (en m)
dt = 0.03 # Periode de la simulation
dureeFeuVertM = 30 # Duree de feu vert en mode manuel
dureeFeuRougeMax = 120 # Duree de feu rouge maximale
dureeRougeDeDegagement = ceil(float(2*largeurVoie)/1) # Duree pendant laquelle tous les feux sont rouges (1 m/s pour les pietons en France)
utiliserFeuxManuels = False # Utiliser les feux avec sequences predefinies ?
mM = 1000 # Masse moyenne d'une voiture (en kg)
vmaxS = 50 # Vitesse maximale de toute la simulation (en km/h)
amaxM = 3 # Acceleration moyenne d'une voiture (en m/s2)
longueurVoitureM = 4 # Longueur moyenne d'une voiture (en m)
largeurVoitureM = 2 # Largeur moyenne d'une voiture (en m)
vps = 30 # Voitures par seconde
n = 100 # Nombre de voiture pour une simulation
taillePop = 9 # Taille de la population (> 1)
mutation = 0.01 # Taux de mutation

def p2m(p): # Pixel vers metre
    return p // ppm

def m2p(m): # Metre vers pixel
    return m * ppm

def mps2kmph(v): # m/s vers km/h
    return v * 3.6

def kmph2mps(v): # km/h vers m/s
    return v / 3.6

def mps2pps(v): # m/s vers pixel/s
    return m2p(v)

def kmph2pps(v): # km/h vers pixel/s
    return mps2pps(kmph2mps(v))
