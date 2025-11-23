import numpy as np
import matplotlib.pyplot as plt
from simulation.galaxy_rotation import BaryonicMassGradient
from simulation import cosmology
from simulation.black_hole import BlackHole
import os

# Ensure output directory exists
output_dir = "papers/figures"
os.makedirs(output_dir, exist_ok=True)

def generate_rotation_curve():
    print("Generating Figure 1: Galaxy Rotation Curve...")
    
    # Parameters (The "Kill Shot")
    m0 = 2.76e9 # Fitted M0 for NGC 6503
    scale_length = 0.89 # Fitted R
    beta = 0.98 # Fitted Beta
    coupling = 1.0e-6 # Tuning parameter
    
    # Define physics functions locally to ensure consistency with Experiment 1
    c_val = 299792.458 # km/s
    phi_0 = c_val**2
    
    def calculate_velocity(r_val):
        # phi = phi_0 * (1 + r/R)^beta
        # dphi/dr = phi_0 * beta * (1 + r/R)^(beta-1) / R
        # a = (c^2 / 2phi) * dphi/dr * coupling
        
        term1 = (1 + r_val / scale_length)
        phi = phi_0 * term1**beta
        dphi_dr = phi_0 * beta * term1**(beta - 1) / scale_length
        
        # Convert units: R is in kpc. c is in km/s.
        # We need acceleration in (km/s)^2 / kpc ?
        # v^2 = r * a
        # a has units of velocity^2 / length.
        # c^2 is velocity^2. phi is velocity^2.
        # dphi/dr is velocity^2 / length.
        # So a is velocity^2 / length. Correct.
        
        a_machian = (c_val**2 / (2 * phi)) * dphi_dr * coupling
        
        # Newtonian part (approximate point mass for visualization)
        # v_newt^2 = G * M / r
        # G in (km/s)^2 * kpc / M_sun
        G_const = 4.30091e-6 
        a_newt = G_const * m0 / r_val**2
        
        v_sq = r_val * (a_newt + a_machian)
        return np.sqrt(v_sq)

    r = np.linspace(0.1, 20, 100)
    v_machian = [calculate_velocity(ri) for ri in r]
    
    # Load Real Data
    data_path = "data/ngc6503.dat"
    r_obs, v_obs, v_err = None, None, None
    if os.path.exists(data_path):
        from simulation.galaxy_rotation import load_sparc_data
        r_obs, v_obs, v_err = load_sparc_data(data_path)
    
    plt.figure(figsize=(10, 6))
    plt.plot(r, v_machian, label=f'Machian Fit (Beta={beta:.2f})', color='cyan', linewidth=2)
    
    if r_obs is not None:
        plt.errorbar(r_obs, v_obs, yerr=v_err, fmt='o', color='white', label='NGC 6503 (SPARC)', markersize=4)
    
    plt.title(f"Galaxy Rotation Curve: Theory vs Observation")
    plt.xlabel("Radius (kpc)")
    plt.ylabel("Velocity (km/s)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.style.use('dark_background')
    
    plt.savefig(f"{output_dir}/fig1_rotation_curve.png", dpi=300)
    plt.close()

def generate_cosmology_plot():
    print("Generating Figure 2: Age vs Redshift...")
    
    z_range = np.linspace(0, 15, 100)
    machian_ages = [cosmology.lookback_time_machian(z) for z in z_range]
    lcdm_ages = [cosmology.lookback_time_lcdm(z) for z in z_range]
    
    plt.figure(figsize=(10, 6))
    plt.plot(z_range, machian_ages, label='Machian Universe (Static)', color='cyan', linewidth=2)
    plt.plot(z_range, lcdm_ages, label='Standard LCDM (Expanding)', color='red', linestyle='dashed')
    
    plt.title("Lookback Time vs Redshift")
    plt.xlabel("Redshift (z)")
    plt.ylabel("Lookback Time (Gyr)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.style.use('dark_background')
    
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
    
    color = 'cyan'
    ax1.set_xlabel("Coordinate Time t (s) [Bob]")
    ax1.set_ylabel("Distance (Rs)", color=color)
    ax1.plot(t, r, color=color, linewidth=2, label="Trajectory")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.axhline(y=1.0, color='white', linestyle=':', label="Event Horizon")
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'magenta'
    ax2.set_ylabel("Proper Time tau (s) [Alice]", color=color)  # we already handled the x-label with ax1
    ax2.plot(t, tau, color=color, linestyle='--', linewidth=2, label="Proper Time")
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title("Black Hole Infall: The Solid State Transition")
    plt.style.use('dark_background')
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(f"{output_dir}/fig3_black_hole_infall.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_rotation_curve()
    generate_cosmology_plot()
    generate_black_hole_plot()
    print("Figures generated successfully.")
