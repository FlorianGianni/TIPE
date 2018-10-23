ppm = 2 # Taille d'un metre en pixel (en pixel/m)
largeurVoie = 3 # Largeur d'une voie en France (3.5 normalement) (en m)
largeurLigneContinue = 0.15 # Largeur d'une ligne continue en France (en m)
dessinerLignesContinues = False # Dessiner les lignes continues ?
mgrid = 10 # Longueur du cote d'un carre de l'echelle (en m)
dt = 0.03 # Periode de la simulation

def p2m(p): # Pixel vers metre
    return p // ppm

def m2p(m): # Metre vers pixel
    return m * ppm
