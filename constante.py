import numpy as np

############ Constantes de la simulation ############

tau = 360 #s
Nt = 2**16 #Nombre de pas de temps
Pr = 10
b = 8/3
q = np.pi/np.sqrt(2)
r=30
h=tau/Nt
grid_length = 50
grid_height = 50