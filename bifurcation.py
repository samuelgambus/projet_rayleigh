from constante import *
from integration import *
import matplotlib.pyplot as plt

def bifurcation_stable(N=50):
    """comp = 0 pour X, 1 pour Y, 2 pour Z"""
    rs = np.linspace(0, 30, 100)
    noms = ['X', 'Y', 'Z']

    fig, ax = plt.subplots(figsize=(12, 5))
    for X0, couleur, label in [(1, 'tab:blue', 'CI : X0 = +1'),
                               (-1, 'tab:red', 'CI : X0 = -1')]:
        R, V = [], []
        for r in rs:
            T = np.array(integration(X0, 0, 0, r))          # shape (Nt+1, 3)
            V.append(T[-N:, 0])                # N derniers points
            R.append(np.full(N, r))
        ax.plot(np.concatenate(R), np.concatenate(V), '.', color=couleur, markersize=2, alpha=0.6, label=label)

    ax.set_xlabel('r')
    ax.set_ylabel(noms[0])
    ax.set_title(f'Diagramme de bifurcation ({noms[0]}, {N} derniers points)')
    ax.legend(markerscale=5)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def maxima_locaux(Z): #garde les maximas locaux d'une liste
    Z_max = []
    for i in range(1,len(Z) - 1):
        if Z[i]>Z[i-1] and Z[i]>Z[i+1]:
            Z_max.append(Z[i])
    return Z_max

def bifurcation_chaos(Np): # Affcihe les maximas 
    fig, ax = plt.subplots(figsize=(12, 5))

    R, V = [], []
    for r in np.linspace(30,350,100):
        T = np.array(integration(1, 0, 0, r))         # shape (Nt+1, 3)
        V.append(maxima_locaux(T[:, 2] - r)[-Np:])                # Np derniers maxima
        R.append(np.full(Np, r))
    ax.plot(np.concatenate(R), np.concatenate(V), '.', color='blue', markersize=2, alpha=0.6)

    ax.set_xlabel('r')
    ax.set_ylabel('Zmax - r')
    ax.set_title(f'Diagramme de bifurcation ( {Np} derniers points)')
    ax.legend(markerscale=5)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

bifurcation_stable(50)