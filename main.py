from affichage import *
from constante import *
from integration import *
import numpy as np

x_ = np.linspace(-2*np.pi/q,2*np.pi/q,grid_length)
z_ = np.linspace(-1/2,1/2,grid_height)
x,z = np.meshgrid(x_,z_) #renvoie les coordonnées réelles des éléments de la grille

psi = np.array([[0 for _ in range(grid_length)] for _ in range(grid_height)])
theta = np.array([[0 for _ in range(grid_length)] for _ in range(grid_height)])

U = u(x,z,q,X0)
V = v(x,z,q,X0)

w = (np.pi**2 + q**2)*psi #rotationnel du champ de vitesse


#afficher_vort_et_vitesse(x,z,U,V )
#afficher_theta_et_vitesse(x,z,U,V)

tab = integration(1,0,0,28)
X,Y,Z = zip(*tab)

t = temp(x,z,q,Y,Z)


