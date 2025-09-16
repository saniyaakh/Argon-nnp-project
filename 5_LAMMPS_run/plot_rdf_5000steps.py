# plot rdf from 5000 step simulation
import numpy as np
import matplotlib.pyplot as plt

# read rdf data
rdf_data = []
with open('rdf_5k.dat', 'r') as f:
   for line in f:
       if not line.startswith('#') and 'TimeStep' not in line:
           parts = line.strip().split()
           if len(parts) >= 3:
               try:
                   r = float(parts[1])
                   gr = float(parts[2])
                   rdf_data.append([r, gr])
               except:
                   continue

rdf_array = np.array(rdf_data)

plt.figure(figsize=(8, 6))
plt.plot(rdf_array[:, 0], rdf_array[:, 1], 'navy', linewidth=2)
plt.xlabel('distance r (a)')
plt.ylabel('g(r)')
plt.title('radial distribution function (5000 steps)')
plt.grid(True, alpha=0.3)
plt.xlim(0, 8)
plt.savefig('rdf_5000steps.png', dpi=150, bbox_inches='tight')
plt.show()
