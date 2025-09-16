#!/usr/bin/env python3
"""
Simple converter for n2p2 atom data to LAMMPS format
"""

def convert_atoms_to_lammps(input_file, output_file):
    """Convert n2p2 atom data to LAMMPS data file"""
    
    atoms = []
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('atom'):
                parts = line.split()
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                element = parts[4]  # Should be 'Ar'
                
                atoms.append({
                    'id': len(atoms) + 1,
                    'type': 1,  # Argon type
                    'x': x, 'y': y, 'z': z
                })
    
    # Find box bounds from atom positions
    if atoms:
        xs = [atom['x'] for atom in atoms]
        ys = [atom['y'] for atom in atoms]
        zs = [atom['z'] for atom in atoms]
        
        xlo, xhi = min(xs) - 2.0, max(xs) + 2.0
        ylo, yhi = min(ys) - 2.0, max(ys) + 2.0
        zlo, zhi = min(zs) - 2.0, max(zs) + 2.0
    
    # Write LAMMPS data file
    with open(output_file, 'w') as f:
        f.write("LAMMPS data file for Argon system from n2p2\n\n")
        f.write(f"{len(atoms)} atoms\n")
        f.write("1 atom types\n\n")
        
        f.write(f"{xlo:.6f} {xhi:.6f} xlo xhi\n")
        f.write(f"{ylo:.6f} {yhi:.6f} ylo yhi\n") 
        f.write(f"{zlo:.6f} {zhi:.6f} zlo zhi\n\n")
        
        f.write("Masses\n\n")
        f.write("1 39.948  # Ar\n\n")
        
        f.write("Atoms\n\n")
        for atom in atoms:
            f.write(f"{atom['id']} {atom['type']} {atom['x']:.6f} {atom['y']:.6f} {atom['z']:.6f}\n")
    
    print(f"Converted {len(atoms)} atoms to LAMMPS format")
    print(f"Box bounds: x=[{xlo:.2f}, {xhi:.2f}], y=[{ylo:.2f}, {yhi:.2f}], z=[{zlo:.2f}, {zhi:.2f}]")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    convert_atoms_to_lammps("../validation_500_clean/output.data", "structure.data")
