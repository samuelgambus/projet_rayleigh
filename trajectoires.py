from integration import *
import matplotlib.pyplot as plt

def euler(x0,y0,X):
    x = [x0]
    z = [y0]
    for i in range(Nt):
        u = np.pi * np.sin(np.pi * z[i]) * np.sin(q*x[i]) * X[i]
        v = q * np.cos(np.pi * z[i]) * np.cos(q*x[i]) * X[i]
        x.append(x[i] + h * u)
        z.append(z[i] + h * v)

    plt.plot(x,z)
    plt.show()
"""
X = np.array(integration(1,1,1,10))[:,0]
euler(1,0,X)
Ca marche pas ya un carré c pas physique
"""

def g(x,z,i,X):
    if i.is_integer():
        Xi = X[i]
    else:
        Xi = (X[int(i-1/2)] + X[int(i+1/2)])/2
    u = np.pi * np.sin(np.pi * z) * np.sin(q*x) * Xi
    v = q * np.cos(np.pi * z) * np.cos(q*x) * Xi
    return (u,v)


def runge_kutta_traj(x,z,i,X):
    k1 = g(x,z,i,X)

    k2 = g(x + (h/2)*k1[0],z + (h/2)*k1[1],i+1/2,X)

    k3 = g(x + (h/2)*k2[0],z + (h/2)*k2[1],i+1/2,X)

    k4 = g(x + h*k2[0],z + h*k2[1],i+1,X)

    return (x + (h/6)*(k1[0]+2*k2[0]+2*k3[0]+k4[0]), z + (h/6)*(k1[1]+2*k2[1]+2*k3[1]+k4[1]))

def integration_traj(x0,z0,X): ## Intègre le système 4 entre le temps 0 et tau (définie en constante)
    tab=[[x0,z0]]
    for i in range(Nt):
        tab.append(list(runge_kutta_traj(tab[i][0],tab[i][1],i,X)))
    return tab

X = np.array(integration(1,1,1,28))[:,0]
tab = integration_traj(1,0,X)
x = [p[0] for p in tab]
z = [p[1] for p in tab]
plt.plot(x,z)
plt.show()