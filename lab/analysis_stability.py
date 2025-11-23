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
    # Prevent singularity
    if phi < 1e-4: phi = 1e-4
    
    # Potentials & Forces
    # V_vac ~ 1/phi^2  -> dV = -2*V0/phi^3
    dV_vac = -2 * V0 / (phi**3)
    
    # V_therm ~ phi    -> dV = 0.5*C
    dV_therm = 0.5 * C_THERM
    
    # V_em ~ ln(phi)   -> dV = K/phi
    dV_em = K_WALL / phi
    
    V_prime = dV_vac + dV_therm + dV_em
    
    # Matter Source
    # rho_m = rho_0 / sqrt(phi)
    # coupling = - d(rho)/dphi? No, coupling is d(mass)/dphi * density number.
    # Lagrangian interaction is -m(phi) * n.
    # m ~ phi^-0.5. dm/dphi = -0.5 * m / phi.
    # Force = - dm/dphi * n = 0.5 * rho_m / phi.
    rho_m = RHO_M0 / np.sqrt(phi)
    S_matter = rho_m * (-0.5 / phi) # This is actually on the RHS of the EOM
    
    # The Force Term combines Potential and Matter
    # Equation: (2w/phi) * phi_ddot = (w/phi^2)*phi_dot^2 - V' - S_matter
    # phi_ddot = (1/2phi)*phi_dot^2 - (phi/2w)*(V' + S_matter)
    
    # Note: The sign of S_matter depends on convention. 
    # If L = ... - V - m, then EOM has -V' - m'.
    # So both act as restoring forces if positive slopes.
    
    Total_Force = V_prime + S_matter # S_matter is negative (slope is negative)
    
    # Correct geometric coefficient for Brans-Dicke is 0.5, not 1.5
    geometric_term = (1.0 / (2.0 * phi)) * phi_dot**2
    
    force_term = - (phi / (2.0 * OMEGA_BD)) * Total_Force
    
    d_phi = phi_dot
    d_phi_dot = geometric_term + force_term
    
    return [d_phi, d_phi_dot]

def run_stability_analysis():
    print("Running Long-Term Stability Analysis...")
    
    # Initial Conditions
    y0 = [0.5, 0.0]
    
    # Run for many cycles
    t_max = 1000.0
    t_span = (0, t_max)
    
    # High precision integration to distinguish physical drift from numerical error
    sol = solve_ivp(derivatives, t_span, y0, method='LSODA', rtol=1e-10, atol=1e-12, max_step=0.05)
    
    t = sol.t
    phi = sol.y[0]
    phi_dot = sol.y[1]
    
    # --- Analysis ---
    
    # 1. Cycle Detection (Peaks)
    # Find indices where phi_dot crosses zero from positive to negative (Max phi)
    # or negative to positive (Min phi)
    
    # We'll just look at Maxima of phi
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(phi)
    
    if len(peaks) < 2:
        print("Not enough cycles detected to analyze stability.")
        return

    print(f"Detected {len(peaks)} cycles over T={t_max}")
    
    peak_vals = phi[peaks]
    peak_times = t[peaks]
    periods = np.diff(peak_times)
    
    mean_amp = np.mean(peak_vals)
    std_amp = np.std(peak_vals)
    drift_amp = (peak_vals[-1] - peak_vals[0]) / len(peaks)
    
    mean_period = np.mean(periods)
    std_period = np.std(periods)
    
    print(f"Mean Amplitude (phi_max): {mean_amp:.6f} +/- {std_amp:.6e}")
    print(f"Amplitude Drift per Cycle: {drift_amp:.6e}")
    print(f"Mean Period: {mean_period:.6f} +/- {std_period:.6e}")
    
    if std_amp < 1e-4:
        print("CONCLUSION: The system is STABLE (Limit Cycle / Conservative).")
    else:
        print("CONCLUSION: The system exhibits drift (possibly numerical or physical instability).")
        
    # --- Plotting ---
    output_dir = 'papers/figures'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plt.figure(figsize=(10, 8))
    
    # Phase Portrait
    plt.subplot(2, 2, (1, 3)) # Main plot
    # Color by time to show evolution
    plt.scatter(phi, phi_dot, c=t, cmap='plasma', s=1, alpha=0.5)
    plt.colorbar(label='Time (t)')
    plt.xlabel(r'$\phi$')
    plt.ylabel(r'$\dot{\phi}$')
    plt.title('Phase Space Stability Portrait (1000 Time Units)')
    plt.grid(True, alpha=0.3)
    
    # Inset: Zoom on the attractor/orbit
    # We plot the last few cycles in black over the first few in red
    # Actually, scatter handles this via color.
    
    # Amplitude Stability
    plt.subplot(2, 2, 2)
    plt.plot(np.arange(len(peak_vals)), peak_vals, 'b.-')
    plt.xlabel('Cycle Number')
    plt.ylabel(r'Max $\phi$')
    plt.title('Amplitude Stability')
    plt.grid(True, alpha=0.3)
    
    # Period Stability
    plt.subplot(2, 2, 4)
    plt.plot(np.arange(len(periods)), periods, 'r.-')
    plt.xlabel('Cycle Number')
    plt.ylabel('Period')
    plt.title('Period Stability')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'stability_analysis.png')
    plt.savefig(output_path, dpi=300)
    print(f"Stability Portrait saved to {output_path}")

if __name__ == "__main__":
    run_stability_analysis()
