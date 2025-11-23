import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

# Constants
OMEGA_BD = 1000.0 
RHO_M0 = 1.0
V0 = 10.0
C_THERM = 50.0
K_WALL = 50.0

def derivatives(t, y):
    phi, phi_dot = y
    if phi < 1e-3: phi = 1e-3
    
    # Potentials: V_vac ~ 1/phi^2, V_therm ~ phi, V_em ~ ln(phi)
    dV_vac = -2 * V0 / (phi**3)
    dV_therm = 0.5 * C_THERM
    dV_em = K_WALL / phi
    V_prime = dV_vac + dV_therm + dV_em
    
    # Matter Source: rho_m ~ phi^-0.5 => S_m ~ -phi^-1.5
    rho_m = RHO_M0 / np.sqrt(phi)
    S_matter = rho_m * (-0.5 / phi)
    
    Total_Force = V_prime + S_matter
    
    geometric_term = (3.0 / (2.0 * phi)) * phi_dot**2
    force_term = - (phi / (2.0 * OMEGA_BD)) * Total_Force
    
    return [phi_dot, geometric_term + force_term]

def generate_paper_figure():
    y0 = [0.5, 0.0]
    t_span = (0, 80.0)
    sol = solve_ivp(derivatives, t_span, y0, method='LSODA', rtol=1e-9, atol=1e-10, max_step=0.05)
    
    t = sol.t
    phi = sol.y[0]
    phi_dot = sol.y[1]
    
    # Create Figure
    plt.figure(figsize=(8, 6))
    
    # Top Panel: Field Evolution
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(t, phi, color='#00FFFF', linewidth=2, label=r'$\phi(t)$ (Scalar Field)')
    ax1.set_ylabel(r'Scalar Field $\phi$', color='white')
    ax1.set_facecolor('black')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.grid(True, color='#333333')
    ax1.set_title('The Machian Heartbeat: Cyclic Scalar Evolution', color='white')
    
    # Bottom Panel: Phase Space
    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(phi, phi_dot, color='#FF00FF', linewidth=1.5)
    ax2.set_xlabel(r'Field Value $\phi$', color='white')
    ax2.set_ylabel(r'Velocity $\dot{\phi}$', color='white')
    ax2.set_facecolor('black')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    ax2.grid(True, color='#333333')
    ax2.set_title('Phase Space Limit Cycle', color='white')
    
    # Styling for the dark theme paper
    plt.tight_layout()
    
    # Save
    output_dir = 'papers/figures'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, 'bounce_cycles.png')
    plt.savefig(output_path, facecolor='black', dpi=300)
    print(f"Figure saved to {output_path}")

if __name__ == "__main__":
    generate_paper_figure()
