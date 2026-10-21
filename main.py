from affichage import *
import numpy as np

############ Constantes de la simulation ############

tau = 360 #s
Nt = 2**16 #Nombre de pas de temps
Pr = 10
b = 8/3
q = np.pi/2
grid_length = 1000
grid_height = 1000

x = np.linspace(-2*np.pi/q,2*np.pi/q,grid_length)
y = np.linspace(0,1,grid_height)
X,Y = np.meshgrid(x,y) #renvoie les coordonnées réelles des éléments de la grille

psi = np.array([[0 for i in range(grid_length)] for j in range(grid_height)])

