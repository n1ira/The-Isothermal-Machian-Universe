import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import scipy.constants as const

# === Constants (Natural Units: eV approx) ===
# We work in dimensionless units where H0 = 1, Omega_m0 = 0.3 approx.
# Model Parameters
N_POWER = 3.0 # Inverse cubic potential
LAMBDA_SCALE = 1.0 
BETA = 1.0 # Conformal coupling strength

# Cosmology
OMEGA_M0 = 0.3
OMEGA_L0 = 0.7 # Effective Dark Energy (Scalar Potential)

def background_evolution(t, y):
    # y = [a, phi, phi_dot]
    a, phi, phi_dot = y
    
    rho_m = OMEGA_M0 / (a**3)
    
    # V(phi) normalization: V(phi=1) = OMEGA_L0
    V = OMEGA_L0 / (phi**N_POWER)
    dV_dphi = -N_POWER * V / phi
    
    rho_phi = 0.5 * phi_dot**2 + V
    
    H_sq = (rho_m + rho_phi) # 8piG/3 = 1 normalization
    H = np.sqrt(H_sq)
    
    a_dot = a * H
    
    # Source term in KG eq: S = - BETA * rho_m (Trace T = -rho)
    source = -BETA * rho_m
    
    phi_ddot = -3*H*phi_dot - dV_dphi + source
    
    return [a_dot, phi_dot, phi_ddot]

def run_linear_perturbation_solver():
    print("\n=== IMU Linear Perturbation Solver (Einstein Frame) ===")
    print("Goal: Calculate Matter Power Spectrum P(k) with Scalar Fifth Force")
    
    # 1. Solve Background
    a_start = 1e-3
    
    # Equilibrium: V' = source = - beta * rho
    # -n V / phi = - beta rho
    rho_start = OMEGA_M0 / (a_start**3)
    
    if abs(BETA) > 1e-10:
        phi_init = (N_POWER * OMEGA_L0 / (BETA * rho_start))**(1.0/(N_POWER+1))
    else:
        phi_init = 1.0
    
    print(f"Initial Phi (Equilibrium): {phi_init:.2e}")
    
    y0 = [a_start, phi_init, 0.0] # Assume tracking
    
    t_span = [0, 2.0] 
    
    def event_a_1(t, y): return y[0] - 1.0
    event_a_1.terminal = True
    
    print("Solving Background Evolution (Stiff)...")
    sol_bg = solve_ivp(background_evolution, t_span, y0, events=event_a_1, 
                       method='Radau', rtol=1e-6, atol=1e-10)
    
    if not sol_bg.success:
        print("Background integration failed.")
        return

    ts = sol_bg.t
    a_s = sol_bg.y[0]
    phi_s = sol_bg.y[1]
    H_s = np.gradient(a_s, ts) / a_s
    
    print(f"Background solved. Final a: {a_s[-1]:.4f}")

    # 2. Solve Perturbations for k=100 (Sub-horizon)
    k_mode = 100.0
    
    def pert_system(t, y_pert):
        # y_pert = [delta_m, theta_m, delta_phi, delta_phi_dot]
        delta_m, theta_m, dphi, dphi_dot = y_pert
        
        # Interpolate background
        a = np.interp(t, ts, a_s)
        phi = np.interp(t, ts, phi_s)
        H = np.interp(t, ts, H_s)
        
        # Potentials
        V = OMEGA_L0 / (phi**N_POWER)
        V_prime = -N_POWER * V / phi
        V_prime_prime = N_POWER * (N_POWER+1) * V / (phi**2)
        
        # Equations
        # 1. Continuity: delta_dot = - theta / a
        delta_m_dot = -theta_m / a
        
        # 2. Euler: theta_dot = - H theta + Gravity + Fifth Force
        # Gravity Term: 4 pi G rho a delta (ATTRACTIVE -> Makes theta negative -> delta positive)
        # 4 pi G rho = 1.5 * Omega_m0 / a^3 (in H0=1 units)
        # Gravity = (1.5 * Omega_m0 / a^2) * delta
        Gravity_Force = (1.5 * OMEGA_M0 / (a**2)) * delta_m
        
        # Fifth Force: F = - Beta grad dphi.
        # In k-space: F = - Beta (ik) dphi.
        # div F = - Beta (ik) (ik) dphi = + k^2 Beta dphi.
        # This term adds to theta_dot.
        # If dphi < 0 (Well), this term is Negative (Attractive).
        Fifth_Force = (k_mode**2 / a) * BETA * dphi
        
        # Total Euler
        # Note: Gravity_Force has + sign because I derived "Gravity = + ... delta" implies Attraction.
        # Wait. If delta > 0. Gravity_Force > 0.
        # theta_dot += Gravity_Force.
        # theta starts at -H delta < 0.
        # theta_dot > 0 means theta becomes LESS negative (closer to 0).
        # This means Decay!
        # Attraction means collapse -> theta becomes MORE negative.
        # So Gravity Term should be NEGATIVE?
        # Let's check standard eq:
        # delta'' + 2H delta' - 4 pi G rho delta = 0.
        # delta'' = ... + 4 pi G rho delta.
        # delta' = - theta / a.
        # delta'' = - theta' / a + H theta / a^2.
        # - theta' / a = ... + 4 pi G rho delta.
        # theta' = ... - a * 4 pi G rho delta.
        # So theta' should have NEGATIVE term for Gravity.
        
        # CORRECTION: Gravity Force should be NEGATIVE in theta equation.
        # - (1.5 * Omega / a^2) * delta.
        
        theta_m_dot = -H * theta_m - Gravity_Force + Fifth_Force
        
        # 3. Scalar Perturbation Eq
        rho_m = OMEGA_M0 / (a**3)
        # Source_pert = - Beta rho delta
        source_pert = -BETA * rho_m * delta_m
        
        k_phys_sq = (k_mode / a)**2
        
        dphi_ddot = -3*H*dphi_dot - (k_phys_sq + V_prime_prime) * dphi + source_pert
        
        return [delta_m_dot, theta_m_dot, dphi_dot, dphi_ddot]

    # Initial conditions
    # theta = - a H delta (Growing mode)
    y0_pert = [1e-5, -a_start * H_s[0] * 1e-5, 0.0, 0.0]
    
    print(f"Solving Perturbations for k={k_mode} (Stiff Solver)...")
    sol_pert = solve_ivp(pert_system, [ts[0], ts[-1]], y0_pert, t_eval=ts, method='Radau')
    
    if not sol_pert.success:
        print("Perturbation integration failed.")
        print(sol_pert.message)
    
    delta_m_res = sol_pert.y[0]
    
    print(f"Final Delta: {delta_m_res[-1]:.4e}")
    print(f"Final Scale Factor: {a_s[-1]:.4f}")
    
    growth_rate = delta_m_res / a_s
    final_enhancement = growth_rate[-1] / growth_rate[0]
    
    plt.figure(figsize=(10, 10))
    plt.subplot(2, 1, 1)
    plt.plot(a_s, delta_m_res, label='IMU Matter Density $\delta_m$')
    plt.plot(a_s, a_s * delta_m_res[0]/a_s[0], '--', label='Standard CDM')
    plt.legend()
    plt.grid(True)
    plt.subplot(2, 1, 2)
    plt.plot(a_s, growth_rate / growth_rate[0], label='Enhancement')
    plt.legend()
    plt.grid(True)
    plt.savefig('boltzmann_growth_result.png')
    
    print(f"\nResult:")
    print(f"Growth Enhancement Factor: {final_enhancement:.2f}")

if __name__ == "__main__":
    run_linear_perturbation_solver()