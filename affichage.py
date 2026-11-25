import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

try:
    from constante import *
except ImportError:
    r = 28  # valeur par defaut si constante.py est introuvable

try:
    from integration import *
except ImportError:
    # integration.py introuvable -> petit RK4 de secours (sigma=10, b=8/3, dt=0.01)
    def _lorenz(p, r, sigma=10.0, b=8.0 / 3.0):
        x, y, z = p
        return np.array([sigma * (y - x), r * x - y - x * z, x * y - b * z])

    def _rk4(p, r, dt):
        k1 = _lorenz(p, r)
        k2 = _lorenz(p + dt / 2 * k1, r)
        k3 = _lorenz(p + dt / 2 * k2, r)
        k4 = _lorenz(p + dt * k3, r)
        return p + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    def integration(X0, Y0, Z0, r, dt=0.01, N=5000):
        traj = [np.array([X0, Y0, Z0], dtype=float)]
        for _ in range(N):
            traj.append(_rk4(traj[-1], r, dt))
        return traj

    def integration_r_increasing(X0, Y0, Z0, r_min=0.0, r_max=35.0, dt=0.01, N=5000):
        traj = [np.array([X0, Y0, Z0], dtype=float)]
        for i in range(N):
            r_i = r_min + (r_max - r_min) * i / N
            traj.append(_rk4(traj[-1], r_i, dt))
        return traj

# X(t) = X0 constant pour la 1ere partie
# fonctions u, v, vort et temp (je les redefinis plus bas pour X(t))

def u(x, z, q, X0):
    return X0 * np.pi * np.sin(np.pi * z) * np.sin(q * x)

def v(x, z, q, X_t):
    return X_t * q * np.cos(np.pi * z) * np.cos(q * x)

def vort(x, z, q, X_t):
    return np.pi**2 * X_t * np.cos(np.pi * z) * np.sin(q * x) + q**2 * X_t * np.cos(np.pi * z) * np.sin(q * x)

def temp(x, z, q, Y_t, Z_t):
    return Y_t * np.cos(np.pi * z) * np.cos(q * x) + Z_t * np.sin(2 * np.pi * z)


# ================= affichages =================

def afficher_vorti_temp_cst(X, Z, U, V, q, X0, Y0, Z0):
    bg_color = "#171d26"
    text_color = "#f1f5f9"

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=bg_color)

    # graphe du haut : vorticité + vitesse
    ax1.set_facecolor(bg_color)
    mesh1 = ax1.pcolormesh(X, Z, vort(X, Z, q, X0), shading="gouraud", cmap="coolwarm")
    cbar1 = fig.colorbar(mesh1, ax=ax1, label="Vorticité")
    cbar1.ax.yaxis.label.set_color(text_color)
    cbar1.ax.tick_params(colors=text_color)

    # on garde 1 fleche sur 6 sinon trop dense
    pas = 6
    ax1.quiver(X[::pas, ::pas], Z[::pas, ::pas], U[::pas, ::pas], V[::pas, ::pas], color="#0f172a", width=0.003)
    ax1.set_title(f"Vorticité et champ de vitesse (X0 = {X0})", color=text_color)
    ax1.set_xlabel("x", color=text_color)
    ax1.set_ylabel("z", color=text_color)
    ax1.tick_params(colors=text_color)

    # graphe du bas : température + vitesse
    ax2.set_facecolor(bg_color)
    mesh2 = ax2.pcolormesh(X, Z, temp(X, Z, q, Y0, Z0), shading="gouraud", cmap="inferno")
    cbar2 = fig.colorbar(mesh2, ax=ax2, label="Écart de température theta")
    cbar2.ax.yaxis.label.set_color(text_color)
    cbar2.ax.tick_params(colors=text_color)

    ax2.quiver(X[::pas, ::pas], Z[::pas, ::pas], U[::pas, ::pas], V[::pas, ::pas], color="#f8fafc", width=0.003)
    ax2.set_title(f"Température et champ de vitesse (Y0 = {Y0}, Z0 = {Z0})", color=text_color)
    ax2.set_xlabel("x", color=text_color)
    ax2.set_ylabel("z", color=text_color)
    ax2.tick_params(colors=text_color)

    plt.tight_layout()
    plt.show()


# paramètres et grille
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


# --- les memes fonctions mais avec la valeur à l'instant t ---
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

    # on recup X, Y, Z a l'instant n
    X_n = traj[n][0]
    Y_n = traj[n][1]
    Z_n = traj[n][2]

    # x dans [-2pi/q, 2pi/q] et z dans [0,1] (cf sujet)
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 40)
    z_vals = np.linspace(0, 1, 40)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)

    # les champs
    U = u(X_grid, Z_grid, q, X_n)
    V = v(X_grid, Z_grid, q, X_n)
    Vort_grid = vort(X_grid, Z_grid, q, X_n)
    Theta_grid = temp(X_grid, Z_grid, q, Y_n, Z_n)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=bg_color)

    # haut : vorticité
    ax1.set_facecolor(bg_color)
    mesh1 = ax1.pcolormesh(X_grid, Z_grid, Vort_grid, shading="auto", cmap="coolwarm")
    cbar1 = fig.colorbar(mesh1, ax=ax1, label="Vorticité")
    cbar1.ax.yaxis.label.set_color(text_color)
    cbar1.ax.tick_params(colors=text_color)

    ax1.quiver(X_grid, Z_grid, U, V, color="black")
    ax1.set_title(f"Vorticité et Vitesse (instant n={n}, r={r})", color=text_color)
    ax1.set_xlabel("x", color=text_color)
    ax1.set_ylabel("z", color=text_color)
    ax1.tick_params(colors=text_color)

    # bas : température
    ax2.set_facecolor(bg_color)
    mesh2 = ax2.pcolormesh(X_grid, Z_grid, Theta_grid, shading="auto", cmap="inferno")
    cbar2 = fig.colorbar(mesh2, ax=ax2, label="Écart de température theta")
    cbar2.ax.yaxis.label.set_color(text_color)
    cbar2.ax.tick_params(colors=text_color)

    ax2.quiver(X_grid, Z_grid, U, V, color="white")
    ax2.set_title(f"Température et Vitesse (instant n={n}, r={r})", color=text_color)
    ax2.set_xlabel("x", color=text_color)
    ax2.set_ylabel("z", color=text_color)
    ax2.tick_params(colors=text_color)

    plt.tight_layout()
    plt.show()

# trajectoire avec la fonction integration
traj = integration(X0, Y0, Z0, r)

# instant n et q (faut 0 <= n < len(traj))
n = 50
q = np.pi / 2

#afficher_physique_instant(traj, n, q)


# conditions initiales
X0, Y0, Z0 = 1.0, 1.0, 1.0

# r = 10 -> stable
print("Calcul pour r = 10...")
traj_r10 = integration(X0, Y0, Z0, r=10)
#afficher_physique_instant(traj_r10, -1, q)

# r = 28 -> chaos, ça bouge tout le temps donc tester plusieurs n (100, 500, -1)
print("Calcul pour r = 28...")
traj_r28 = integration(X0, Y0, Z0, r=28)
#afficher_physique_instant(traj_r28, -1, q)


def afficher_vorticite_instants(traj, instants, q, r=None, pas_q=6):
    bg_color = "#171d26"
    text_color = "#f1f5f9"
    suffix_r = f", r={r}" if r is not None else ""

    # grille fine pour que ce soit lisse
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 120)
    z_vals = np.linspace(0, 1, 120)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)

    # grille moins dense pour les flèches sinon illisible
    Xq, Zq = X_grid[::pas_q, ::pas_q], Z_grid[::pas_q, ::pas_q]

    champs = []
    for n in instants:
        X_n = traj[n][0]
        Vort_n = vort(X_grid, Z_grid, q, X_n)
        Uq_n = u(Xq, Zq, q, X_n)
        Vq_n = v(Xq, Zq, q, X_n)
        champs.append((n, Vort_n, Uq_n, Vq_n))

    # meme echelle pour tous les instants pour comparer
    vmin = min(np.min(item[1]) for item in champs)
    vmax = max(np.max(item[1]) for item in champs)
    max_speed = max(max(np.max(np.hypot(item[2], item[3])), 1e-6) for item in champs)
    arrow_scale = max_speed * 7.5

    fig, axes = plt.subplots(1, len(instants), figsize=(18, 4.8), facecolor=bg_color)
    if len(instants) == 1:
        axes = [axes]

    for ax, (n, Vort_n, Uq_n, Vq_n) in zip(axes, champs):
        ax.set_facecolor(bg_color)
        mesh = ax.pcolormesh(X_grid, Z_grid, Vort_n, shading="gouraud", cmap="coolwarm", vmin=vmin, vmax=vmax)
        cbar = fig.colorbar(mesh, ax=ax, label="Vorticité")
        cbar.ax.yaxis.label.set_color(text_color)
        cbar.ax.tick_params(colors=text_color)

        ax.quiver(Xq, Zq, Uq_n, Vq_n, color="#0f172a", scale=arrow_scale, scale_units="xy", width=0.003)

        ax.set_title(f"Vorticité — instant n={n}{suffix_r}", color=text_color)
        ax.set_xlabel("x", color=text_color)
        ax.set_ylabel("z", color=text_color)
        ax.tick_params(colors=text_color)

    plt.tight_layout()
    plt.show()


def animer_lorenz_rapide(traj, q, r=28, max_frames=20, pas_q=6, interval=40, save_path=None):
    bg_color = "#171d26"
    text_color = "#f1f5f9"
    suffix_r = f", r={r}" if r is not None else ""

    n_final = len(traj) - 1
    nb_frames = min(max_frames, len(traj))
    indices = np.unique(np.linspace(0, n_final, nb_frames, dtype=int))

    # grille fine (fond) + grille espacée (flèches)
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 120)
    z_vals = np.linspace(0, 1, 120)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)
    Xq, Zq = X_grid[::pas_q, ::pas_q], Z_grid[::pas_q, ::pas_q]

    # on estime les bornes sur quelques frames seulement (sinon trop long)
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

    # état de départ
    X0_n, Y0_n, Z0_n = traj[indices[0]]
    Vort0 = vort(X_grid, Z_grid, q, X0_n)
    Theta0 = temp(X_grid, Z_grid, q, Y0_n, Z0_n)
    Uq0 = u(Xq, Zq, q, X0_n)
    Vq0 = v(Xq, Zq, q, X0_n)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=bg_color)

    # en haut : vorticité
    ax1.set_facecolor(bg_color)
    mesh1 = ax1.pcolormesh(X_grid, Z_grid, Vort0, shading="gouraud", cmap="coolwarm", vmin=vort_min, vmax=vort_max)
    cbar1 = fig.colorbar(mesh1, ax=ax1, label="Vorticité")
    cbar1.ax.yaxis.label.set_color(text_color)
    cbar1.ax.tick_params(colors=text_color)

    quiv1 = ax1.quiver(Xq, Zq, Uq0, Vq0, color="#0f172a", scale=arrow_scale, scale_units="xy", width=0.003)
    title1 = ax1.set_title(f"Vorticité et Vitesse (n = {indices[0]}/{n_final}{suffix_r})", color=text_color)
    ax1.set_xlabel("x", color=text_color)
    ax1.set_ylabel("z", color=text_color)
    ax1.tick_params(colors=text_color)

    # en bas : température
    ax2.set_facecolor(bg_color)
    mesh2 = ax2.pcolormesh(X_grid, Z_grid, Theta0, shading="gouraud", cmap="inferno", vmin=theta_min, vmax=theta_max)
    cbar2 = fig.colorbar(mesh2, ax=ax2, label="Écart de température theta")
    cbar2.ax.yaxis.label.set_color(text_color)
    cbar2.ax.tick_params(colors=text_color)

    quiv2 = ax2.quiver(Xq, Zq, Uq0, Vq0, color="#f8fafc", scale=arrow_scale, scale_units="xy", width=0.003)
    title2 = ax2.set_title(f"Température et Vitesse (n = {indices[0]}/{n_final}{suffix_r})", color=text_color)
    ax2.set_xlabel("x", color=text_color)
    ax2.set_ylabel("z", color=text_color)
    ax2.tick_params(colors=text_color)

    plt.tight_layout()

    # mise à jour à chaque frame
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

    ani = animation.FuncAnimation(fig, update, len(indices), interval=interval, blit=False)

    if save_path: ani.save(save_path, writer="pillow", fps=25, dpi=120, savefig_kwargs={"facecolor": bg_color})

    plt.show()
    return ani


q = np.pi / 2
traj_28 = integration(X0, Y0, Z0, 28)
traj_10 = integration(X0, Y0, Z0, 10)
#ani_28 = animer_lorenz_rapide(traj_28, q=q, r=28, max_frames=250, interval=40)
#ani_10 = animer_lorenz_rapide(traj_10, q=q, r=10, max_frames=250, interval=40)


def papillons_r(valeurs_r):
    bg_color = "#171d26"
    text_color = "#f1f5f9"
    grid_color = "#334155"
    couleurs = ["#5ec3ee", "#f472b6", "#894CCA"]

    T = [integration(X0, Y0, Z0, r) for r in valeurs_r]

    fig = plt.figure(figsize=(15, 5), facecolor=bg_color)

    for i, r in enumerate(valeurs_r):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d", facecolor=bg_color)
        couleur_courbe = couleurs[i]

        # theme sombre pour les faces 3D
        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            axis.pane.set_facecolor(bg_color)
            axis.pane.set_edgecolor(grid_color)
            axis._axinfo["grid"]["color"] = grid_color
            axis._axinfo["tick"]["color"] = text_color

        traj = T[i]
        x_vals = [point[0] for point in traj]
        y_vals = [point[1] for point in traj]
        z_vals = [point[2] for point in traj]

        ax.plot(x_vals, y_vals, z_vals, label=f"r = {r}", color=couleur_courbe, linewidth=0.6)

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


def papillons_r_non_constant(X0, Y0, Z0, step=2, point_size=1.2):
    bg_color = "#171d26"
    text_color = "#f1f5f9"

    fig = plt.figure(figsize=(10.5, 10), facecolor=bg_color)
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.set_facecolor(bg_color)

    # trajectoire avec r qui augmente
    traj = integration_r_increasing(X0, Y0, Z0)
    traj_np = np.asarray(traj, dtype=float)[::step]

    x_vals = traj_np[:, 0]
    y_vals = traj_np[:, 1]
    z_vals = traj_np[:, 2]

    # 0 = debut, 1 = fin
    progression = np.linspace(0.0, 1.0, len(x_vals))

    scatter = ax.scatter(x_vals, y_vals, z_vals,  # type:ignore
                         c=progression, cmap="plasma", s=point_size,  # type:ignore
                         alpha=0.85, edgecolors="none", depthshade=True)

    # point de départ et d'arrivée
    ax.scatter([x_vals[0]], [y_vals[0]], [z_vals[0]],  # type:ignore
               color="#38bdf8", s=45, edgecolors="#f8fafc", linewidths=0.8, label="Début")
    ax.scatter([x_vals[-1]], [y_vals[-1]], [z_vals[-1]],  # type:ignore
               color="#fb7185", s=55, edgecolors="#f8fafc", linewidths=0.8, label="Fin")

    ax.set_axis_off()
    ax.set_title("Système de Lorenz avec r croissant (évolution temporelle)", color=text_color, fontsize=14, pad=18)

    leg = ax.legend(loc="upper left", facecolor="#1e2632", edgecolor="#334155", fontsize=10)
    for txt in leg.get_texts():
        txt.set_color(text_color)

    cbar = fig.colorbar(scatter, ax=ax, shrink=0.55, pad=0.04)
    cbar.set_label("Progression temporelle (0 → 1)", color=text_color, fontsize=11)
    cbar.ax.yaxis.set_tick_params(color=text_color, labelcolor=text_color)
    cbar.outline.set_edgecolor("#334155")

    plt.tight_layout()
    plt.show()


#papillons_r_non_constant(X0, Y0, Z0)


# (1ere version de la comparaison, la 2eme juste en dessous la remplace)
def papillons_r_comparaison(X0, Y0, Z0, r_min=None, r_max=None, step=2, point_size=1.2):
    bg_color = "#171d26"
    panel_color = "#1e2632"
    text_color = "#f1f5f9"
    grid_color = "#334155"

    fig = plt.figure(figsize=(18, 9.5), facecolor=bg_color)

    # gauche : r croissant
    traj_inc = np.asarray(integration_r_increasing(X0, Y0, Z0), dtype=float)[::step]
    x_inc, y_inc, z_inc = traj_inc[:, 0], traj_inc[:, 1], traj_inc[:, 2]
    n_inc = len(x_inc)

    # si on donne r_min et r_max on affiche r, sinon juste 0 -> 1
    if r_min is not None and r_max is not None:
        r_vals = np.linspace(r_min, r_max, n_inc)
        color_metric = r_vals
        cbar_label = "Paramètre r (croissant)"
        r_info_text = f"r : {r_min:g} → {r_max:g} (croissant)"
    else:
        color_metric = np.linspace(0.0, 1.0, n_inc)
        cbar_label = "Progression temporelle / r (0 → 1)"
        r_info_text = "r croissant au cours du temps"

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.set_facecolor(bg_color)

    scatter1 = ax1.scatter(x_inc, y_inc, z_inc, c=color_metric, cmap="plasma", s=point_size,
                           alpha=0.88, edgecolors="none", depthshade=True)

    ax1.scatter([x_inc[0]], [y_inc[0]], [z_inc[0]], color="#38bdf8", s=45,
                edgecolors="#f8fafc", linewidths=0.8, label="Début")
    ax1.scatter([x_inc[-1]], [y_inc[-1]], [z_inc[-1]], color="#fb7185", s=55,
                edgecolors="#f8fafc", linewidths=0.8, label="Fin")

    ax1.set_axis_off()
    ax1.set_title(f"Lorenz — r variable\n({r_info_text})", color=text_color, fontsize=13, pad=14)

    # petit encadré avec les infos sur r
    ax1.text2D(0.02, 0.12, f"Infos paramètre r :\n• {r_info_text}\n• Points affichés : {n_inc}",
               transform=ax1.transAxes, color=text_color, fontsize=9.5,
               bbox=dict(boxstyle="round,pad=0.45", facecolor=panel_color, edgecolor=grid_color, alpha=0.92))

    leg1 = ax1.legend(loc="upper left", facecolor=panel_color, edgecolor=grid_color, fontsize=9.5)
    for txt in leg1.get_texts():
        txt.set_color(text_color)

    cbar1 = fig.colorbar(scatter1, ax=ax1, shrink=0.52, pad=0.03)
    cbar1.set_label(cbar_label, color=text_color, fontsize=10.5)
    cbar1.ax.yaxis.set_tick_params(color=text_color, labelcolor=text_color)
    cbar1.outline.set_edgecolor(grid_color)

    # droite : r = 28 fixe
    traj_28 = np.asarray(integration(X0, Y0, Z0, 28), dtype=float)[::step]
    x_28, y_28, z_28 = traj_28[:, 0], traj_28[:, 1], traj_28[:, 2]
    prog_28 = np.linspace(0.0, 1.0, len(x_28))

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.set_facecolor(bg_color)

    scatter2 = ax2.scatter(x_28, y_28, z_28, c=prog_28, cmap="viridis", s=point_size,
                           alpha=0.88, edgecolors="none", depthshade=True)

    ax2.scatter([x_28[0]], [y_28[0]], [z_28[0]], color="#38bdf8", s=45,
                edgecolors="#f8fafc", linewidths=0.8, label="Début")
    ax2.scatter([x_28[-1]], [y_28[-1]], [z_28[-1]], color="#fb7185", s=55,
                edgecolors="#f8fafc", linewidths=0.8, label="Fin")

    ax2.set_axis_off()
    ax2.set_title("Lorenz — r = 28 fixé\n(Régime chaotique stationnaire)", color=text_color, fontsize=13, pad=14)

    leg2 = ax2.legend(loc="upper left", facecolor=panel_color, edgecolor=grid_color, fontsize=9.5)
    for txt in leg2.get_texts():
        txt.set_color(text_color)

    cbar2 = fig.colorbar(scatter2, ax=ax2, shrink=0.52, pad=0.03)
    cbar2.set_label("Progression temporelle (0 → 1)", color=text_color, fontsize=10.5)
    cbar2.ax.yaxis.set_tick_params(color=text_color, labelcolor=text_color)
    cbar2.outline.set_edgecolor(grid_color)

    plt.tight_layout()
    plt.show()


# exemple (mettre r_min et r_max si on veut les vraies valeurs de r)
#papillons_r_comparaison(X0, Y0, Z0, r_min=0, r_max=35, step=2, point_size=1.2)


# 2eme version : pareil mais la couleur de droite = celle de r=28 sur la colorbar de gauche
def papillons_r_comparaison(X0, Y0, Z0, r_min=None, r_max=None, step=2, point_size=1.2, point_size_28=2.2):
    bg_color = "#171d26"
    panel_color = "#1e2632"
    text_color = "#f1f5f9"
    grid_color = "#334155"

    cmap = plt.get_cmap("plasma")

    fig = plt.figure(figsize=(18, 9.5), facecolor=bg_color)

    # gauche : r croissant
    traj_inc = np.asarray(integration_r_increasing(X0, Y0, Z0), dtype=float)[::step]
    x_inc, y_inc, z_inc = traj_inc[:, 0], traj_inc[:, 1], traj_inc[:, 2]
    n_inc = len(x_inc)

    if r_min is not None and r_max is not None:
        r_vals = np.linspace(r_min, r_max, n_inc)
        color_metric = r_vals
        cbar_label = "Paramètre r (croissant)"
        r_info_text = f"r : {r_min:g} → {r_max:g} (croissant)"
        # position de r=28 dans la colormap
        if r_max != r_min:
            r28_norm = np.clip((28.0 - r_min) / (r_max - r_min), 0.0, 1.0)
        else:
            r28_norm = 0.5
    else:
        color_metric = np.linspace(0.0, 1.0, n_inc)
        cbar_label = "Progression temporelle / r (0 → 1)"
        r_info_text = "r croissant au cours du temps"
        r28_norm = 0.75  # valeur au pif

    couleur_r28 = cmap(r28_norm)

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.set_facecolor(bg_color)

    scatter1 = ax1.scatter(x_inc, y_inc, z_inc,  # type:ignore
                           c=color_metric, cmap=cmap, s=point_size,  # type:ignore
                           alpha=0.88, edgecolors="none", depthshade=True)

    ax1.scatter([x_inc[0]], [y_inc[0]], [z_inc[0]],  # type:ignore
                color="#38bdf8", s=55, edgecolors="#f8fafc", linewidths=0.9, label="État initial")
    ax1.scatter([x_inc[-1]], [y_inc[-1]], [z_inc[-1]],  # type:ignore
                color="#fb7185", s=65, edgecolors="#f8fafc", linewidths=0.9, label="État final")

    ax1.set_axis_off()
    ax1.set_title(f"Lorenz — r variable\n({r_info_text})", color=text_color, fontsize=13, pad=14)

    ax1.text2D(0.02, 0.12, f"Infos paramètre r :\n• {r_info_text}\n• Points affichés : {n_inc}",
               transform=ax1.transAxes, color=text_color, fontsize=9.5,
               bbox=dict(boxstyle="round,pad=0.45", facecolor=panel_color, edgecolor=grid_color, alpha=0.92))

    leg1 = ax1.legend(loc="upper left", facecolor=panel_color, edgecolor=grid_color, fontsize=9.5)
    for txt in leg1.get_texts():
        txt.set_color(text_color)

    cbar1 = fig.colorbar(scatter1, ax=ax1, shrink=0.52, pad=0.03)
    cbar1.set_label(cbar_label, color=text_color, fontsize=10.5)
    cbar1.ax.yaxis.set_tick_params(color=text_color, labelcolor=text_color)
    cbar1.outline.set_edgecolor(grid_color)

    # droite : r = 28 fixe
    traj_28 = np.asarray(integration(X0, Y0, Z0, 28), dtype=float)[::step]
    x_28, y_28, z_28 = traj_28[:, 0], traj_28[:, 1], traj_28[:, 2]

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.set_facecolor(bg_color)

    ax2.scatter(x_28, y_28, z_28, color=couleur_r28, s=point_size_28,
                alpha=0.85, edgecolors="none", depthshade=True)

    # on met juste le début et la fin en évidence
    ax2.scatter([x_28[0]], [y_28[0]], [z_28[0]], color="#38bdf8", s=55,
                edgecolors="#f8fafc", linewidths=0.9, label="État initial")
    ax2.scatter([x_28[-1]], [y_28[-1]], [z_28[-1]], color="#fb7185", s=65,
                edgecolors="#f8fafc", linewidths=0.9, label="État final")

    ax2.set_axis_off()
    ax2.set_title("Lorenz — r = 28 fixé\n(Couleur associée à r = 28)", color=text_color, fontsize=13, pad=14)

    leg2 = ax2.legend(loc="upper left", facecolor=panel_color, edgecolor=grid_color, fontsize=9.5)
    for txt in leg2.get_texts():
        txt.set_color(text_color)

    plt.tight_layout()
    plt.show()


# ================= paramètres + exécution =================

# X(t) = X0 cst pour le 1er affichage
X0, Y0, Z0 = 1.0, 1.0, 1.0
q = np.pi / 2  # nombre d'onde (sujet)

grid_length = 120
grid_height = 120

x_ = np.linspace(-2 * np.pi / q, 2 * np.pi / q, grid_length)
z_ = np.linspace(0, 1, grid_height)
X, Z = np.meshgrid(x_, z_)
U = u(X, Z, q, X0)
V = v(X, Z, q, X0)

# affichage avec X0 constant
afficher_vorti_temp_cst(X, Z, U, V, q, X0, Y0, Z0)

# r vient de constante.py
traj = integration(X0, Y0, Z0, r)
n = 50  # 0 <= n < len(traj)
#afficher_physique_instant(traj, n, q)

# r = 10 (stable) et r = 28 (chaos)
print("Calcul pour r = 10...")
traj_r10 = integration(X0, Y0, Z0, r=10)
#afficher_physique_instant(traj_r10, -1, q)

print("Calcul pour r = 28...")
traj_r28 = integration(X0, Y0, Z0, r=28)
#afficher_physique_instant(traj_r28, -1, q)  # tester aussi n = 100, 500, -1

# animations
ani_28 = animer_lorenz_rapide(traj_r28, q=q, r=28, max_frames=250, interval=40)
ani_10 = animer_lorenz_rapide(traj_r10, q=q, r=10, max_frames=250, interval=40)

# papillons pour plusieurs r
valeurs_r = [1, 18, 28]
#papillons_r(valeurs_r)

r = 28

# REMARQUE : perturbé ou pas c'est les memes trajectoires. En chaos le systeme
# explore tout l'attracteur donc la perturbation change pas grand chose visuellement.
# avec r = 18 (pas de chaos) y'a pas de bifurcation non plus, 1e-3 ça se voit pas
#papillons_CI_comparaison([X0, Y0, Z0], r)

#comparer_r10_r28_instants(indices=[50, 300, 900])
#papillons_r_non_constant(X0, Y0, Z0)
#papillons_r_comparaison(X0, Y0, Z0, r_min=0, r_max=35, step=2, point_size=1.2)