import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from simulation import cosmology
from simulation.black_hole import BlackHole

# Ensure output directory exists
output_dir = "papers/figures"
os.makedirs(output_dir, exist_ok=True)

def load_sparc_data_pandas(filepath):
    """Loads SPARC data for NGC 6503 using Pandas."""
    # Columns: Rad(kpc)  Vobs(km/s)  errV(km/s)  Vgas(km/s)  Vdisk(km/s)  Vbulge(km/s)
    try:
        data = pd.read_csv(filepath, sep='\s+', comment='#', 
                           names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbulge'])
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def generate_rotation_curve():
    print("Generating Figure 1: Galaxy Rotation Curve...")
    
    # Optimized Parameters for NGC 6503 (Chi2 ~ 40.6)
    # Note: m0 is implicitly part of the baryon data for the fit, 
    # but for the analytic smooth line we still use a point mass approx + profile guess?
    # Actually, let's just use the fit parameters for the Machian part.
    
    scale_length = 3.625 # Fitted R
    beta = 1.5412        # Fitted Beta
    coupling = 1.2534e-07 # Fitted Coupling
    m0_approx = 4.0e9    # Approx Baryonic Mass for analytic line (tuned for visual match if needed)
    
    c_val = 299792.458 # km/s
    phi_0 = c_val**2
    
    # Load Real Data First
    data_path = "data/ngc6503.dat"
    df = None
    if os.path.exists(data_path):
        df = load_sparc_data_pandas(data_path)
    
    r_model = np.linspace(0.1, 25, 100)
    
    # Define Physics
    def calculate_machian_velocity_analytic(r_val):
        # Analytic Machian Acceleration (Fifth Force approximation)
        # a_mach = (c^2 * coup * beta) / (2 * R * (1 + r/R))
        
        a_machian = (c_val**2 * coupling * beta) / (2 * scale_length * (1 + r_val / scale_length))
        
        # Analytic Newtonian (Approximate Baryonic Potential)
        # Use a simple Pseudo-Isothermal or Exponential Disk profile for the smooth line
        # v_baryon^2 approx V_max^2 * (1 - exp(-r/R_disk))?
        # NGC 6503 V_baryon peaks around 95 km/s at 5kpc.
        v_baryon_analytic_sq = (95.0**2) * (r_val / (r_val + 1.5)) # Simple rise
        
        v_sq = v_baryon_analytic_sq + r_val * a_machian
        return np.sqrt(v_sq)

    # Calculate Model Curve (Smooth)
    v_machian_smooth = [calculate_machian_velocity_analytic(ri) for ri in r_model]
    
    plt.figure(figsize=(10, 6))
    plt.style.use('default') # Ensure white background
    
    # 1. Plot Baryonic (Newtonian) Contribution if available
    if df is not None:
        radii = df['Rad'].values
        v_obs = df['Vobs'].values
        v_err = df['errV'].values
        v_gas = df['Vgas'].values
        v_disk = df['Vdisk'].values
        v_bulge = df['Vbulge'].values
        
        # Calculate Total Baryonic Velocity
        v_baryon_sq = np.abs(v_gas)*v_gas + np.abs(v_disk)*v_disk + np.abs(v_bulge)*v_bulge
        v_baryon = np.sqrt(np.maximum(0, v_baryon_sq))
        
        # Plot Newtonian (Baryons)
        plt.plot(radii, v_baryon, label='Newtonian (Baryons)', color='red', linestyle='--', linewidth=2)
        
        # Plot Observed Data
        plt.errorbar(radii, v_obs, yerr=v_err, fmt='o', color='black', label='Observed (SPARC)', markersize=4)
        
        # Calculate Machian Fit using REAL Baryons + Optimized Boost
        a_mach_data = (c_val**2 * coupling * beta) / (2 * scale_length * (1 + radii / scale_length))
        v_mach_total_data = np.sqrt(v_baryon_sq + radii * a_mach_data)
        
        # Plot the Machian Fit based on REAL Baryons (connected line)
        plt.plot(radii, v_mach_total_data, label=f'Machian Fit', color='blue', linewidth=2)

    else:
        # Fallback if no data
        plt.plot(r_model, v_machian_smooth, label=f'Machian Model (Analytic)', color='blue', linewidth=2)

    plt.title(f"Galaxy Rotation Curve: NGC 6503")
    plt.xlabel("Radius (kpc)")
    plt.ylabel("Velocity (km/s)")
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    
    plt.savefig(f"{output_dir}/fig1_rotation_curve.png", dpi=300)
    plt.close()

def generate_cosmology_plot():
    print("Generating Figure 2: Age vs Redshift...")
    
    z_range = np.linspace(0, 15, 100)
    machian_ages = [cosmology.lookback_time_machian(z) for z in z_range]
    lcdm_ages = [cosmology.lookback_time_lcdm(z) for z in z_range]
    
    plt.figure(figsize=(10, 6))
    plt.plot(z_range, machian_ages, label='Machian Universe (Static)', color='blue', linewidth=2)
    plt.plot(z_range, lcdm_ages, label='Standard LCDM (Expanding)', color='red', linestyle='dashed')
    
    plt.title("Lookback Time vs Redshift")
    plt.xlabel("Redshift (z)")
    plt.ylabel("Lookback Time (Gyr)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    # Removed dark_background
    
    plt.savefig(f"{output_dir}/fig2_age_redshift.png", dpi=300)
    plt.close()

def generate_black_hole_plot():
    print("Generating Figure 3: Black Hole Infall...")
    
    bh = BlackHole(mass_solar=10.0)
    # Simulate infall
    sim_data = bh.simulate_infall(start_distance_rs=5.0, steps=1000)
    
    tau = sim_data['tau']
    t = sim_data['t']
    r = sim_data['r']
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'blue'
    ax1.set_xlabel("Coordinate Time t (s) [Bob]")
    ax1.set_ylabel("Distance (Rs)", color=color)
    ax1.plot(t, r, color=color, linewidth=2, label="Trajectory")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.axhline(y=1.0, color='black', linestyle=':', label="Event Horizon")
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'red'
    ax2.set_ylabel("Proper Time tau (s) [Alice]", color=color)  # we already handled the x-label with ax1
    ax2.plot(t, tau, color=color, linestyle='--', linewidth=2, label="Proper Time")
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title("Black Hole Infall: The Solid State Transition")
    # Removed dark_background
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(f"{output_dir}/fig3_black_hole_infall.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_rotation_curve()
    generate_cosmology_plot()
    generate_black_hole_plot()
    print("Figures generated successfully.")
