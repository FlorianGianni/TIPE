from settings import *
from Feu import *
from Voie import *
from Route import *
from Voiture import *

from time import sleep

def setup():
    size(900, 900)
    noStroke()
    rectMode(CENTER)
    
    global routes
    routes = [
              Route('x', height//3), 
              Route('x', 2*height//3), 
              Route('y', width//3), 
              Route('y', 2*width//3)
              ]

def draw():
    background(100)
    afficherGrille()
    afficherRoutes()
    
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
