"""
SIMULATION 2: Lookback Time Calculator
Goal: Replicate the "Lookback Time" divergence and the future singularity predicted at z approx -1.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the current directory to path to import cosmology
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import cosmology
except ImportError:
    # If running from root
    from lab.simulation import cosmology

def run_simulation():
    print("Running Experiment 2: The 'Blue Screen of Death' Cosmology")
    
    # 1. SETUP
    # Create array of redshifts z = np.linspace(-0.9, 15, 100)
    z_values = np.linspace(-0.9, 15, 100)
    
    # 2. CALCULATE TIMES
    times_machian = []
    times_lcdm = []
    
    print("Calculating lookback times...")
    for z in z_values:
        t_m = cosmology.lookback_time_machian(z)
        t_l = cosmology.lookback_time_lcdm(z)
        times_machian.append(t_m)
        times_lcdm.append(t_l)
        
    # 3. CHECK FOR "IMPOSSIBLE GALAXIES"
    z_check = 10.0
    t_m_10 = cosmology.lookback_time_machian(z_check)
    t_l_10 = cosmology.lookback_time_lcdm(z_check)
    
    print(f"\n--- Age of Universe at z={z_check} ---")
    print(f"Standard LCDM: {t_l_10:.2f} Gyr")
    print(f"Machian Model: {t_m_10:.2f} Gyr")
    
    if t_m_10 > t_l_10 + 1.0:
        print("SUCCESS: Machian universe is significantly older at high z, allowing for 'impossible' galaxies.")
    else:
        print("WARNING: Ages are similar.")
        
    # 4. CHECK FOR SINGULARITY
    print("\n--- Future Evolution ---")
    time_left = cosmology.time_to_singularity()
    print(f"Time to 'Blue Screen of Death' (z=-1): {time_left:.2f} Gyr")
    
    if time_left > 0 and time_left < 100:
        print("SUCCESS: Future singularity detected at finite time.")
    else:
        print("WARNING: Singularity time is unexpected.")
        
    # 5. PLOTTING
    plt.figure(figsize=(10, 6))
    plt.plot(z_values, times_machian, label='Machian (Mass Evolution)', color='cyan', linewidth=2)
    plt.plot(z_values, times_lcdm, label='Standard LCDM', color='red', linestyle='--', linewidth=2)
    
    plt.title("Lookback Time vs Redshift")
    plt.xlabel("Redshift z")
    plt.ylabel("Lookback Time (Gyr)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axvline(x=0, color='k', linewidth=0.5)
    
    # Annotate z=10
    plt.plot([z_check], [t_m_10], 'co')
    plt.annotate(f"z={z_check}\nt={t_m_10:.1f} Gyr", (z_check, t_m_10), xytext=(z_check-2, t_m_10-5), arrowprops=dict(arrowstyle="->", color='cyan'))
    
    output_file = "experiment_2_result.png"
    plt.savefig(output_file)
    print(f"\nPlot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
