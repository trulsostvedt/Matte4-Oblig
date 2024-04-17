import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Parametere
L = 1.0  # Lengde på domenet
T = 1.0  # Total tid
Nx = 50  # Antall rutenettspunkter i x
Ny = 50  # Antall rutenettspunkter i y
Nt = 100  # Antall tidssteg
alpha = 0.01  # Termisk diffusivitet

# Rutenettavstander
dx = L / (Nx - 1)
dy = L / (Ny - 1)
dt = T / Nt

# Funksjon for initialbetingelser
def initial_condition(x, y):
    return np.sin(np.pi * x) * np.sin(np.pi * y)

# Lag rutenettet
x = np.linspace(0, L, Nx)
y = np.linspace(0, L, Ny)
X, Y = np.meshgrid(x, y)

# Initialiser temperaturfeltet
u = initial_condition(X, Y)

# Randbetingelser (fast temperatur ved grensene)
u[:, 0] = 0
u[:, -1] = 0
u[0, :] = 0
u[-1, :] = 0

# Funksjon for å oppdatere plottet for animasjonen
def update_plot(frame, plot):
    # Oppdater temperaturfeltet
    for n in range(Nt):
        un = u.copy()
        u[1:-1, 1:-1] = un[1:-1, 1:-1] + alpha * dt * (
                (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[:-2, 1:-1]) / dx**2 +
                (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, :-2]) / dy**2
            )

    # Oppdater plottet
    plot[0].remove()
    plot[0] = ax.plot_surface(X, Y, u, cmap='coolwarm')

# Lag 3D-plottet
fig = plt.figure()
plt.title('Varmelikningen i 3D')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
plt.axis('off')
ax = fig.add_subplot(111, projection='3d')

# Plott initialbetingelsen
plot = [ax.plot_surface(X, Y, u, cmap='coolwarm')]

# Sett plottets parametere
ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.set_zlim(0, 1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Temperatur')

# Lag animasjonen
ani = animation.FuncAnimation(fig, update_plot, frames=Nt, fargs=(plot,), interval=500, repeat=True)

# Vis animasjonen
plt.show()
