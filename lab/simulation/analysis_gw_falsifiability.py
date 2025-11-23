import numpy as np
import matplotlib.pyplot as plt

def calculate_falsifiability():
    """
    Calculates the Gravitational Wave Luminosity Distance deviation for the IMU
    and determines the redshift horizon for falsification.
    """
    z = np.logspace(-2, 1.5, 100) # z from 0.01 to ~30
    
    # 1. Theoretical Prediction (IMU)
    # d_GW / d_EM = 1 / (1+z)
    ratio_imu = 1.0 / (1 + z)
    
    # 2. Standard General Relativity
    ratio_gr = np.ones_like(z)
    
    # 3. Sensitivity Curves (Approximate fractional error on distance measurement)
    # Based on LISA and Einstein Telescope white papers
    def error_model(z_val):
        # Simple heuristic model:
        # Low z: limited by peculiar velocities (high error)
        # Mid z (1-3): Sweet spot for LISA (low error)
        # High z (>5): SNR drops (error increases)
        
        base_error = 0.05 # 5% baseline
        # Increase at low z
        low_z_noise = 0.1 / (z_val * 100 + 1) 
        # Increase at high z
        high_z_noise = 0.01 * z_val
        
        return base_error + low_z_noise + high_z_noise

    sigma = error_model(z)
    
    # 4. Determine Falsifiability
    # Where does the IMU prediction fall outside the GR 5-sigma band?
    # Condition: |1 - ratio_imu| > 5 * sigma
    
    deviation = np.abs(1 - ratio_imu)
    threshold = 5 * sigma
    
    falsifiable_indices = np.where(deviation > threshold)[0]
    
    if len(falsifiable_indices) > 0:
        z_crit = z[falsifiable_indices[0]]
        print(f"Falsifiability Horizon (5-sigma): z > {z_crit:.3f}")
    else:
        print("Model is not falsifiable within z < 30 (Check error model)")

    # 5. Plotting
    plt.figure(figsize=(10, 6))
    
    plt.plot(z, ratio_gr, 'k--', label='General Relativity (Standard)')
    plt.fill_between(z, ratio_gr - 5*sigma, ratio_gr + 5*sigma, color='gray', alpha=0.2, label='GR 5-sigma Confidence')
    
    plt.plot(z, ratio_imu, 'r-', linewidth=2, label='Isothermal Machian (alpha_M = -2)')
    
    # Markers for instruments
    plt.axvline(x=0.01, color='b', linestyle=':', alpha=0.5)
    plt.text(0.011, 0.2, 'LIGO (GW170817)', rotation=90, color='b')
    
    plt.axvline(x=2.0, color='g', linestyle=':', alpha=0.5)
    plt.text(2.1, 0.2, 'LISA Peak Sensitivity', rotation=90, color='g')
    
    plt.xlabel('Redshift z')
    plt.ylabel('GW / EM Luminosity Distance Ratio')
    plt.title('The Smoking Gun: GW Luminosity Distance Falsifiability')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.savefig('gw_luminosity_prediction.png')
    print("Plot saved to gw_luminosity_prediction.png")

if __name__ == "__main__":
    calculate_falsifiability()
