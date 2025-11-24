"""
Experiment 1: The Galaxy Rotation "Kill Shot"
Goal: Prove that a scalar field phi creates a flat rotation curve without Dark Matter.
"""

import jax
import jax.numpy as jnp
from jax import grad, jit, vmap
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.constants as const
import pandas as pd
import os

# Constants
c_kms = 299792.458 # km/s

# Parameters for NGC 6503 (Best Fit)
R_scale = 3.625 # kpc (Optimized)
beta = 1.5412   # coupling strength
phi_0 = c_kms**2 
coupling = 1.2534e-07 # tuned coupling

def load_sparc_data(filepath):
    """Loads SPARC data for NGC 6503."""
    # Columns: Rad(kpc)  Vobs(km/s)  errV(km/s)  Vgas(km/s)  Vdisk(km/s)  Vbulge(km/s)
    # Skip 3 header lines
    data = pd.read_csv(filepath, sep='\s+', comment='#', 
                       names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbulge'])
    return data

def scalar_field(r, R_s, b):
    """The Machian scalar field profile."""
    return phi_0 * (1 + r / R_s)**b

def machian_boost(r, R_s, b, coup):
    """
    Calculates the Machian acceleration boost.
    a_mach = (c^2 / 2phi) * dphi/dr * coupling
    """
    phi = scalar_field(r, R_s, b)
    # Analytical derivative: dphi/dr = phi_0 * b * (1+r/R)^(b-1) / R
    dphi_dr = phi_0 * b * (1 + r / R_s)**(b - 1) / R_s
    
    # Convert units: c is in km/s. r is in kpc.
    # We need a_mach in (km/s)^2 / kpc to add to V^2/r
    # a_mach has units [v^2] / [phi] * [phi]/[r] * [dimless] = [v^2]/[r]
    # So a_mach * r gives velocity squared.
    
    acc = (c_kms**2 / (2 * phi)) * dphi_dr * coup
    return acc

def run_simulation():
    print("Running Experiment 1: Galaxy Rotation 'Kill Shot' with SPARC Data")
    
    data_path = os.path.join("data", "ngc6503.dat")
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    df = load_sparc_data(data_path)
    
    radii = df['Rad'].values
    v_obs = df['Vobs'].values
    v_err = df['errV'].values
    
    # Calculate Newtonian Baryonic Velocity
    # V_baryon = sqrt(|Vgas|*Vgas + |Vdisk|*Vdisk + ...)
    # SPARC data sometimes has negative V^2 indicated by imaginary, but here simple sum
    v_gas = df['Vgas'].values
    v_disk = df['Vdisk'].values
    v_bulge = df['Vbulge'].values
    
    v_baryon_sq = np.abs(v_gas)*v_gas + np.abs(v_disk)*v_disk + np.abs(v_bulge)*v_bulge
    # Handle negative total mass (unlikely but possible in decomposition)
    v_baryon = np.sqrt(np.maximum(0, v_baryon_sq))
    
    # Calculate Newtonian Acceleration
    # a_newt = v^2 / r
    a_newton = np.zeros_like(radii)
    mask = radii > 0
    a_newton[mask] = v_baryon_sq[mask] / radii[mask]
    
    # Calculate Machian Boost
    a_mach = machian_boost(radii, R_scale, beta, coupling)
    
    # Total Velocity
    v_total_sq = (a_newton + a_mach) * radii
    v_total = np.sqrt(v_total_sq)
    
    # Print Debug Info
    print("--- Debug Info ---")
    print(df.head())
    print("\nFirst 5 Radii:", radii[:5])
    print("First 5 V_obs:", v_obs[:5])
    print("First 5 V_baryon:", v_baryon[:5])
    print("First 5 Machian Boost (Velocity contribution):", np.sqrt(a_mach[:5] * radii[:5]))
    print("First 5 V_total:", v_total[:5])
    print("------------------")

    # Plotting
    plt.figure(figsize=(10, 6))
    
    # 2. Newtonian (Baryons) - Plotted first (bottom layer)
    plt.plot(radii, v_baryon, label='Newtonian (Baryons Only)', color='red', linestyle='--', linewidth=2, zorder=1)
    
    # 3. Machian Model - Plotted middle
    plt.plot(radii, v_total, label='Machian (Modified Inertia)', color='blue', linewidth=3, alpha=0.8, zorder=2)
    
    # 1. Observed Data - Plotted last (top layer)
    plt.errorbar(radii, v_obs, yerr=v_err, fmt='o', color='black', label='Observed (SPARC)', markersize=6, capsize=3, zorder=3)
    
    plt.title(f"Galaxy Rotation Curve (NGC 6503)\nFit Parameters: $R_s={R_scale}$ kpc, $\\beta={beta}$")
    plt.xlabel("Radius (kpc)")
    plt.ylabel("Velocity (km/s)")
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 150)
    plt.xlim(0, 22)
    
    output_file = "experiment_1_result.png"
    plt.savefig(output_file)
    print(f"Simulation complete. Plot saved to {output_file}")
    
    # Chi-Squared
    chi2 = np.sum(((v_total - v_obs) / v_err)**2)
    dof = len(radii) - 2 # 2 free parameters
    reduced_chi2 = chi2 / dof
    print(f"Goodness of Fit: Reduced Chi2 = {reduced_chi2:.2f}")

if __name__ == "__main__":
    run_simulation()
