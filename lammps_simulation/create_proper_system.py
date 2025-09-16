#!/usr/bin/env python3
"""Create a properly spaced Argon system"""
import numpy as np

def create_fcc_argon(nx=4, ny=4, nz=4, lattice_param=5.26):
    """Create FCC Argon structure with proper spacing"""
    atoms = []
    atom_id = 1
    
    # FCC unit cell positions (fractional coordinates)
    fcc_positions = [
        [0.0, 0.0, 0.0],
        [0.5, 0.5, 0.0],
        [0.5, 0.0, 0.5],
        [0.0, 0.5, 0.5]
    ]
    
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                for pos in fcc_positions:
                    x = (i + pos[0]) * lattice_param
                    y = (j + pos[1]) * lattice_param
                    z = (k + pos[2]) * lattice_param
                    atoms.append([atom_id, 1, x, y, z])
                    atom_id += 1
    
    # Box dimensions
    xhi = nx * lattice_param
    yhi = ny * lattice_param
    zhi = nz * lattice_param
    
    # Write LAMMPS data file
    with open("structure_fcc.data", 'w') as f:
        f.write("LAMMPS data file for FCC Argon crystal\n\n")
        f.write(f"{len(atoms)} atoms\n")
        f.write("1 atom types\n\n")
        f.write(f"0.0 {xhi:.6f} xlo xhi\n")
        f.write(f"0.0 {yhi:.6f} ylo yhi\n")
        f.write(f"0.0 {zhi:.6f} zlo zhi\n\n")
        f.write("Masses\n\n")
        f.write("1 39.948  # Ar\n\n")
        f.write("Atoms\n\n")
        
        for atom in atoms:
            f.write(f"{atom[0]} {atom[1]} {atom[2]:.6f} {atom[3]:.6f} {atom[4]:.6f}\n")
    
    print(f"Created FCC Argon system with {len(atoms)} atoms")
    print(f"Box size: {xhi:.2f} x {yhi:.2f} x {zhi:.2f} Angstroms")
    return len(atoms)

if __name__ == "__main__":
    create_fcc_argon()
