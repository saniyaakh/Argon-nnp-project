# plot msd and pdf from 1000 step simulation
import numpy as np
import matplotlib.pyplot as plt

# read msd data
msd_data = np.loadtxt('msd-all.dat', skiprows=1)
plt.figure(figsize=(12, 5))

# msd plot
plt.subplot(1, 2, 1)
plt.plot(msd_data[:, 0], msd_data[:, 1], 'purple', linewidth=2)
plt.xlabel('time (ps)')
plt.ylabel('msd (a^2)')
plt.title('mean squared displacement (1000 steps)')
plt.grid(True, alpha=0.3)

# pdf plot
plt.subplot(1, 2, 2)
pdf_data = np.loadtxt('pdf-X-X.dat', skiprows=1)
distances = pdf_data[:, 0]
pdf_values = pdf_data[:, 1]

plt.plot(distances, pdf_values, 'navy', linewidth=2)
plt.xlabel('distance r (a)')
plt.ylabel('pdf g(r)')
plt.title('pair distribution function (1000 steps)')
plt.grid(True, alpha=0.3)
plt.xlim(0, 8)

plt.tight_layout()
plt.savefig('msd_pdf_1000steps.png', dpi=150, bbox_inches='tight')
plt.show()
