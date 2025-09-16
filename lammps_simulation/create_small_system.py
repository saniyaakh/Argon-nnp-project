#!/usr/bin/env python3
"""Create a smaller system for testing"""

def create_small_system():
    atoms = []
    atom_id = 1
    
    with open("structure.data", 'r') as f:
        lines = f.readlines()
    
    # Find the atoms section
    in_atoms = False
    for line in lines:
        if line.strip() == "Atoms":
            in_atoms = True
            continue
        elif in_atoms and line.strip() and not line.startswith("#"):
            atoms.append(line.strip())
            atom_id += 1
            if len(atoms) >= 1000:  # Take only first 1000 atoms
                break
    
    # Write smaller system
    with open("structure_small.data", 'w') as f:
        f.write("LAMMPS data file for small Argon test system\n\n")
        f.write(f"{len(atoms)} atoms\n")
        f.write("1 atom types\n\n")
        f.write("-2.0 15.35 xlo xhi\n")
        f.write("-2.0 15.35 ylo yhi\n")
        f.write("-2.0 15.35 zlo zhi\n\n")
        f.write("Masses\n\n")
        f.write("1 39.948  # Ar\n\n")
        f.write("Atoms\n\n")
        
        for i, atom_line in enumerate(atoms):
            parts = atom_line.split()
            f.write(f"{i+1} 1 {parts[2]} {parts[3]} {parts[4]}\n")
    
    print(f"Created small system with {len(atoms)} atoms")

if __name__ == "__main__":
    create_small_system()
