#!/usr/bin/env python3
"""
Convert n2p2 output.data format to LAMMPS structure.data format
"""

def convert_n2p2_to_lammps(input_file, output_file):
    """Convert n2p2 structure to LAMMPS data file"""
    
    atoms = []
    box_info = None
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Parse the structure
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('begin'):
            i += 1
            continue
        elif line.startswith('comment'):
            i += 1
            continue
        elif line.startswith('lattice'):
            # Read lattice vectors
            lattice = []
            for j in range(3):
                i += 1
                vec = [float(x) for x in lines[i].strip().split()]
                lattice.append(vec)
            
            # Calculate box bounds (assuming orthogonal for simplicity)
            box_info = {
                'xlo': 0.0, 'xhi': lattice[0][0],
                'ylo': 0.0, 'yhi': lattice[1][1], 
                'zlo': 0.0, 'zhi': lattice[2][2]
            }
            i += 1
            continue
        elif line.startswith('atom'):
            parts = line.split()
            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
            element = parts[4]  # Should be 'Ar'
            
            atoms.append({
                'id': len(atoms) + 1,
                'type': 1,  # Argon type
                'x': x, 'y': y, 'z': z
            })
        i += 1
        
        # Only process first structure
        if line.startswith('end'):
            break
    
    # Write LAMMPS data file
    with open(output_file, 'w') as f:
        f.write("LAMMPS data file for Argon system from n2p2\n\n")
        f.write(f"{len(atoms)} atoms\n")
        f.write("1 atom types\n\n")
        
        if box_info:
            f.write(f"{box_info['xlo']:.6f} {box_info['xhi']:.6f} xlo xhi\n")
            f.write(f"{box_info['ylo']:.6f} {box_info['yhi']:.6f} ylo yhi\n") 
            f.write(f"{box_info['zlo']:.6f} {box_info['zhi']:.6f} zlo zhi\n\n")
        else:
            # Default box if lattice not found
            f.write("0.0 13.0 xlo xhi\n")
            f.write("0.0 13.0 ylo yhi\n")
            f.write("0.0 13.0 zlo zhi\n\n")
        
        f.write("Masses\n\n")
        f.write("1 39.948  # Ar\n\n")
        
        f.write("Atoms\n\n")
        for atom in atoms:
            f.write(f"{atom['id']} {atom['type']} {atom['x']:.6f} {atom['y']:.6f} {atom['z']:.6f}\n")
    
    print(f"Converted {len(atoms)} atoms to LAMMPS format")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    convert_n2p2_to_lammps("../validation_500_clean/output.data", "structure.data")
