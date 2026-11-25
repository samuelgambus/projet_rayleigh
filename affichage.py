import matplotlib.pyplot as plt
import numpy as np
from constante import *
from integration import * 

#on suppose X(t) = X0 constant
#on définit ici les fonction u et v avec X0 constant


def u(x, z, q, X0):
    return X0 * np.pi * np.sin(np.pi * z) * np.sin(q * x)

def v(x, z, q, X0):
    return X0 * q * np.cos(np.pi * z) * np.cos(q * x)

def vort(x, z, q, X0):
    return (np.pi**2 + q**2) * X0 * np.cos(np.pi * z) * np.sin(q * x)

def temp(x, z, q, Y, Z):
    return Y * np.cos(np.pi * z) * np.cos(q * x) + Z * np.sin(2 * np.pi * z)

def afficher_vorti_temp_cst(X, Z, U, V, q, X0, Y0, Z0, pas_q=6):
    bg_color = "#171d26"
    text_color = "#f1f5f9"

    Xq, Zq = X[::pas_q, ::pas_q], Z[::pas_q, ::pas_q]
    Uq, Vq = U[::pas_q, ::pas_q], V[::pas_q, ::pas_q]
    max_speed = max(np.max(np.hypot(Uq, Vq)), 1e-6)
    arrow_scale = max_speed * 7.5

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=bg_color)

    # --- Graphique 1 (en haut) : Vorticité et champ de vitesse ---
    ax1.set_facecolor(bg_color)
    mesh1 = ax1.pcolormesh(
        X, Z, vort(X, Z, q, X0), shading="gouraud", cmap="coolwarm"
    )
    cbar1 = fig.colorbar(mesh1, ax=ax1, label="Vorticité")
    cbar1.ax.yaxis.label.set_color(text_color)
    cbar1.ax.tick_params(colors=text_color)

    ax1.quiver(
        Xq,
        Zq,
        Uq,
        Vq,
        color="#0f172a",
        scale=arrow_scale,
        scale_units="xy",
        width=0.003,
    )
    ax1.set_title(f"Vorticité et champ de vitesse (X0 = {X0})", color=text_color)
    ax1.set_xlabel("x", color=text_color)
    ax1.set_ylabel("z", color=text_color)
    ax1.tick_params(colors=text_color)

    # --- Graphique 2 (en bas) : Température et champ de vitesse ---
    ax2.set_facecolor(bg_color)
    mesh2 = ax2.pcolormesh(
        X, Z, temp(X, Z, q, Y0, Z0), shading="gouraud", cmap="inferno"
    )
    cbar2 = fig.colorbar(mesh2, ax=ax2, label="Écart de température theta")
    cbar2.ax.yaxis.label.set_color(text_color)
    cbar2.ax.tick_params(colors=text_color)

    ax2.quiver(
        Xq,
        Zq,
        Uq,
        Vq,
        color="#f8fafc",
        scale=arrow_scale,
        scale_units="xy",
        width=0.003,
    )
    ax2.set_title(
        f"Température et champ de vitesse (Y0 = {Y0}, Z0 = {Z0})", color=text_color
    )
    ax2.set_xlabel("x", color=text_color)
    ax2.set_ylabel("z", color=text_color)
    ax2.tick_params(colors=text_color)

    plt.tight_layout()
    plt.show()


# --- Paramètres et grille ---
X0, Y0, Z0 = 1, 1, 1
q = np.pi / 2
grid_length = 120
grid_height = 120

x_ = np.linspace(-2 * np.pi / q, 2 * np.pi / q, grid_length)
z_ = np.linspace(0, 1, grid_height)
X, Z = np.meshgrid(x_, z_)
U = u(X, Z, q, X0)
V = v(X, Z, q, X0)

#AFFICHAAAAAAAAAAAAGE##################################################
afficher_vorti_temp_cst(X, Z, U, V, q, X0, Y0, Z0)




# --- Fonctions adaptées avec les valeurs à l'instant t ---
#def u(x,z,q, X0):
    #return X0*np.pi*np.sin(np.pi*z)*np.sin(q*x)

def u(x, z, q, X_t):
    return X_t * np.pi * np.sin(np.pi * z) * np.sin(q * x)

def v(x, z, q, X_t):
    return X_t * q * np.cos(np.pi * z) * np.cos(q * x)

def vort(x, z, q, X_t):
    return np.pi**2 * X_t * np.cos(np.pi * z) * np.sin(q * x) + q**2 * X_t * np.cos(np.pi * z) * np.sin(q * x)

def temp(x, z, q, Y_t, Z_t):
    return Y_t * np.cos(np.pi * z) * np.cos(q * x) + Z_t * np.sin(2 * np.pi * z)

def afficher_physique_instant(traj, n, q, r=None):
    bg_color = "#171d26"
    text_color = "#f1f5f9"

    # Récupération des valeurs de X, Y, Z à l'instant t_n
    X_n = traj[n][0]
    Y_n = traj[n][1]
    Z_n = traj[n][2]

    # Définition de l'espace physique (selon le sujet : x dans [-2*pi/q, 2*pi/q] et z dans [0, 1])
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 40)
    z_vals = np.linspace(0, 1, 40)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)

    # Calcul des champs sur la grille
    U = u(X_grid, Z_grid, q, X_n)
    V = v(X_grid, Z_grid, q, X_n)
    Vort_grid = vort(X_grid, Z_grid, q, X_n)
    Theta_grid = temp(X_grid, Z_grid, q, Y_n, Z_n)

    suffix_r = f", r={r}" if r is not None else ""

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=bg_color)

    # --- Graphique 1 : Vorticité et Champ de vitesse ---
    ax1.set_facecolor(bg_color)
    mesh1 = ax1.pcolormesh(X_grid, Z_grid, Vort_grid, shading="auto", cmap="coolwarm")
    cbar1 = fig.colorbar(mesh1, ax=ax1, label="Vorticité")
    cbar1.ax.yaxis.label.set_color(text_color)
    cbar1.ax.tick_params(colors=text_color)

    ax1.quiver(X_grid, Z_grid, U, V, color="black")
    ax1.set_title(f"Vorticité et Vitesse (instant n={n}, r=28)", color=text_color)
    ax1.set_xlabel("x", color=text_color)
    ax1.set_ylabel("z", color=text_color)
    ax1.tick_params(colors=text_color)

    # --- Graphique 2 : Température et Champ de vitesse ---
    ax2.set_facecolor(bg_color)
    mesh2 = ax2.pcolormesh(X_grid, Z_grid, Theta_grid, shading="auto", cmap="inferno")
    cbar2 = fig.colorbar(mesh2, ax=ax2, label="Écart de température theta")
    cbar2.ax.yaxis.label.set_color(text_color)
    cbar2.ax.tick_params(colors=text_color)

    ax2.quiver(X_grid, Z_grid, U, V, color="white")
    ax2.set_title(f"Température et Vitesse (instant n={n}, r=28)", color=text_color)
    ax2.set_xlabel("x", color=text_color)
    ax2.set_ylabel("z", color=text_color)
    ax2.tick_params(colors=text_color)

    plt.tight_layout()
    plt.show()

# 1. Récupérer une trajectoire (ex. avec ta fonction existante)
traj = integration(X0, Y0, Z0, r)

# 2. Choisir l'indice de l'instant n et le paramètre q
n = 50  # doit vérifier : 0 <= n < len(traj)
q = np.pi / 2  # exemple classique pour le modèle de Lorenz / convection

# 3. Lancer l'affichage
afficher_physique_instant(traj, n, q)



# Paramètre du nombre d'onde q donné dans le sujet


# Condition initiale et paramètres
X0, Y0, Z0 = 1.0, 1.0, 1.0

# --- Cas r = 10 (Régime stable / stationnaire) ---
print("Calcul pour r = 10...")
traj_r10 = integration(X0, Y0, Z0, r=10)
# On prend un instant vers la fin de la simulation (ex: le dernier point -1)
#afficher_physique_instant(traj_r10, -1, q)

# --- Cas r = 28 (Régime chaotique) ---
print("Calcul pour r = 28...")
traj_r28 = integration(X0, Y0, Z0, r=28)
# En régime chaotique, les mouvements changent tout le temps, vous pouvez tester différents indices n (ex: 100, 500, -1)
#afficher_physique_instant(traj_r28, -1, q)



import matplotlib.pyplot as plt
import numpy as np


def afficher_vorticite_instants(traj, instants, q, r=None, pas_q=6):
    bg_color = "#171d26"
    text_color = "#f1f5f9"
    suffix_r = f", r={r}" if r is not None else ""

    # Grille fine pour un rendu lisse
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 120)
    z_vals = np.linspace(0, 1, 120)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)

    # Grille espacée pour les flèches
    Xq, Zq = X_grid[::pas_q, ::pas_q], Z_grid[::pas_q, ::pas_q]

    # Calcul des champs pour les instants choisis
    champs = []
    for n in instants:
        X_n = traj[n][0]
        Vort_n = vort(X_grid, Z_grid, q, X_n)
        Uq_n = u(Xq, Zq, q, X_n)
        Vq_n = v(Xq, Zq, q, X_n)
        champs.append((n, Vort_n, Uq_n, Vq_n))

    # Échelle commune de vorticité et de flèches sur les 3 instants comparés
    vmin = min(np.min(item[1]) for item in champs)
    vmax = max(np.max(item[1]) for item in champs)
    max_speed = max(max(np.max(np.hypot(item[2], item[3])), 1e-6) for item in champs)
    arrow_scale = max_speed * 7.5

    fig, axes = plt.subplots(1, len(instants), figsize=(18, 4.8), facecolor=bg_color)
    if len(instants) == 1:
        axes = [axes]

    for ax, (n, Vort_n, Uq_n, Vq_n) in zip(axes, champs):
        ax.set_facecolor(bg_color)
        mesh = ax.pcolormesh(
            X_grid, Z_grid, Vort_n, shading="gouraud", cmap="coolwarm", vmin=vmin, vmax=vmax
        )
        cbar = fig.colorbar(mesh, ax=ax, label="Vorticité")
        cbar.ax.yaxis.label.set_color(text_color)
        cbar.ax.tick_params(colors=text_color)

        ax.quiver(
            Xq,
            Zq,
            Uq_n,
            Vq_n,
            color="#0f172a",
            scale=arrow_scale,
            scale_units="xy",
            width=0.003,
        )

        ax.set_title(f"Vorticité — instant n={n}{suffix_r}", color=text_color)
        ax.set_xlabel("x", color=text_color)
        ax.set_ylabel("z", color=text_color)
        ax.tick_params(colors=text_color)

    plt.tight_layout()
    plt.show()



import matplotlib.animation as animation


def animer_lorenz_rapide(
    traj, q, r=28, max_frames=250, pas_q=6, interval=40, save_path=None
):
    bg_color = "#171d26"
    text_color = "#f1f5f9"
    suffix_r = f", r={r}" if r is not None else ""

    n_final = len(traj) - 1
    nb_frames = min(max_frames, len(traj))
    indices = np.unique(np.linspace(0, n_final, nb_frames, dtype=int))

    # Grille fine pour le fond et grille espacée pour les flèches
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 120)
    z_vals = np.linspace(0, 1, 120)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)

    Xq, Zq = X_grid[::pas_q, ::pas_q], Z_grid[::pas_q, ::pas_q]

    # Estimation rapide des bornes et de l'échelle des flèches sur les frames échantillonnées
    sample_idx = indices[:: max(1, len(indices) // 40)]
    vort_min, vort_max = np.inf, -np.inf
    theta_min, theta_max = np.inf, -np.inf
    max_speed = 1e-6

    for k in sample_idx:
        Xk, Yk, Zk = traj[k][0], traj[k][1], traj[k][2]
        vk = vort(X_grid, Z_grid, q, Xk)
        tk = temp(X_grid, Z_grid, q, Yk, Zk)
        uk = u(Xq, Zq, q, Xk)
        vk_vel = v(Xq, Zq, q, Xk)

        vort_min, vort_max = min(vort_min, np.min(vk)), max(vort_max, np.max(vk))
        theta_min, theta_max = min(theta_min, np.min(tk)), max(theta_max, np.max(tk))
        max_speed = max(max_speed, np.max(np.hypot(uk, vk_vel)))

    arrow_scale = max_speed * 7.5

    # État initial (n = indices[0] = 0) — une seule figure avec 2 sous-graphiques superposés
    X0_n, Y0_n, Z0_n = traj[indices[0]]
    Vort0 = vort(X_grid, Z_grid, q, X0_n)
    Theta0 = temp(X_grid, Z_grid, q, Y0_n, Z0_n)
    Uq0 = u(Xq, Zq, q, X0_n)
    Vq0 = v(Xq, Zq, q, X0_n)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=bg_color)

    # --- Graphique 1 (en haut) : Vorticité et Vitesse ---
    ax1.set_facecolor(bg_color)
    mesh1 = ax1.pcolormesh(
        X_grid,
        Z_grid,
        Vort0,
        shading="gouraud",
        cmap="coolwarm",
        vmin=vort_min,
        vmax=vort_max,
    )
    cbar1 = fig.colorbar(mesh1, ax=ax1, label="Vorticité")
    cbar1.ax.yaxis.label.set_color(text_color)
    cbar1.ax.tick_params(colors=text_color)

    quiv1 = ax1.quiver(
        Xq,
        Zq,
        Uq0,
        Vq0,
        color="#0f172a",
        scale=arrow_scale,
        scale_units="xy",
        width=0.003,
    )
    title1 = ax1.set_title(
        f"Vorticité et Vitesse (n = {indices[0]}/{n_final}{suffix_r})",
        color=text_color,
    )
    ax1.set_xlabel("x", color=text_color)
    ax1.set_ylabel("z", color=text_color)
    ax1.tick_params(colors=text_color)

    # --- Graphique 2 (en bas) : Température et Vitesse ---
    ax2.set_facecolor(bg_color)
    mesh2 = ax2.pcolormesh(
        X_grid,
        Z_grid,
        Theta0,
        shading="gouraud",
        cmap="inferno",
        vmin=theta_min,
        vmax=theta_max,
    )
    cbar2 = fig.colorbar(mesh2, ax=ax2, label="Écart de température theta")
    cbar2.ax.yaxis.label.set_color(text_color)
    cbar2.ax.tick_params(colors=text_color)

    quiv2 = ax2.quiver(
        Xq,
        Zq,
        Uq0,
        Vq0,
        color="#f8fafc",
        scale=arrow_scale,
        scale_units="xy",
        width=0.003,
    )
    title2 = ax2.set_title(
        f"Température et Vitesse (n = {indices[0]}/{n_final}{suffix_r})",
        color=text_color,
    )
    ax2.set_xlabel("x", color=text_color)
    ax2.set_ylabel("z", color=text_color)
    ax2.tick_params(colors=text_color)

    plt.tight_layout()

    def update(frame_idx):
        n = indices[frame_idx]
        Xn, Yn, Zn = traj[n][0], traj[n][1], traj[n][2]

        Vort_n = vort(X_grid, Z_grid, q, Xn)
        Theta_n = temp(X_grid, Z_grid, q, Yn, Zn)
        Uq_n = u(Xq, Zq, q, Xn)
        Vq_n = v(Xq, Zq, q, Xn)

        mesh1.set_array(Vort_n.ravel())
        quiv1.set_UVC(Uq_n, Vq_n)
        title1.set_text(f"Vorticité et Vitesse (n = {n}/{n_final}{suffix_r})")

        mesh2.set_array(Theta_n.ravel())
        quiv2.set_UVC(Uq_n, Vq_n)
        title2.set_text(f"Température et Vitesse (n = {n}/{n_final}{suffix_r})")

        return mesh1, quiv1, title1, mesh2, quiv2, title2

    ani = animation.FuncAnimation(
        fig, update, frames=len(indices), interval=interval, blit=False
    )

    if save_path:
        ani.save(save_path, writer="pillow", fps=25, facecolor=bg_color)

    plt.show()
    return ani


q = np.pi / 2
traj_28 = integration(X0, Y0, Z0, 28)
traj_10 = integration(X0, Y0, Z0, 10)
ani_28 = animer_lorenz_rapide(traj_28, q=q, r=28, max_frames=250, interval=40)
ani_10 = animer_lorenz_rapide(traj_10, q=q, r=10, max_frames=250, interval=40)






def papillons_r(valeurs_r):
    bg_color = "#171d26"
    text_color = "#f1f5f9"
    grid_color = "#334155"
    couleurs = ["#5ec3ee", "#f472b6", "#894CCA"]

    T = [integration(X0, Y0, Z0, r) for r in valeurs_r]

    fig = plt.figure(figsize=(15, 5), facecolor=bg_color)

    for i, r in enumerate(valeurs_r):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d", facecolor=bg_color)
        couleur_courbe = couleurs[i % len(couleurs)]

        # Fond des faces 3D et grilles adaptés au thème sombre
        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            axis.pane.set_facecolor(bg_color)
            axis.pane.set_edgecolor(grid_color)
            axis._axinfo["grid"]["color"] = grid_color
            axis._axinfo["tick"]["color"] = text_color

        traj = T[i]
        x_vals = [point[0] for point in traj]
        y_vals = [point[1] for point in traj]
        z_vals = [point[2] for point in traj]

        ax.plot(
            x_vals,
            y_vals,
            z_vals,
            label=f"r = {r}",
            color=couleur_courbe,
            linewidth=0.6,
        )

        ax.set_title(f"Système de Lorenz (r = {r})", color=text_color)
        ax.set_xlabel("X", color=text_color)
        ax.set_ylabel("Y", color=text_color)
        ax.set_zlabel("Z", color=text_color)
        ax.tick_params(colors=text_color)

        leg = ax.legend(facecolor="#1e293b", edgecolor=grid_color)
        for text in leg.get_texts():
            text.set_color(text_color)

    plt.tight_layout()
    plt.show()


valeurs_r = [1, 18, 28]

#papillons_r(valeurs_r)

r=28


def papillons_CI_comparaison(CI_initiale, r, temps_court_max=30.0):
    # Nombre de pas de temps pour la vue courte
    Nt_court = int(temps_court_max / h)
    temps_court = np.arange(Nt_court + 1) * h
    
    # 1. Calcul de la trajectoire de référence (sans perturbation)
    traj_ref = integration(CI_initiale[0], CI_initiale[1], CI_initiale[2], r)
    
    fig = plt.figure(figsize=(16, 10))
    noms = {0: 'X', 1: 'Y', 2: 'Z'}
    
    # Limite pour la référence sur le temps court
    limite_3d_ref = min(Nt_court + 1, len(traj_ref))
    x_ref_3d = [traj_ref[k][0] for k in range(limite_3d_ref)]
    y_ref_3d = [traj_ref[k][1] for k in range(limite_3d_ref)]
    z_ref_3d = [traj_ref[k][2] for k in range(limite_3d_ref)]
    
    for i in range(3):
        # Création d'une copie stricte et perturbation UNIQUE de la i-ème variable
        CI_pert = list(CI_initiale)
        CI_pert[i] += 1e-3  # Ajout de 10^-3 exactement sur la variable i
        
        # Calcul de la trajectoire perturbée
        traj_pert = integration(CI_pert[0], CI_pert[1], CI_pert[2], r)
        
        # --- LIGNE DU HAUT : 3D (Référence vs Perturbé sur le temps court) ---
        ax_3d = fig.add_subplot(2, 3, i + 1, projection='3d')
        
        limite_3d_pert = min(Nt_court + 1, len(traj_pert))
        x_p = [traj_pert[k][0] for k in range(limite_3d_pert)]
        y_p = [traj_pert[k][1] for k in range(limite_3d_pert)]
        z_p = [traj_pert[k][2] for k in range(limite_3d_pert)]
        
        # Tracé de la trajectoire de référence en 3D (ex: en gris/noir pointillé ou fin)
        ax_3d.plot(x_ref_3d, y_ref_3d, z_ref_3d, color='blue', linestyle='--', linewidth=0.4, label='réf')
        # Tracé de la trajectoire perturbée en 3D (en rouge ou bleu)
        ax_3d.plot(x_p, y_p, z_p, color='red', linewidth=0.5, alpha=0.8, label='perturbé')
        
        ax_3d.set_title(f'Espace des phases 3D\n(Perturbation sur {noms[i]})')
        ax_3d.set_xlabel('X')
        ax_3d.set_ylabel('Y')
        ax_3d.set_zlabel('Z')
        ax_3d.legend()
        
        # --- LIGNE DU BAS : Comparaison Référence vs Perturbé (Temps court) ---
        ax_2d = fig.add_subplot(2, 3, i + 4)
        
        # Extraction de la variable i sur le temps court
        var_ref = [traj_ref[k][i] for k in range(min(Nt_court + 1, len(traj_ref)))]
        var_pert = [traj_pert[k][i] for k in range(min(Nt_court + 1, len(traj_pert)))]
        t_reel = temps_court[:len(var_ref)]
        
        # Tracé avec des styles bien distincts pour les distinguer
        ax_2d.plot(t_reel, var_ref, color='blue', linestyle='--', linewidth=1.5, label=f'{noms[i]} (réf)')
        ax_2d.plot(t_reel, var_pert, color='red', linestyle='-', linewidth=1.0, alpha=0.8, label=f'{noms[i]} (perturbé)')
        
        ax_2d.set_title(f'Divergence de {noms[i]} (0 à {temps_court_max}s)')
        ax_2d.set_xlabel('Temps t')
        ax_2d.set_ylabel(noms[i])
        ax_2d.legend()

    plt.tight_layout()
    plt.show()


import matplotlib.pyplot as plt
import numpy as np


def papillons_CI_comparaison(CI_initiale, r, temps_court_max=30.0):
    bg_color = "#171d26"
    panel_color = "#1e2632"
    text_color = "#f1f5f9"
    grid_color = "#334155"

    # Couleurs contrastées pour distinguer référence et perturbation sur fond sombre
    ref_color = "#38bdf8"  # bleu ciel lumineux (pointillé)
    pert_colors = ["#fb7185", "#fbbf24", "#34d399"]  # rose corail, ambre, vert émeraude selon i

    # Nombre de pas de temps pour la vue courte
    Nt_court = int(temps_court_max / h)
    temps_court = np.arange(Nt_court + 1) * h

    # 1. Calcul de la trajectoire de référence (sans perturbation)
    traj_ref = integration(CI_initiale[0], CI_initiale[1], CI_initiale[2], r)

    fig = plt.figure(figsize=(16, 10), facecolor=bg_color)
    noms = {0: "X", 1: "Y", 2: "Z"}

    # Limite pour la référence sur le temps court
    limite_3d_ref = min(Nt_court + 1, len(traj_ref))
    x_ref_3d = [traj_ref[k][0] for k in range(limite_3d_ref)]
    y_ref_3d = [traj_ref[k][1] for k in range(limite_3d_ref)]
    z_ref_3d = [traj_ref[k][2] for k in range(limite_3d_ref)]

    for i in range(3):
        pert_color = pert_colors[i]

        # Création d'une copie stricte et perturbation UNIQUE de la i-ème variable
        CI_pert = list(CI_initiale)
        CI_pert[i] += 1e-3  # Ajout de 10^-3 exactement sur la variable i

        # Calcul de la trajectoire perturbée
        traj_pert = integration(CI_pert[0], CI_pert[1], CI_pert[2], r)

        # --- LIGNE DU HAUT : 3D (Référence vs Perturbé sur le temps court) ---
        ax_3d = fig.add_subplot(2, 3, i + 1, projection="3d")
        ax_3d.set_facecolor(bg_color)
        for axis in (ax_3d.xaxis, ax_3d.yaxis, ax_3d.zaxis):
            axis.pane.set_facecolor(panel_color)
            axis.pane.set_edgecolor(grid_color)
            axis.pane.set_alpha(0.35)
            axis._axinfo["grid"]["color"] = grid_color
            axis._axinfo["grid"]["linewidth"] = 0.6

        limite_3d_pert = min(Nt_court + 1, len(traj_pert))
        x_p = [traj_pert[k][0] for k in range(limite_3d_pert)]
        y_p = [traj_pert[k][1] for k in range(limite_3d_pert)]
        z_p = [traj_pert[k][2] for k in range(limite_3d_pert)]

        ax_3d.plot(
            x_ref_3d,
            y_ref_3d,
            z_ref_3d,
            color=ref_color,
            linestyle="--",
            linewidth=0.9,
            alpha=0.85,
            label="réf",
        )
        ax_3d.plot(
            x_p,
            y_p,
            z_p,
            color=pert_color,
            linestyle="-",
            linewidth=1.1,
            alpha=0.92,
            label=f"perturbé (+1e-3 sur {noms[i]})",
        )

        ax_3d.set_title(
            f"Espace des phases 3D\n(Perturbation sur {noms[i]}, r={r})",
            color=text_color,
        )
        ax_3d.set_xlabel("X", color=text_color)
        ax_3d.set_ylabel("Y", color=text_color)
        ax_3d.set_zlabel("Z", color=text_color)
        ax_3d.tick_params(colors=text_color)

        leg_3d = ax_3d.legend(facecolor=panel_color, edgecolor=grid_color)
        for text in leg_3d.get_texts():
            text.set_color(text_color)

        # --- LIGNE DU BAS : Comparaison Référence vs Perturbé (Temps court) ---
        ax_2d = fig.add_subplot(2, 3, i + 4)
        ax_2d.set_facecolor(panel_color)
        ax_2d.grid(True, color=grid_color, linestyle=":", linewidth=0.6, alpha=0.7)
        for spine in ax_2d.spines.values():
            spine.set_color(grid_color)

        var_ref = [
            traj_ref[k][i] for k in range(min(Nt_court + 1, len(traj_ref)))
        ]
        var_pert = [
            traj_pert[k][i] for k in range(min(Nt_court + 1, len(traj_pert)))
        ]
        t_reel = temps_court[: len(var_ref)]

        ax_2d.plot(
            t_reel,
            var_ref,
            color=ref_color,
            linestyle="--",
            linewidth=1.6,
            label=f"{noms[i]} (réf)",
        )
        ax_2d.plot(
            t_reel,
            var_pert,
            color=pert_color,
            linestyle="-",
            linewidth=1.3,
            alpha=0.95,
            label=f"{noms[i]} (perturbé)",
        )

        ax_2d.set_title(
            f"Divergence de {noms[i]} (0 à {temps_court_max}s)",
            color=text_color,
        )
        ax_2d.set_xlabel("Temps t", color=text_color)
        ax_2d.set_ylabel(noms[i], color=text_color)
        ax_2d.tick_params(colors=text_color)

        leg_2d = ax_2d.legend(facecolor=bg_color, edgecolor=grid_color)
        for text in leg_2d.get_texts():
            text.set_color(text_color)

    plt.tight_layout()
    plt.show()




#papillons_CI_comparaison([X0,Y0,Z0],r)


#REMARQUE ANALYSE: on remarque que perturbé ou non, c'est les memes trajectoires
#genre l'idée c'est que en régime chaotioque, dans tous les cas il vont explorer
#toutes les possibilités, donc la perturbation n'a pas tant d'impact
#en d'ailleurs si on teste avec r=18, ie pas de chaos, ça bifurque pas
#prcq 10e3 ça se voit pas quoi



















import matplotlib.pyplot as plt
import numpy as np
from constante import *
from integration import *

def comparer_r10_r28_instants(indices=[50, 200, 500]):
    q = np.pi / np.sqrt(2)
    X0, Y0, Z0 = 1.0, 1.0, 1.0
    
    # 1. Calcul des trajectoires pour r = 10 et r = 28
    print("Calcul des trajectoires...")
    traj_r10 = integration(X0, Y0, Z0, r=10)
    traj_r28 = integration(X0, Y0, Z0, r=28)
    
    # 2. Définition de la grille spatiale (x et z)
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 30)
    z_vals = np.linspace(0, 1, 30)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)
    
    # 3. Création de la figure 2x3
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    
    # --- LIGNE DU HAUT : r = 10 à 3 instants différents ---
    for j, n in enumerate(indices):
        X_n = traj_r10[n][0]
        
        # Calcul des champs
        Vort_grid = vort(X_grid, Z_grid, q, X_n)
        U = u(X_grid, Z_grid, q, X_n)
        V = v(X_grid, Z_grid, q, X_n)
        
        ax = axes[0, j]
        im = ax.pcolormesh(X_grid, Z_grid, Vort_grid, shading='auto', cmap='coolwarm')
        ax.quiver(X_grid, Z_grid, U, V, color='black', scale=400)
        ax.set_title(f"r = 10 (instant t_n, n={n})")
        ax.set_xlabel('x')
        ax.set_ylabel('z')

    # --- LIGNE DU BAS : r = 28 à 3 instants différents ---
    for j, n in enumerate(indices):
        X_n = traj_r28[n][0]
        
        # Calcul des champs
        Vort_grid = vort(X_grid, Z_grid, q, X_n)
        U = u(X_grid, Z_grid, q, X_n)
        V = v(X_grid, Z_grid, q, X_n)
        
        ax = axes[1, j]
        im = ax.pcolormesh(X_grid, Z_grid, Vort_grid, shading='auto', cmap='coolwarm')
        ax.quiver(X_grid, Z_grid, U, V, color='black', scale=400)
        ax.set_title(f"r = 28 (chaos, n={n})")
        ax.set_xlabel('x')
        ax.set_ylabel('z')

    plt.tight_layout()
    plt.show()

#comparer_r10_r28_instants(indices=[50, 300, 900])


import matplotlib.pyplot as plt
import numpy as np

def papillons_r_non_constant():
    # 1. Utiliser un thème sombre pour faire ressortir les couleurs
    plt.style.use('dark_background')
    
    fig = plt.figure(figsize=(10, 10))
    # 2. Utiliser 1, 1, 1 pour centrer l'unique graphique
    ax = fig.add_subplot(1, 1, 1, projection='3d')
        
    # Récupération de la trajectoire
    traj = integration_r_increasing(X0, Y0, Z0)

    # Conversion en tableau NumPy pour une manipulation plus performante
    traj_np = np.array(traj)
    x_vals = traj_np[:, 0]
    y_vals = traj_np[:, 1]
    z_vals = traj_np[:, 2]

    # 3. Créer un dégradé de couleur basé sur le temps (l'index)
    temps = np.linspace(0, 1, len(x_vals))

    # Tracé avec scatter pour bénéficier du dégradé (cmap)
    # s=0.5 gère la taille des points, alpha la transparence
    scatter = ax.scatter(x_vals, y_vals, z_vals, #type:ignore
                         c=temps, cmap='magma', 
                         s=0.5, alpha=0.8, edgecolor='none') #type:ignore

    # 4. Esthétique : suppression des axes et de la grille pour un effet "flottant"
    ax.set_axis_off()
    
    ax.set_title('Système de Lorenz (r augmentant)', color='white', fontsize=14, pad=20)
    
    # Ajout d'une barre de couleur pour indiquer l'écoulement du temps
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, pad=0.05)
    cbar.set_label('Évolution du temps', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.tight_layout()
    plt.show()

#papillons_r_non_constant()


import matplotlib.pyplot as plt
import numpy as np


def papillons_r_non_constant(X0, Y0, Z0, max_points=15000):
    bg_color = "#171d26"
    text_color = "#f1f5f9"

    fig = plt.figure(figsize=(10.5, 10), facecolor=bg_color)
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.set_facecolor(bg_color)

    # Récupération et conversion de la trajectoire
    traj = integration_r_increasing(X0, Y0, Z0)
    traj_np = np.asarray(traj, dtype=float)

    # Sous-échantillonnage léger si la trajectoire est très longue pour garder des points nets et rapides
    if len(traj_np) > max_points:
        idx = np.linspace(0, len(traj_np) - 1, max_points, dtype=int)
        traj_np = traj_np[idx]
    else:
        idx = np.arange(len(traj_np))

    x_vals = traj_np[:, 0]
    y_vals = traj_np[:, 1]
    z_vals = traj_np[:, 2]

    # Progression normalisée de 0 (début) à 1 (fin)
    progression = np.linspace(0.0, 1.0, len(x_vals))

    # Fin filigrane très discret pour relier les points et montrer le sens de la trajectoire
    ax.plot(
        x_vals,
        y_vals,
        z_vals,
        color="#94a3b8",
        linewidth=0.45,
        alpha=0.22,
    )

    # Points plus visibles avec taille progressive (début -> fin) et colormap 'plasma'
    sizes = np.linspace(2.5, 8.5, len(x_vals))
    scatter = ax.scatter(
        x_vals,
        y_vals,
        z_vals,
        c=progression,
        cmap="plasma",
        s=sizes,
        alpha=0.88,
        edgecolors="none",
        depthshade=True,
    )

    # Repères discrets pour l'instant initial et l'instant final
    ax.scatter(
        [x_vals[0]],
        [y_vals[0]],
        [z_vals[0]],
        color="#38bdf8",
        s=55,
        edgecolors="#f8fafc",
        linewidths=0.8,
        label="Début (t = 0)",
    )
    ax.scatter(
        [x_vals[-1]],
        [y_vals[-1]],
        [z_vals[-1]],
        color="#fb7185",
        s=65,
        edgecolors="#f8fafc",
        linewidths=0.8,
        label="Fin",
    )

    ax.set_axis_off()
    ax.set_title(
        "Système de Lorenz avec r croissant (évolution temporelle)",
        color=text_color,
        fontsize=14,
        pad=18,
    )

    leg = ax.legend(
        loc="upper left",
        facecolor="#1e2632",
        edgecolor="#334155",
        fontsize=10,
    )
    for txt in leg.get_texts():
        txt.set_color(text_color)

    cbar = fig.colorbar(scatter, ax=ax, shrink=0.55, pad=0.04)
    cbar.set_label("Progression temporelle (0 → 1)", color=text_color, fontsize=11)
    cbar.ax.yaxis.set_tick_params(color=text_color, labelcolor=text_color)
    cbar.outline.set_edgecolor("#334155")

    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np



import matplotlib.pyplot as plt
import numpy as np


def papillons_r_non_constant(X0, Y0, Z0, step=2, point_size=1.2):
    bg_color = "#171d26"
    text_color = "#f1f5f9"

    fig = plt.figure(figsize=(10.5, 10), facecolor=bg_color)
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.set_facecolor(bg_color)

    # Récupération de la trajectoire à haute précision
    traj = integration_r_increasing(X0, Y0, Z0)
    traj_np = np.asarray(traj, dtype=float)[::step]

    x_vals = traj_np[:, 0]
    y_vals = traj_np[:, 1]
    z_vals = traj_np[:, 2]

    # Progression normalisée de 0 (début) à 1 (fin)
    progression = np.linspace(0.0, 1.0, len(x_vals))

    # Nuage de points fins avec dégradé temporel 'plasma'
    scatter = ax.scatter(
        x_vals,
        y_vals,
        z_vals,
        c=progression,
        cmap="plasma",
        s=point_size,
        alpha=0.85,
        edgecolors="none",
        depthshade=True,
    )

    # Repères discrets pour l'instant initial et l'instant final
    ax.scatter(
        [x_vals[0]],
        [y_vals[0]],
        [z_vals[0]],
        color="#38bdf8",
        s=45,
        edgecolors="#f8fafc",
        linewidths=0.8,
        label="Début",
    )
    ax.scatter(
        [x_vals[-1]],
        [y_vals[-1]],
        [z_vals[-1]],
        color="#fb7185",
        s=55,
        edgecolors="#f8fafc",
        linewidths=0.8,
        label="Fin",
    )

    ax.set_axis_off()
    ax.set_title(
        "Système de Lorenz avec r croissant (évolution temporelle)",
        color=text_color,
        fontsize=14,
        pad=18,
    )

    leg = ax.legend(
        loc="upper left",
        facecolor="#1e2632",
        edgecolor="#334155",
        fontsize=10,
    )
    for txt in leg.get_texts():
        txt.set_color(text_color)

    cbar = fig.colorbar(scatter, ax=ax, shrink=0.55, pad=0.04)
    cbar.set_label("Progression temporelle (0 → 1)", color=text_color, fontsize=11)
    cbar.ax.yaxis.set_tick_params(color=text_color, labelcolor=text_color)
    cbar.outline.set_edgecolor("#334155")

    plt.tight_layout()
    plt.show()


papillons_r_non_constant(X0, Y0, Z0)





