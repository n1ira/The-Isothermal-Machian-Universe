import sympy
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from sympy import symbols, Function, diff, sqrt, Matrix, simplify, solve, Eq, Rational

# --- SYMBOLIC DERIVATIONS ---

def derive_cosmology_symbolic():
    print("\n--- 1. SYMBOLIC DERIVATION: COSMOLOGY (FLRW) ---")
    
    t = symbols('t')
    a = Function('a')(t)      
    phi = Function('phi')(t)  
    H = diff(a, t) / a        
    
    adot = diff(a, t)
    phidot = diff(phi, t)
    V = Function('V')(phi)
    
    # Effective Lagrangian for Minisuperspace (a, phi)
    # L = -3 a * adot^2 + a^3 * (0.5 * phidot^2 - V)
    L_eff = -3 * a * adot**2 + a**3 * (Rational(1,2) * phidot**2 - V)
    
    dL_dadot = diff(L_eff, adot)
    dL_dphidot = diff(L_eff, phidot)
    
    # Hamiltonian Constraint (Friedmann Eq 1)
    Energy = dL_dadot * adot + dL_dphidot * phidot - L_eff
    print(f"\nHamiltonian Constraint (Friedmann Eq 1):")
    print(simplify(Energy))
    print("Result: H^2 = 8piG/3 * (0.5 phidot^2 + V)")

def derive_refractive_index_symbolic():
    print("\n--- 2. SYMBOLIC DERIVATION: LENSING (Refractive Index) ---")
    
    lambda_gamma = symbols('lambda_gamma')
    phi_prime = symbols('phi_prime') # dphi/dr
    M_pl = symbols('M_pl')
    
    # Interaction: L_int = (lambda / 4 M_pl^2) * (dphi)^2 * F^2
    # This modifies the permittivity/permeability.
    # Effective metric for photons: g_eff_uv = g_uv + (lambda / M_pl^2) d_u phi d_v phi
    
    term = 1 + (lambda_gamma / M_pl**2) * phi_prime**2
    n_derived = sqrt(term)
    
    print(f"\nDerived Refractive Index n(r):")
    print(n_derived)
    print(f"Taylor Expansion (small phi'): {n_derived.series(phi_prime, 0, 3)}")

# --- NUMERICAL SOLUTIONS ---

def solve_cosmology_numerical():
    print("\n--- 3. NUMERICAL SOLUTION: COSMOLOGY ---")
    # Solve Friedmann + Klein-Gordon for V(phi) = V0 * phi^-2
    # We want to check if phi(t) ~ t and H(t) ~ 1/t
    
    def system(t, y):
        # y = [a, phi, phidot]
        # H = adot/a
        # Friedmann: H^2 = (rho_m + 0.5 phidot^2 + V) / 3  (8piG=1)
        # KG: phidotdot + 3H phidot + V' = - d(rho_m)/dphi (coupling)
        # Matter: rho_m = rho_m0 / a^3 * m(phi)/m0
        
        a, phi, phidot = y
        
        # Parameters
        V0 = 1.0
        rho_m0 = 0.0 # Vacuum domination for simplicity first
        
        # Potential V = V0 / phi^2
        V = V0 / (phi**2)
        dV_dphi = -2 * V0 / (phi**3)
        
        # Friedmann Constraint for H
        rho_phi = 0.5 * phidot**2 + V
        H = np.sqrt(rho_phi / 3.0)
        
        # KG Equation
        # phidotdot = -3 H phidot - dV_dphi
        phidotdot = -3 * H * phidot - dV_dphi
        
        adot = H * a
        
        return [adot, phidot, phidotdot]
    
    t_span = (0.1, 10.0)
    y0 = [1.0, 1.0, 1.0] # Initial a=1, phi=1, phidot=1
    
    sol = solve_ivp(system, t_span, y0, rtol=1e-6)
    
    t = sol.t
    phi = sol.y[1]
    
    # Check scaling
    # We expect phi ~ t
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(t, phi, label='phi(t)')
    plt.plot(t, t, '--', label='Linear t')
    plt.title("Scalar Field Evolution")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.loglog(t, phi, label='phi(t)')
    plt.title("Log-Log Scaling")
    plt.grid(True)
    
    plt.savefig('papers/figures/cosmology_solution.png')
    print("Saved cosmology_solution.png. Visual check: Does phi scale linearly?")

def solve_galaxy_numerical():
    print("\n--- 4. NUMERICAL SOLUTION: GALAXY ---")
    # Solve static spherical scalar field with source
    # Laplacian phi = V'(phi) + alpha * rho_matter
    # Radial: phi'' + 2/r phi' = dV/dphi + alpha * rho(r)
    
    # We assume V(phi) = m_eff^2 * phi^2 / 2 (Massive scalar / Chameleon)
    # Or V(phi) = V0 / phi^n
    
    # Let's try to RECOVER the exponential profile from a source.
    # If rho(r) is NFW or exponential disk, what is phi(r)?
    
    def system(r, y):
        # y = [phi, phi_prime]
        phi, phi_prime = y
        
        # Parameters
        alpha = 1.0
        m_scalar = 0.1 # Inverse range
        
        # Source: Point mass at origin? Or distributed?
        # Let's use an exponential disk density approximation
        rho = np.exp(-r) 
        
        # Equation: phi'' = -2/r phi' + m^2 phi + alpha * rho
        if r < 1e-3:
            term1 = 0 # Regularity at origin
        else:
            term1 = -2/r * phi_prime
            
        phi_double_prime = term1 + m_scalar**2 * phi + alpha * rho
        
        return [phi_prime, phi_double_prime]
    
    r_span = (0.01, 20.0)
    y0 = [1.0, 0.0] # phi(0)=1, phi'(0)=0
    
    sol = solve_ivp(system, r_span, y0, rtol=1e-6)
    
    r = sol.t
    phi = sol.y[0]
    
    # Calculate "Inertial Mass" m(r) = m0 * phi(r) (if coupling is linear)
    # We want m(r) ~ exp(-r/R)
    
    plt.figure()
    plt.plot(r, phi, label='phi(r)')
    plt.plot(r, np.exp(-r * 0.1), '--', label='Target exp(-r)')
    plt.title("Galactic Scalar Profile")
    plt.legend()
    plt.savefig('papers/figures/galaxy_solution.png')
    print("Saved galaxy_solution.png.")

if __name__ == "__main__":
    derive_cosmology_symbolic()
    derive_refractive_index_symbolic()
    solve_cosmology_numerical()
    solve_galaxy_numerical()
