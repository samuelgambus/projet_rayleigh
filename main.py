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

x_ = np.linspace(-2*np.pi/q,2*np.pi/q,grid_length)
z_ = np.linspace(0,1,grid_height)
x,z = np.meshgrid(x_,z_) #renvoie les coordonnées réelles des éléments de la grille

psi = np.array([[0 for _ in range(grid_length)] for _ in range(grid_height)])
theta = np.array([[0 for _ in range(grid_length)] for _ in range(grid_height)])

U = u(x,z,q,X0)
V = v(x,z,q,X0)

w = (np.pi**2 + q**2)*psi #rotationnel du champ de vitesse




