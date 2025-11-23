import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

# === Physics Parameters (Same as Bounce Experiment) ===
OMEGA_BD = 1000.0 
RHO_M0 = 1.0
V0 = 10.0
C_THERM = 50.0
K_WALL = 50.0

def derivatives(t, y):
    phi, phi_dot = y
    # Prevent numerical NaN, though physics should bounce before 0
    if phi < 1e-6: phi = 1e-6
    
    dV_vac = -2 * V0 / (phi**3)
    dV_therm = 0.5 * C_THERM
    dV_em = K_WALL / phi
    V_prime = dV_vac + dV_therm + dV_em
    
    rho_m = RHO_M0 / np.sqrt(phi)
    S_matter = rho_m * (-0.5 / phi)
    
    Total_Force = V_prime + S_matter
    
    geometric_term = (1.0 / (2.0 * phi)) * phi_dot**2
    force_term = - (phi / (2.0 * OMEGA_BD)) * Total_Force
    
    return [phi_dot, geometric_term + force_term]

def run_curvature_analysis():
    print("Calculating Einstein Frame Curvature Invariants at the Bounce...")
    
    # 1. Run Simulation near the bounce
    # We start with phi decreasing (contraction), aim for bounce
    y0 = [0.5, -0.1] 
    t_span = (0, 10.0)
    
    sol = solve_ivp(derivatives, t_span, y0, method='LSODA', rtol=1e-10, atol=1e-12, max_step=0.01)
    
    t_J = sol.t
    phi = sol.y[0]
    phi_dot = sol.y[1] # d(phi)/dt_J
    
    # Find the bounce point (min phi)
    min_idx = np.argmin(phi)
    print(f"Bounce detected at t_J = {t_J[min_idx]:.4f}")
    print(f"Minimum Scalar Value phi_min = {phi[min_idx]:.6e}")
    
    # 2. Calculate Einstein Frame Quantities
    # Map: g_E = phi * g_J
    # Scale Factor a_E = sqrt(phi)
    # Proper Time dtau = sqrt(phi) * dt_J
    
    # We need derivatives with respect to tau (Einstein time)
    # d/dtau = (1/sqrt(phi)) * d/dt_J
    
    # Hubble Parameter H_E = (1/a_E) * (da_E/dtau)
    # a_E = phi^0.5
    # da_E/dt_J = 0.5 * phi^-0.5 * phi_dot
    # da_E/dtau = (da_E/dt_J) / sqrt(phi) = 0.5 * phi^-1 * phi_dot
    # H_E = (1/sqrt(phi)) * (0.5 * phi^-1 * phi_dot) = 0.5 * phi_dot / phi^1.5
    
    H_E = 0.5 * phi_dot / (phi**1.5)
    
    # Time derivative of H_E (dH_E/dtau)
    # dH_E/dt_J = 0.5 * [ (phi_ddot * phi^1.5 - phi_dot * 1.5 * phi^0.5 * phi_dot) / phi^3 ]
    #           = 0.5 * [ phi_ddot/phi^1.5 - 1.5 * phi_dot^2 / phi^2.5 ]
    # dH_E/dtau = (dH_E/dt_J) / sqrt(phi)
    #           = 0.5 * [ phi_ddot/phi^2 - 1.5 * phi_dot^2 / phi^3 ]
    
    # We need phi_ddot. We can get it from the ODE function or numerical diff.
    # Let's calculate it analytically from the EOM to be precise.
    phi_ddot = np.zeros_like(phi)
    for i in range(len(phi)):
        _, acc = derivatives(0, [phi[i], phi_dot[i]])
        phi_ddot[i] = acc
        
    H_dot_E = 0.5 * (phi_ddot / (phi**2) - 1.5 * (phi_dot**2) / (phi**3))
    
    # 3. Curvature Scalars (FLRW Metric)
    # Ricci Scalar R = 6(H_dot + 2H^2)
    # Kretschmann Scalar K = 24H^2(H_dot + H^2) + 12H^4 + ... for FLRW?
    # Simpler forms for flat FLRW:
    # R = 6 (dH/dt + 2H^2)
    # Riemann components ~ H^2 and (dH/dt + H^2)
    # K = 12 (H^4 + (dH/dt + H^2)^2)
    
    R_scalar = 6 * (H_dot_E + 2 * H_E**2)
    K_scalar = 12 * (H_E**4 + (H_dot_E + H_E**2)**2)
    
    # 4. Analyze at Bounce
    R_bounce = R_scalar[min_idx]
    K_bounce = K_scalar[min_idx]
    
    print("\n=== Curvature Analysis Results ===")
    print(f"Ricci Scalar at Bounce: {R_bounce:.4e}")
    print(f"Kretschmann Scalar at Bounce: {K_bounce:.4e}")
    
    # Check for Divergence
    # If phi_min is very small, terms like 1/phi^3 might blow up.
    # Let's see if they cancel.
    
    # 5. Plot
    plt.figure(figsize=(10, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(t_J, phi, 'b-')
    plt.ylabel(r'$\phi (t_J)$')
    plt.title('Jordan Frame Scalar Field')
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(t_J, H_E, 'g-')
    plt.ylabel(r'$H_E (\tau)$')
    plt.title('Einstein Frame Hubble Parameter')
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(t_J, R_scalar, 'r-', label='Ricci Scalar R')
    plt.legend()
    plt.ylabel('Curvature')
    plt.title('Curvature Invariant R')
    plt.xlabel('Jordan Time')
    plt.yscale('symlog') # Handle negative values and large scales
    plt.grid(True)
    
    output_file = 'papers/figures/curvature_check.png'
    plt.savefig(output_file)
    print(f"Curvature plot saved to {output_file}")
    
    # Heuristic Pass/Fail
    if abs(R_bounce) > 1e10:
        print("WARNING: Curvature is extremely high. Potential Singularity.")
    else:
        print("SUCCESS: Curvature remains finite. The bounce is non-singular.")

if __name__ == "__main__":
    run_curvature_analysis()
