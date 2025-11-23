# SIMULATION 5: CMB Geometric Verification
# Goal: Calculate the angular scale of the first acoustic peak in the Isothermal Machian Universe.
# Verify if the 'Static Universe + Mass Evolution' duality preserves the CMB geometry.

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy.integrate import quad

# Add the current directory to path to import cosmology
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import cosmology
except ImportError:
    from lab.simulation import cosmology

# Constants
c_km_s = 299792.458
H0 = 70.0
z_cmb = 1090.0  # Recombination redshift

def calculate_angular_diameter_distance_lcdm(z):
    # Standard LCDM Angular Diameter Distance.
    # D_A = D_M / (1+z)
    # D_M = c/H0 * Integral[ dz/E(z) ]
    def integrand(z_prime):
        return 1.0 / cosmology.hubble_parameter(z_prime)
    
    result, _ = quad(integrand, 0, z)
    dm = (c_km_s / H0) * result # Mpc
    da = dm / (1 + z)
    return da

def calculate_angular_diameter_distance_machian(z):
    # Machian Angular Diameter Distance.
    # In a static universe, D_A = D_proper.
    # D_proper = c * t_lookback
    
    # lookback_time_machian returns Gyr. We need Mpc.
    # 1 Gyr * c = 306.601 Mpc
    t_gyr = cosmology.lookback_time_machian(z)
    da = t_gyr * 306.601  # Mpc
    return da

def run_simulation():
    print(f"Running Experiment 5: CMB Geometric Verification (z={z_cmb})")
    print("-" * 60)
    
    # 1. Calculate Distances
    print("Calculating Angular Diameter Distances...")
    d_a_lcdm = calculate_angular_diameter_distance_lcdm(z_cmb)
    d_a_machian = calculate_angular_diameter_distance_machian(z_cmb)
    
    print(f"LCDM D_A(z={z_cmb}):    {d_a_lcdm:.2f} Mpc")
    print(f"Machian D_A(z={z_cmb}): {d_a_machian:.2f} Mpc")
    
    ratio_d = d_a_machian / d_a_lcdm
    print(f"Ratio (Machian/LCDM): {ratio_d:.2f}")
    
    # 2. The Sound Horizon Problem
    # In LCDM, r_s (comoving) approx 144.43 Mpc. Physical r_s = 144.43 / (1+z)
    # Theta = r_s_phys / D_A = (144.43 / 1091) / 12.7 = 144.43 / D_M
    r_s_comoving_lcdm = 144.43 # Mpc (Planck 2018 approx)
    theta_lcdm = r_s_comoving_lcdm / (d_a_lcdm * (1 + z_cmb)) # rad
    
    print(f"\nStandard LCDM Prediction:")
    print(f"Sound Horizon (Comoving): {r_s_comoving_lcdm:.2f} Mpc")
    print(f"Angular Scale theta:      {theta_lcdm:.6f} rad ({np.degrees(theta_lcdm):.4f} deg)")
    print(f"Multipole l ~ pi/theta:   {np.pi/theta_lcdm:.1f}")

    # 3. Machian Interpretation
    # If physics is conformally dual, the dimensionless angle must match.
    # theta_machian = r_s_machian_phys / d_a_machian
    
    # Let's solve for the required r_s to match observations
    required_r_s = theta_lcdm * d_a_machian
    
    print(f"\nMachian Analysis:")
    print(f"Distance to Surface:      {d_a_machian:.2f} Mpc")
    print(f"Required Ruler Size:      {required_r_s:.2f} Mpc (to match peak)")
    
    scaling_factor = required_r_s / (r_s_comoving_lcdm / (1+z_cmb))
    print(f"Scaling vs LCDM Physical: {scaling_factor:.2f}x")
    
    # Plotting the Distance Ladder
    z_range = np.linspace(0, 1200, 1000)
    da_l = []
    da_m = []
    
    for z in z_range:
        da_l.append(calculate_angular_diameter_distance_lcdm(z))
        da_m.append(calculate_angular_diameter_distance_machian(z))
        
    plt.figure(figsize=(10, 6))
    plt.plot(z_range, da_l, 'r--', label='LCDM D_A')
    plt.plot(z_range, da_m, 'c-', label='Machian D_A (Static)')
    plt.axvline(z_cmb, color='k', linestyle=':', alpha=0.5, label='Recombination')
    plt.title("Angular Diameter Distance: Expanding vs Static")
    plt.xlabel("Redshift z")
    plt.ylabel("Distance (Mpc)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_file = "experiment_5_cmb_result.png"
    plt.savefig(output_file)
    print(f"\nPlot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
