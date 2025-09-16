#!/usr/bin/env python3
"""
Analysis of LAMMPS trajectory for MSD and RDF calculations with zoomed RDF
"""

import numpy as np
import matplotlib.pyplot as plt

def read_lammpstrj(filename):
    """Read LAMMPS trajectory file"""
    frames = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        if "ITEM: TIMESTEP" in lines[i]:
            timestep = int(lines[i+1].strip())
            i += 2
            
            # Number of atoms
            if "ITEM: NUMBER OF ATOMS" in lines[i]:
                natoms = int(lines[i+1].strip())
                i += 2
            
            # Box bounds
            if "ITEM: BOX BOUNDS" in lines[i]:
                i += 1
                box = []
                for j in range(3):
                    bounds = lines[i+j].strip().split()
                    box.append([float(bounds[0]), float(bounds[1])])
                i += 3
            
            # Atoms
            if "ITEM: ATOMS" in lines[i]:
                i += 1
                atoms = []
                for j in range(natoms):
                    parts = lines[i+j].strip().split()
                    atom_id = int(parts[0])
                    atom_type = int(parts[1])
                    x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                    atoms.append([atom_id, atom_type, x, y, z])
                i += natoms
                
                frames.append({
                    'timestep': timestep,
                    'natoms': natoms,
                    'box': box,
                    'atoms': np.array(atoms)
                })
        else:
            i += 1
    
    print(f"Read {len(frames)} frames from trajectory")
    return frames

def calculate_msd(frames):
    """Calculate Mean Square Displacement"""
    if len(frames) < 2:
        print("Need at least 2 frames for MSD calculation")
        return None, None
    
    timesteps = []
    msd_values = []
    
    # Reference positions from first frame
    ref_positions = frames[0]['atoms'][:, 2:5]  # x, y, z columns
    
    for frame in frames:
        positions = frame['atoms'][:, 2:5]
        
        # Calculate displacement
        displacement = positions - ref_positions
        
        # Calculate MSD
        msd = np.mean(np.sum(displacement**2, axis=1))
        
        timesteps.append(frame['timestep'])
        msd_values.append(msd)
    
    return np.array(timesteps), np.array(msd_values)

def calculate_rdf(frames, dr=0.05, rmax=10.0):
    """Calculate Radial Distribution Function with higher resolution"""
    if len(frames) == 0:
        return None, None
    
    # Use last frame for RDF calculation
    frame = frames[-1]
    positions = frame['atoms'][:, 2:5]  # x, y, z columns
    box = frame['box']
    
    # Box dimensions
    Lx = box[0][1] - box[0][0]
    Ly = box[1][1] - box[1][0]
    Lz = box[2][1] - box[2][0]
    volume = Lx * Ly * Lz
    
    natoms = len(positions)
    
    # Distance bins with higher resolution
    nbins = int(rmax / dr)
    r_bins = np.linspace(0, rmax, nbins)
    hist = np.zeros(nbins)
    
    # Calculate all pairwise distances
    for i in range(natoms):
        for j in range(i+1, natoms):
            dx = positions[j][0] - positions[i][0]
            dy = positions[j][1] - positions[i][1]
            dz = positions[j][2] - positions[i][2]
            
            # Apply minimum image convention
            dx = dx - Lx * round(dx/Lx)
            dy = dy - Ly * round(dy/Ly)
            dz = dz - Lz * round(dz/Lz)
            
            r = np.sqrt(dx*dx + dy*dy + dz*dz)
            
            if r < rmax:
                bin_idx = int(r / dr)
                if bin_idx < nbins:
                    hist[bin_idx] += 2  # Count both i-j and j-i
    
    # Normalize RDF
    density = natoms / volume
    for i in range(nbins):
        r = (i + 0.5) * dr
        shell_volume = 4 * np.pi * r*r * dr
        expected_count = density * shell_volume * natoms
        if expected_count > 0:
            hist[i] /= expected_count
    
    return r_bins[:-1] + dr/2, hist[:-1]

def create_plots(timesteps, msd, r_values, rdf):
    """Create MSD and RDF plots with zoomed-in first coordination shell"""
    fig = plt.figure(figsize=(16, 10))
    
    # Create subplot layout: MSD (top left), full RDF (top right), zoomed RDF (bottom)
    ax1 = plt.subplot(2, 2, 1)  # MSD
    ax2 = plt.subplot(2, 2, 2)  # Full RDF
    ax3 = plt.subplot(2, 1, 2)  # Zoomed RDF
    
    # MSD plot
    if timesteps is not None and msd is not None:
        ax1.plot(timesteps * 0.001, msd, 'b-', linewidth=2)
        ax1.set_xlabel('Time (ps)', fontsize=12)
        ax1.set_ylabel('MSD (Ų)', fontsize=12)
        ax1.set_title('Mean Square Displacement', fontsize=14)
        ax1.grid(True, alpha=0.3)
    
    # Full RDF plot
    if r_values is not None and rdf is not None:
        ax2.plot(r_values, rdf, 'r-', linewidth=2)
        ax2.set_xlabel('Distance (Å)', fontsize=12)
        ax2.set_ylabel('g(r)', fontsize=12)
        ax2.set_title('Full Radial Distribution Function', fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 10)
        ax2.set_xticks(np.arange(0, 11, 2))
        
        # Zoomed RDF plot - focus on first coordination shell
        ax3.plot(r_values, rdf, 'r-', linewidth=3)
        ax3.set_xlabel('Distance (Å)', fontsize=14)
        ax3.set_ylabel('g(r)', fontsize=14)
        ax3.set_title('First Coordination Shell (Zoomed)', fontsize=16, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Zoom in on the region with the sharp peaks (0-6 Å typically covers first few shells)
        ax3.set_xlim(0, 6)
        ax3.set_xticks(np.arange(0, 6.5, 0.5))  # Ticks every 0.5 Å
        ax3.set_xticks(np.arange(0, 6.1, 0.1), minor=True)  # Minor ticks every 0.1 Å
        ax3.tick_params(axis='both', which='major', labelsize=12)
        ax3.tick_params(axis='x', which='minor', labelsize=10)
        
        # Add a box around the zoomed region in the full RDF
        from matplotlib.patches import Rectangle
        rect = Rectangle((0, 0), 6, max(rdf), linewidth=2, edgecolor='blue', 
                        facecolor='lightblue', alpha=0.2)
        ax2.add_patch(rect)
        ax2.text(3, max(rdf)*0.8, 'Zoomed\nRegion', ha='center', va='center', 
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    plt.tight_layout()
    plt.savefig('trajectory_analysis_zoomed.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Analysis plots saved as 'trajectory_analysis_zoomed.png'")

def main():
    print("Reading LAMMPS trajectory...")
    frames = read_lammpstrj('trajectory_fcc.lammpstrj')
    
    if not frames:
        print("No frames found in trajectory!")
        return
    
    print("Calculating MSD...")
    timesteps, msd = calculate_msd(frames)
    
    print("Calculating RDF with higher resolution...")
    r_values, rdf = calculate_rdf(frames)
    
    print("Creating plots with zoomed first coordination shell...")
    create_plots(timesteps, msd, r_values, rdf)
    
    if msd is not None:
        print(f"Final MSD: {msd[-1]:.4f} Ų")
    
    print("Analysis complete!")

if __name__ == "__main__":
    main()
