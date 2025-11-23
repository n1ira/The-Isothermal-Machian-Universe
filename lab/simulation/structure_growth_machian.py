import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def calculate_growth():
    # Parameters
    # Planck 2018
    Omega_m0 = 0.315
    Omega_L0 = 0.685
    h = 0.674
    sigma8_0 = 0.811
    
    # IMU Parameters (Dilaton)
    # beta = 1/sqrt(6) -> 2*beta^2 = 1/3
    # G_eff = G * (1 + 2*beta^2) = 1.333 * G
    # But wait, this enhancement applies to Baryons.
    # Does the Scalar Fluid (Dark Matter) feel enhanced gravity?
    # If it's the source, it self-interacts.
    # We assume for the "Hardening" argument that the enhancement is universal (mimetic fluid follows tilde metric).
    mu = 1.0 / 3.0 
    
    z_range = np.linspace(2.5, 0, 50)
    a_range = 1.0 / (1.0 + z_range)
    
    # Differential Equation for Growth Factor D(a)
    # D'' + (2 - 1.5*Om(a))/a * D' - 1.5*Om(a)*(1+mu)/a^2 * D = 0
    # Let y = [D, D']
    
    def Omega_m(a):
        return Omega_m0 / (Omega_m0 + Omega_L0 * a**3)
        
    def system(y, a):
        D, D_prime = y
        Om = Omega_m(a)
        
        term1 = -(2 - 1.5 * Om) / a * D_prime
        
        # Standard GR: mu = 0
        # IMU: mu = 1/3
        term2 = 1.5 * Om * (1 + mu) / a**2 * D
        
        return [D_prime, term1 + term2]
        
    def system_gr(y, a):
        D, D_prime = y
        Om = Omega_m(a)
        term1 = -(2 - 1.5 * Om) / a * D_prime
        term2 = 1.5 * Om * (1.0) / a**2 * D # mu=0
        return [D_prime, term1 + term2]

    # Initial Conditions (High z, Matter Dominated)
    # D ~ a
    a_start = 1e-3
    y0 = [a_start, 1.0]
    
    # Integrate
    a_full = np.linspace(a_start, 1.0, 1000)
    
    sol_imu = odeint(system, y0, a_full)
    sol_gr = odeint(system_gr, y0, a_full)
    
    D_imu = sol_imu[:, 0]
    D_gr = sol_gr[:, 0]
    
    # Normalize to current epoch (z=0, a=1) ?
    # No, we normalize at high z (CMB) where physics is linear and identical.
    # We want to see the deviation at z=0.
    
    # Calculate f = d ln D / d ln a = a * D' / D
    D_prime_imu = sol_imu[:, 1]
    f_imu = a_full * D_prime_imu / D_imu
    
    D_prime_gr = sol_gr[:, 1]
    f_gr = a_full * D_prime_gr / D_gr
    
    # Calculate f*sigma8
    # We need to normalize sigma8. 
    # Usually sigma8 is defined at z=0.
    # Let's assume sigma8(z=0) matches Planck for GR.
    norm_gr = sigma8_0 / D_gr[-1]
    sigma8_z_gr = D_gr * norm_gr
    fs8_gr = f_gr * sigma8_z_gr
    
    # For IMU, if we start from same CMB amplitude, how does it end up?
    # Normalize IMU to match GR at start
    norm_imu = (D_gr[0] / D_imu[0]) * norm_gr
    sigma8_z_imu = D_imu * norm_imu
    fs8_imu = f_imu * sigma8_z_imu
    
    # Get values for plotting range
    z_plot = 1/a_full - 1
    mask = (z_plot >= 0) & (z_plot <= 2.0)
    
    print(f"Growth Rate at z=0 (GR): {f_gr[-1]:.3f}")
    print(f"Growth Rate at z=0 (IMU): {f_imu[-1]:.3f}")
    print(f"Sigma8 at z=0 (IMU): {sigma8_z_imu[-1]:.3f} (Enhanced by factor {sigma8_z_imu[-1]/sigma8_0:.2f})")
    
    plt.figure(figsize=(10, 6))
    plt.plot(z_plot[mask], fs8_gr[mask], 'k--', label='LambdaCDM (GR)')
    plt.plot(z_plot[mask], fs8_imu[mask], 'r-', label='Machian (Enhanced Gravity)')
    
    # Data points (RSD measurements - approximate)
    # z = 0.06, fs8 = 0.45 +/- 0.1
    # z = 0.57, fs8 = 0.45 +/- 0.05
    plt.errorbar([0.06, 0.57], [0.45, 0.45], yerr=[0.1, 0.05], fmt='o', color='blue', label='RSD Data (Approx)')
    
    plt.xlabel('Redshift z')
    plt.ylabel('f * sigma8 (Growth Rate)')
    plt.title('Structure Formation: The Enhanced Growth Problem')
    plt.legend()
    plt.gca().invert_xaxis()
    plt.grid(True, alpha=0.2)
    
    plt.savefig('lab/theory/structure_growth.png')
    print("Plot saved to lab/theory/structure_growth.png")

if __name__ == "__main__":
    calculate_growth()
