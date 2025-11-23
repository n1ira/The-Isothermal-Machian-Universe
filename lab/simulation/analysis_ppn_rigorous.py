import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from scipy.optimize import brentq

# === Constants in Natural Units (eV) ===
KG_TO_EV = 5.609e35
M_TO_INV_EV = 5.067e6

# Fundamental Constants
M_PL_REDUCED = 2.435e18 * 1e9 # eV
M_PL = M_PL_REDUCED 

# Solar Properties
M_SUN_KG = 1.989e30
R_SUN_M = 6.957e8
R_SUN_INV_EV = R_SUN_M * M_TO_INV_EV
RHO_SUN_KG_M3 = 1408.0 
RHO_SUN_EV4 = RHO_SUN_KG_M3 * KG_TO_EV / (M_TO_INV_EV**3)

RHO_GAL_KG_M3 = 1.0e-24 
RHO_GAL_EV4 = RHO_GAL_KG_M3 * KG_TO_EV / (M_TO_INV_EV**3)

PHI_N_SURFACE = (const.G * M_SUN_KG) / (R_SUN_M * const.c**2)

# === Model Parameters (Unified Symmetron + Machian) ===
# Symmetron Parameters from Verification Script
M_SYM = 2.44e15 * 1e9 # eV (M ~ M_pl/1000)
MU_SYM = 1.08e-24 * 1e9 # eV
LAMBDA_SYM = 1.0

# Machian Vacuum Driver Parameters
# V = C / phi^3
# Matches previous search: Lambda=11.7 keV => C = Lambda^7
N_POWER = 3.0
LAMBDA_VAC = 11.7e3 # eV
C_VAC = LAMBDA_VAC**(4+N_POWER)

BETA = 1.0 # Base coupling (approx 1 for Symmetron if phi ~ M)
# Actually Symmetron coupling depends on phi/M. beta_eff = phi/M.

def get_V_eff_prime(phi, rho):
    """
    dV_eff/dphi = dV_sym/dphi + dV_machian/dphi
    V_sym_eff = 0.5*(rho/M^2 - mu^2)*phi^2 + 0.25*lambda*phi^4
    V_machian = C / phi^n
    """
    # Symmetron part
    # d/dphi [ 0.5 * (rho/M^2 - mu^2) * phi^2 ] = (rho/M^2 - mu^2) * phi
    term_sym_quad = (rho / M_SYM**2 - MU_SYM**2) * phi
    term_sym_quart = LAMBDA_SYM * phi**3
    
    # Machian part
    # d/dphi [ C * phi^-n ] = -n * C * phi^-(n+1)
    term_machian = -N_POWER * C_VAC * (phi**(-N_POWER-1))
    
    return term_sym_quad + term_sym_quart + term_machian

def find_phi_min(rho):
    # Search for root of V' = 0
    # Range: small to large.
    # Guess: In high density, dominated by rho/M^2 * phi = n C / phi^(n+1) => phi^(n+2) = n C M^2 / rho
    phi_guess = ((N_POWER * C_VAC * M_SYM**2) / rho)**(1.0/(N_POWER+2.0))
    
    # Bracket the root
    try:
        root = brentq(get_V_eff_prime, phi_guess*0.01, phi_guess*100.0, args=(rho,))
        return root
    except ValueError:
        # Fallback if bracketing fails
        return phi_guess

def run_analysis():
    print("\n=== Unified PPN Analysis (Symmetron + Machian) ===")
    
    # 1. Calculate Fields
    phi_gal = find_phi_min(RHO_GAL_EV4)
    phi_sun = find_phi_min(RHO_SUN_EV4)
    
    print(f"\nField Values:")
    print(f"  Galactic: {phi_gal:.2e} eV")
    print(f"  Solar:    {phi_sun:.2e} eV")
    
    # 2. Calculate Thin Shell Parameter
    # Formula: epsilon = (phi_out - phi_in) / (6 * beta_eff * M_pl * Phi_N)
    # But beta_eff for Symmetron is phi_local / M_SYM ?? 
    # Or is it just standard coupling?
    # The prompt formula used a generic beta.
    # In Symmetron, A(phi) = 1 + phi^2/2M^2.
    # beta(phi) = M_pl * d(ln A)/dphi = M_pl * (phi/M^2) / A ~ (M_pl/M) * (phi/M).
    # This is small if phi is small!
    
    # Let's use the Expert's Formula assuming constant beta for now, 
    # OR calculate the effective beta at the surface.
    beta_eff_surface = (M_PL / M_SYM) * (phi_sun / M_SYM)
    print(f"  Effective Coupling beta(R_sun): {beta_eff_surface:.2e}")
    
    # If beta is very small, epsilon definition changes?
    # Let's use the derived formula:
    # gamma = 1 - 2 * beta_eff^2 * epsilon_thin / (1 + beta_eff^2)
    
    delta_phi = abs(phi_gal - phi_sun)
    
    # Use the local beta for the constraint
    beta_local = beta_eff_surface 
    
    # Epsilon
    # If beta is small, the force is naturally small even without thin shell?
    # Symmetron screening relies on beta -> 0 in dense regions.
    # So we might not even need thin shell suppression if beta is tiny.
    
    force_ratio_symmetron = 2 * beta_local**2 
    
    print(f"\nSymmetron Screening Check:")
    print(f"  In high density, beta_eff -> {beta_local:.2e}")
    print(f"  Force Ratio F_phi / F_N ~ 2 * beta^2 = {force_ratio_symmetron:.2e}")
    
    limit = 2.3e-5
    if force_ratio_symmetron < limit:
        print(f"\n[PASS] Symmetron Screening successful via small coupling.")
        print(f"  Deviation {force_ratio_symmetron:.2e} < {limit:.2e}")
    else:
        print(f"\n[FAIL] Symmetron Screening insufficient.")
        
    # Also check Thin Shell just in case
    epsilon = delta_phi / (6.0 * beta_local * M_PL * PHI_N_SURFACE)
    print(f"  (Thin Shell Epsilon would be: {epsilon:.2e})")

if __name__ == "__main__":
    run_analysis()
