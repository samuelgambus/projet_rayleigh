from affichage import *
import numpy as np

############ Constantes de la simulation ############

tau = 360 #s
Nt = 2**16 #Nombre de pas de temps
Pr = 10
b = 8/3
q = np.pi/2
grid_length = 50
grid_height = 50

x = np.linspace(-2*np.pi/q,2*np.pi/q,grid_length)
z = np.linspace(0,1,grid_height)
X,Z = np.meshgrid(x,z) #renvoie les coordonnées réelles des éléments de la grille

psi = np.array([[0 for _ in range(grid_length)] for _ in range(grid_height)])

U = u(X,Z,q,X0)
V = v(X,Z,q,X0)

afficher(X,Z,U,V)