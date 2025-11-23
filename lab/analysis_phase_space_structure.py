import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

# === Physics Parameters ===
OMEGA_BD = 1000.0 
RHO_M0 = 1.0
V0 = 10.0
C_THERM = 50.0
K_WALL = 50.0

def derivatives(t, y):
    phi, phi_dot = y
    if phi < 1e-4: phi = 1e-4
    
    dV_vac = -2 * V0 / (phi**3)
    dV_therm = 0.5 * C_THERM
    dV_em = K_WALL / phi
    V_prime = dV_vac + dV_therm + dV_em
    
    rho_m = RHO_M0 / np.sqrt(phi)
    S_matter = rho_m * (-0.5 / phi) 
    
    Total_Force = V_prime + S_matter
    
    geometric_term = (1.0 / (2.0 * phi)) * phi_dot**2
    force_term = - (phi / (2.0 * OMEGA_BD)) * Total_Force
    
    d_phi = phi_dot
    d_phi_dot = geometric_term + force_term
    
    return [d_phi, d_phi_dot]

def run_phase_space_scan():
    print("Scanning Phase Space for Attractor vs Conservative Structure...")
    
    # Define a range of initial conditions
    # Varying starting position phi_0 (assuming starting from rest)
    phi_starts = [0.3, 0.4, 0.5, 0.6, 0.7]
    
    trajectories = []
    
    t_span = (0, 200.0)
    
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(1, 1, 1)
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(phi_starts)))
    
    for i, phi_0 in enumerate(phi_starts):
        y0 = [phi_0, 0.0]
        print(f"Simulating IC: phi_0 = {phi_0}")
        
        sol = solve_ivp(derivatives, t_span, y0, method='LSODA', rtol=1e-9, atol=1e-11, max_step=0.05)
        
        # Plot
        ax.plot(sol.y[0], sol.y[1], color=colors[i], linewidth=1.5, label=f'$\phi_0={phi_0}$')
        
        # Store last cycle properties for analysis
        # (Not strictly necessary for visual proof but good for verification)
        
    ax.set_xlabel(r'$\phi$')
    ax.set_ylabel(r'$\dot{\phi}$')
    ax.set_title('Phase Space Structure: Conservative Families vs Attractor')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    output_dir = 'papers/figures'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'phase_space_families.png')
    plt.savefig(output_path, dpi=300)
    print(f"Phase space scan saved to {output_path}")

if __name__ == "__main__":
    run_phase_space_scan()
