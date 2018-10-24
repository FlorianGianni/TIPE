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
dureeRougeDeDepassement = float(2*largeurVoie)/1 # Duree pendant laquelle tous les feux sont rouges (1 m/s pour les pietons en France)
utiliserFeuxManuels = True # Utiliser les feux avec sequences predefinies ?

def p2m(p): # Pixel vers metre
    return p // ppm

def m2p(m): # Metre vers pixel
    return m * ppm
