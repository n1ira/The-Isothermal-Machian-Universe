import numpy as np
from scipy.integrate import solve_ivp, solve_bvp
import matplotlib.pyplot as plt

# === Constants ===
G = 6.674e-11
c = 2.998e8
M_sun = 1.989e30
R_sun = 6.957e8
AU = 1.496e11

# === Theory Parameters (From Paper 1 & 5) ===
# The potential is V(phi) = V0 * phi^-2
# Coupling beta ~ 1 (Order unity)
BETA = 1.0 
M_PL = 2.176e-8 # Planck Mass (kg) - reduced?
# In standard Chameleon literature, M_pl is reduced Planck mass ~ 2.4e18 GeV
# Let's work in dimensionless units where possible or consistent SI.
# The equation is: Laplacian(phi) = dV/dphi + (beta/M_pl) * rho

# We need the scale V0.
# In the galaxy, the Compton wavelength was R_gal ~ 1 kpc ~ 3e19 m.
# m_eff^2 = V''(phi_vac) ~ 1/R_gal^2
# V ~ phi^-2  => V'' ~ phi^-4.
# So 1/R^2 ~ V0 * phi^-4.

# Let's assume the background phi_cosmo ~ 0.1 M_pl (typical for quintessence).
# This sets V0.

# === Simulation Setup ===
# We solve the radial equation:
# phi'' + (2/r)phi' = dV_eff/dphi
# V_eff = V(phi) + (beta/M_pl) * rho(r) * phi

# Density Profile of Sun (Simplified)
rho_core = 1.5e5 # kg/m^3 (Center of Sun)
rho_vac = 1.0e-24 # Interstellar medium

def density(r):
    if r < R_sun:
        return rho_core # constant density star for stability
    else:
        return rho_vac

def run_chameleon_test():
    print("Running Chameleon Consistency Test...")
    
    # 1. Define Potentials based on Galaxy Fit
    # We need the mass in the vacuum to be m_vac = 1/R_gal = 1/(1 kpc)
    R_gal = 3.086e19 # m (1 kpc)
    m_vac = 1.0 / R_gal
    
    # Assume phi_vac = M_PL (just to set a scale).
    phi_vac = M_PL
    
    # V'' = m^2
    # V(phi) = Lambda^4+n / phi^n. Let n=2.
    # V'(phi) = -2 * V / phi
    # V''(phi) = 6 * V / phi^2 = m_vac^2
    # So V_vac = (1/6) * m_vac^2 * phi_vac^2
    
    V_scale = (1.0/6.0) * (m_vac**2) * (phi_vac**2)
    
    print(f"Vacuum Scale m_vac: {m_vac:.2e} 1/m (Range: {1/m_vac/3.086e16:.1f} pc)")
    
    # 2. Solve for Phi inside the Sun
    # Inside the Sun, rho is HUGE.
    # The effective minimum shifts.
    # V_eff' = V' + (beta/M_pl)*rho = 0
    # -2 * V_scale / phi^3 * (phi_vac^2 / phi^2 ?) -> Wait, V = K / phi^2
    # Let's stick to V = V_scale * (phi_vac/phi)^2
    # V' = -2 * V_scale * phi_vac^2 / phi^3
    # V'' = 6 * V_scale * phi_vac^2 / phi^4
    
    # Equilibrium condition inside Sun:
    # 2 * V_scale * phi_vac^2 / phi_in^3 = (BETA/M_PL) * rho_core
    # phi_in^3 = (2 * V_scale * phi_vac^2 * M_PL) / (BETA * rho_core)
    
    term1 = 2 * V_scale * (phi_vac**2) * M_PL
    term2 = BETA * rho_core
    phi_in = (term1 / term2)**(1.0/3.0)
    
    print(f"Scalar Field in Vacuum: {phi_vac:.2e}")
    print(f"Scalar Field in Sun:    {phi_in:.2e}")
    
    if phi_in > phi_vac:
        print("ERROR: Field grew inside matter? Physics check failed.")
        return

    # 3. Calculate Effective Mass in Sun
    # m_in^2 = V_eff''(phi_in)
    #        = 6 * V_scale * phi_vac^2 / phi_in^4
    m_in_sq = 6 * V_scale * (phi_vac**2) / (phi_in**4)
    m_in = np.sqrt(m_in_sq)
    lambda_in = 1.0 / m_in
    
    print(f"Force Range in Vacuum: {1.0/m_vac:.2e} m")
    print(f"Force Range in Sun:    {lambda_in:.2e} m")
    
    # 4. Thin Shell Condition
    # For the sun to be screened, the shell parameter epsilon must be small.
    # epsilon ~ (phi_vac - phi_in) / (6 * beta * M_pl * Phi_Newton)
    
    delta_phi = phi_vac - phi_in # Effectively phi_vac since phi_in is tiny
    Phi_N = G * M_sun / (c**2 * R_sun) # Dimensionless potential ~ 2e-6
    # Note: standard def of Thin Shell usually uses Phi_N without c^2 if units match.
    # Phi_Newton = G M / R (units of v^2).
    # In the dimensionless formula: (phi)/M_pl / Phi_Newton_dimensionless
    
    epsilon = delta_phi / (6 * BETA * M_PL * Phi_N)
    
    print(f"\n=== The Verdict ===")
    print(f"Newtonian Potential Phi_N: {Phi_N:.2e}")
    print(f"Field Step Delta_phi/M_pl: {delta_phi/M_PL:.2e}")
    print(f"Thin Shell Parameter: {epsilon:.2e}")
    
    if epsilon < 1.0:
        print("SUCCESS: The Sun has a Thin Shell. The Fifth Force is screened.")
        if epsilon < 1e-5:
            print("STRONG SUCCESS: Matches Cassini bounds.")
        else:
            print("MARGINAL: Screened, but might still violate precision tests.")
    else:
        print("FAILURE: The Sun is NOT screened. The Fifth Force permeates the Solar System.")
        print("IMPLICATION: Planets should feel ~30% extra gravity. Theory Falsified.")

if __name__ == "__main__":
    run_chameleon_test()
