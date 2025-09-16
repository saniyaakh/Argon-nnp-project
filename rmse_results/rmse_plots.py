#!/usr/bin/env python3
"""
RMSE Validation Analysis Script for n2p2 Neural Network Potentials
Creates RMSE per structure plots for energy and forces validation

Author: Generated for Argon NNP validation
Date: July 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def read_energy_comp(filename):
    """Read energy.comp file and return structure indices, reference and predicted energies"""
    indices = []
    ref_energies = []
    nnp_energies = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                index = int(parts[0])
                ref_energy = float(parts[2])
                nnp_energy = float(parts[3])
                
                indices.append(index)
                ref_energies.append(ref_energy)
                nnp_energies.append(nnp_energy)
    
    return np.array(indices), np.array(ref_energies), np.array(nnp_energies)

def read_forces_comp(filename):
    """Read forces.comp file and return structure-wise force data"""
    # Group forces by structure index
    structure_forces = defaultdict(lambda: {'ref': [], 'nnp': []})
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                struct_idx = int(parts[0])
                ref_force = float(parts[2])
                nnp_force = float(parts[3])
                
                structure_forces[struct_idx]['ref'].append(ref_force)
                structure_forces[struct_idx]['nnp'].append(nnp_force)
    
    return structure_forces

def calculate_energy_rmse_per_structure(indices, ref_energies, nnp_energies):
    """Calculate RMSE per structure for energies"""
    # For energies, we have one value per structure
    rmse_per_structure = np.abs(ref_energies - nnp_energies)  # Actually absolute error for energy
    return indices, rmse_per_structure

def calculate_force_rmse_per_structure(structure_forces):
    """Calculate RMSE per structure for forces"""
    indices = []
    rmse_values = []
    
    for struct_idx in sorted(structure_forces.keys()):
        ref_forces = np.array(structure_forces[struct_idx]['ref'])
        nnp_forces = np.array(structure_forces[struct_idx]['nnp'])
        
        # Calculate RMSE for this structure
        rmse = np.sqrt(np.mean((ref_forces - nnp_forces)**2))
        
        indices.append(struct_idx)
        rmse_values.append(rmse)
    
    return np.array(indices), np.array(rmse_values)

def create_rmse_plots():
    """Create RMSE plots for energy and forces"""
    
    print("Reading energy comparison data...")
    energy_indices, ref_energies, nnp_energies = read_energy_comp('energy.comp')
    
    print("Reading forces comparison data...")
    structure_forces = read_forces_comp('forces.comp')
    
    print("Calculating RMSE values...")
    # Calculate RMSE per structure
    energy_indices, energy_rmse = calculate_energy_rmse_per_structure(energy_indices, ref_energies, nnp_energies)
    force_indices, force_rmse = calculate_force_rmse_per_structure(structure_forces)
    
    # Calculate mean RMSE values
    mean_energy_rmse = np.mean(energy_rmse)
    mean_force_rmse = np.mean(force_rmse)
    
    print(f"Mean Energy RMSE: {mean_energy_rmse:.6f}")
    print(f"Mean Force RMSE: {mean_force_rmse:.6f}")
    
    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Energy RMSE plot
    ax1.scatter(energy_indices, energy_rmse, c='red', alpha=0.7, s=8)
    ax1.axhline(y=mean_energy_rmse, color='orange', linestyle='--', 
                label=f'Mean Energy RMSE: {mean_energy_rmse:.6f}')
    ax1.set_xlabel('Structure Index')
    ax1.set_ylabel('Energy RMSE')
    ax1.set_title('Energy RMSE vs Structure Index')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Force RMSE plot
    ax2.scatter(force_indices, force_rmse, c='blue', alpha=0.7, s=8)
    ax2.axhline(y=mean_force_rmse, color='red', linestyle='--', 
                label=f'Mean Force RMSE: {mean_force_rmse:.6f}')
    ax2.set_xlabel('Structure Index')
    ax2.set_ylabel('RMSE')
    ax2.set_title('RMSE vs Structure Index')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('rmse_validation_plots.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Plots saved as 'rmse_validation_plots.png'")
    print(f"Total structures analyzed: {len(energy_indices)}")

if __name__ == "__main__":
    create_rmse_plots()
