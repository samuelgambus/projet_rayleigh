<<<<<<< HEAD
from passwd import Password
import string

#niveau 0 
"""
p = Password(0)
for c in string.ascii_lowercase:
    print(c)
    print(p.check(c))
"""
#niveau 1
"""
p = Password(1)
for c1 in string.ascii_lowercase:
    for c2 in string.ascii_lowercase:
        for c3 in string.ascii_lowercase:
            check=p.check([c1,c2,c3])
            #print (check )
            if check!=-1:
                print (check )
"""
#niveau 2
"""
p=Password(2)
for i in range(1000000):
    c=str(i)
    c=list(c)
    n=len(c)
    c=['0']*(6-n) + c
    check=p.check(c)
    if check!=-1:
        print (check )
"""
#niveau 3 
p = Password(3)
for i in range(32, 127):
    for j in range(32, 127):
        for k in range(32, 127):
            check=p.check([chr(i),chr(j),chr(k)])
            #print (check )
            if check!=-1:
                print (check )


=======
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
>>>>>>> 15bd2d9937f02cfb6c4a16910339e0a9907589fc

