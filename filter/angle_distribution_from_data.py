import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from itertools import combinations
from tqdm import tqdm

def read_n2p2_data(filepath):
    cell = []
    positions = []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("lattice"):
                parts = line.split()
                cell.append(list(map(float, parts[1:4])))
            elif line.startswith("atom"):
                parts = line.split()
                positions.append(list(map(float, parts[1:4])))

    return np.array(cell), np.array(positions)

def minimum_image(r_ij, cell):
    """Apply periodic boundary conditions using the minimum image convention"""
    inv_cell = np.linalg.inv(cell.T)
    fractional = np.dot(inv_cell, r_ij.T).T
    fractional -= np.round(fractional)
    return np.dot(cell.T, fractional.T).T

def compute_all_angles(cell, positions, r_cut=6.0):
    angles = []
    n_atoms = len(positions)

    # Compute distance matrix with PBC
    for center in tqdm(range(n_atoms), desc="Computing angles"):
        vecs = []
        for j in range(n_atoms):
            if j == center:
                continue
            rij = minimum_image(positions[j] - positions[center], cell)
            dist = np.linalg.norm(rij)
            if dist < r_cut:
                vecs.append(rij)

        # For all vector pairs (k,i) around central atom
        for v1, v2 in combinations(vecs, 2):
            cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            theta = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
            angles.append(theta)

    return np.array(angles)

def plot_angle_distribution(angles, bins=180):
    plt.figure(figsize=(8,6))
    plt.hist(angles, bins=bins, range=(0,180), color='skyblue', edgecolor='black')
    plt.xlabel("Angle θ (degrees)")
    plt.ylabel("Frequency")
    plt.title("Three-body Angle Distribution (θₖᵢⱼ)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python angle_distribution_from_data.py file.data")
        exit()

    filepath = sys.argv[1]
    cell, positions = read_n2p2_data(filepath)
    angles = compute_all_angles(cell, positions)
    print(f"Computed {len(angles)} angles.")
    plot_angle_distribution(angles)

