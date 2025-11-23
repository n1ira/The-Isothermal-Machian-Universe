import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

# === Physics Constants (Normalized for Simulation) ===
# We work in units where 8*pi*G/3 = 1 for simplicity, or keep real units?
# Let's use H0-normalized units.
# Time in units of 1/H0.
# Densities in units of critical density rho_c.

# Parameters
OMEGA_M0 = 0.3
OMEGA_R0 = 8e-5  # Radiation density today
OMEGA_L0 = 0.0   # No cosmological constant in Machian frame (replaced by V)
H0 = 1.0         # Time unit

# Machian Parameters (Tunable)
# Potential V = V0 * phi^-alpha
V0 = 1.5         # Amplitude to match Dark Energy roughly (gives acceleration)
ALPHA = 2.0      # Inverse square potential standard

# Thermal Wall Parameters
C_THERM = 500.0 # Strength of thermal coupling
# In Machian Frame, T scales with Mass m(t) ~ 1/sqrt(phi).
# This creates the feedback loop: phi decreases -> m increases -> T increases -> Wall rises.

# Future Wall Parameters (The "Machian/EM" Wall)
# V_em = Lambda_gamma * rho_rad * ln(phi)
LAMBDA_GAMMA = 0.1 
K_WALL = 5.0 # Increased strength to ensure reflection

def run_bounce_experiment():
    print("Initializing Isothermal Machian Universe Bounce Experiment...")
    
    # Initial Conditions
    # Start with phi small (high mass, high T) but rolling out
    a_init = 1e-4 # Just for scale tracking, not dynamics if we decouple
    
    # Phi init:
    # If Temp ~ 1/sqrt(phi), then V_therm ~ phi.
    # V_vac ~ 1/phi^2.
    # Minimum at -2/phi^3 + C = 0 => phi ~ (2/C)^(1/3)
    phi_init = 0.1
    phi_dot_init = 0.05 # Give it a little push
    
    y0 = [np.log(a_init), phi_init, phi_dot_init] 
    
    t_span = (0, 40.0) # Long run
    
    print(f"Initial State: phi={phi_init:.2e}, K_WALL={K_WALL}")
    
    sol = solve_ivp(derivatives, t_span, y0, method='LSODA', rtol=1e-6, atol=1e-8, max_step=0.05)
    
    # Process Results
    ln_a = sol.y[0]
    a = np.exp(ln_a)
    phi = sol.y[1]
    phi_dot = sol.y[2]
    t = sol.t
    
    # Check for Bounce (phi turning around)
    # We expect phi to grow (roll down 1/phi^2), hit wall, and decrease.
    phi_max_idx = np.argmax(phi)
    has_bounced = phi_max_idx < len(phi) - 1
    
    print(f"Simulation Complete. Steps: {len(t)}")
    if has_bounced:
        print(f"BOUNCE DETECTED at t={t[phi_max_idx]:.2f}, phi_max={phi[phi_max_idx]:.2f}")
        print("The scalar field hit the 'Future Wall' and reversed!")
        
        # Check if it returns to start (Cycle)
        if phi[-1] < phi[phi_max_idx]:
            print(f"Field is contracting. Final phi={phi[-1]:.2f}")
    else:
        print("No bounce detected. Field maxed at phi=", np.max(phi))
        
    # Save Data
    output_file = 'bounce_data.npz'
    np.savez(output_file, t=t, a=a, phi=phi, phi_dot=phi_dot)
    
    # Simple Plot
    generate_plot(t, a, phi, phi_dot, has_bounced)

def derivatives(t, y):
    ln_a, phi, phi_dot = y
    a = np.exp(ln_a)
    
    # Machian Temperature Coupling
    # T ~ m ~ 1/sqrt(phi)
    # We normalize so T=1 at phi=1 for simplicity
    Temp = 1.0 / np.sqrt(phi)
    
    # Potentials & Derivatives
    # 1. Vacuum: V = V0 / phi^2 (Driver)
    V_vac = V0 / (phi**2)
    dV_vac = -2 * V0 / (phi**3)
    
    # 2. Thermal: V = 0.5 * C * T^2 * phi^2
    # With T ~ 1/sqrt(phi), T^2 ~ 1/phi
    # V_therm ~ (1/phi) * phi^2 = phi
    # This is a linear confining potential!
    V_therm = 0.5 * C_THERM * phi 
    dV_therm = 0.5 * C_THERM 
    
    # 3. Future Wall (EM Log Coupling)
    V_em = K_WALL * np.log(phi)
    dV_em = K_WALL / phi
    
    # Total V and dV
    V_tot = V_vac + V_therm + V_em
    dV_tot = dV_vac + dV_therm + dV_em
    
    # Hubble Parameter (Friedmann)
    # For purely scalar dynamics in static frame
    rho_phi = 0.5 * phi_dot**2 + V_tot
    H = np.sqrt(np.abs(rho_phi)) 
    
    # Equations of Motion
    d_ln_a = H
    d_phi = phi_dot
    d_phi_dot = -3 * H * phi_dot - dV_tot
    
    return [d_ln_a, d_phi, d_phi_dot]

def generate_plot(t, a, phi, phi_dot, bounce):
    plt.figure(figsize=(10, 12))
    
    # Subplot 1: Scalar Field Evolution
    plt.subplot(3, 1, 1)
    plt.plot(t, phi, 'c-', label='Scalar Field phi', linewidth=2)
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.title('Experiment Bounce: Scalar Field Dynamics')
    plt.ylabel('Scalar Field phi')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Subplot 2: Potentials
    plt.subplot(3, 1, 2)
    # Reconstruct potentials for plotting
    V_vac = V0 / (phi**2)
    Temp = 1.0 / a
    V_therm = 0.5 * C_THERM * (Temp**2) * phi**2
    V_em = K_WALL * np.log(phi)
    plt.plot(t, V_vac, 'g--', label='Machian Driver (1/phi^2)')
    plt.plot(t, V_therm, 'r--', label='Thermal Wall (T^2 phi^2)')
    plt.plot(t, V_em, 'm--', label='Future Wall (ln phi)')
    plt.plot(t, V_vac + V_therm + V_em, 'k-', label='Total Potential')
    plt.yscale('log')
    plt.ylim(1e-2, 1e3)
    plt.ylabel('Potential Energy')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Subplot 3: Phase Space
    plt.subplot(3, 1, 3)
    plt.plot(phi, phi_dot, 'b-', linewidth=1.5)
    if bounce:
        plt.plot(phi[-1], phi_dot[-1], 'ro', label='End State')
    plt.xlabel('phi')
    plt.ylabel('phi_dot')
    plt.title('Phase Space Trajectory')
    plt.grid(True, alpha=0.3)
    
    filename = 'experiment_bounce_result.png'
    plt.savefig(filename)
    print(f"Plot saved to {filename}")

if __name__ == "__main__":
    run_bounce_experiment()
