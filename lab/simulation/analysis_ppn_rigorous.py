import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const

# === Constants in Natural Units (eV) ===
# 1 kg = 5.609e35 eV
# 1 m = 5.067e6 eV^-1
# 1 s = 1.519e15 eV^-1
KG_TO_EV = 5.609e35
M_TO_INV_EV = 5.067e6

# Fundamental Constants
M_PL_REDUCED = 2.435e18 * 1e9 # 2.435e27 eV (Reduced Planck Mass)
M_PL = M_PL_REDUCED # Use reduced as per standard field theory conventions

# Solar Properties
M_SUN_KG = 1.989e30
R_SUN_M = 6.957e8
R_SUN_INV_EV = R_SUN_M * M_TO_INV_EV

# Densities
RHO_SUN_KG_M3 = 1408.0 # Mean density
RHO_SUN_EV4 = RHO_SUN_KG_M3 * KG_TO_EV / (M_TO_INV_EV**3)

RHO_GAL_KG_M3 = 1.0e-24 # approx 1 proton / cm^3
RHO_GAL_EV4 = RHO_GAL_KG_M3 * KG_TO_EV / (M_TO_INV_EV**3)

# Gravitational Potential at Surface (Dimensionless)
# Phi_N = G M / (R c^2)
PHI_N_SURFACE = (const.G * M_SUN_KG) / (R_SUN_M * const.c**2)

# === Model Parameters ===
# Best fit from search_viable_chameleon.py
# n = 3, Lambda = 11.7 keV
N_POWER = 3.0
LAMBDA_EV = 11.7e3 
BETA = 1.0 # Coupling strength

def get_equilibrium_phi(rho):
    """ 
    Solve V'(phi) + beta/M_pl * rho = 0 
    for V(phi) = Lambda^(4+n) / phi^n
    V'(phi) = -n * Lambda^(4+n) * phi^(-n-1)
    
    n * Lambda^(4+n) / phi^(n+1) = beta * rho / M_pl
    phi^(n+1) = (n * M_pl * Lambda^(4+n)) / (beta * rho)
    """
    term = (N_POWER * M_PL * (LAMBDA_EV**(4+N_POWER))) / (BETA * rho)
    return term**(1.0/(N_POWER+1.0))

def get_mass_squared(phi):
    """ V''(phi) """
    # V'' = n(n+1) Lambda^(4+n) phi^(-n-2)
    return N_POWER * (N_POWER+1) * (LAMBDA_EV**(4+N_POWER)) * (phi**(-N_POWER-2.0))

def run_analysis():
    print("\n=== Rigorous PPN / Thin Shell Analysis ===")
    print(f"Model: Inverse Power n={N_POWER}, Lambda={LAMBDA_EV:.2e} eV")
    
    # 1. Calculate Equilibrium Fields
    phi_gal = get_equilibrium_phi(RHO_GAL_EV4)
    phi_core = get_equilibrium_phi(RHO_SUN_EV4)
    
    print(f"\nEquilibrium Field Values:")
    print(f"  Galactic (Vacuum): {phi_gal:.2e} eV")
    print(f"  Solar Core:        {phi_core:.2e} eV")
    
    # 2. Calculate Masses and Ranges
    m2_gal = get_mass_squared(phi_gal)
    m2_core = get_mass_squared(phi_core)
    
    range_gal = 1.0 / np.sqrt(m2_gal) # in eV^-1
    range_core = 1.0 / np.sqrt(m2_core)
    
    range_gal_m = range_gal / M_TO_INV_EV
    range_core_m = range_core / M_TO_INV_EV
    
    print(f"\nScalar Force Range (Compton Wavelength):")
    print(f"  Galactic: {range_gal_m:.2e} m ({range_gal_m/3.086e19:.2e} kpc)")
    print(f"  Solar:    {range_core_m:.2e} m")
    
    # 3. Thin Shell Parameter epsilon
    # epsilon = (phi_gal - phi_core) / (6 * beta * M_pl * Phi_N)
    # Note: Phi_N is dimensionless (~2e-6). M_pl is in eV. Result is dimensionless.
    
    delta_phi = np.abs(phi_gal - phi_core)
    epsilon = delta_phi / (6.0 * BETA * M_PL * PHI_N_SURFACE)
    
    print(f"\nThin Shell Parameter:")
    print(f"  Delta Phi: {delta_phi:.2e} eV")
    print(f"  Newtonian Potential: {PHI_N_SURFACE:.2e}")
    print(f"  Epsilon: {epsilon:.4e}")
    
    # 4. PPN Gamma
    # If epsilon << 1, the object is screened.
    # The scalar charge Q_eff = 3 * epsilon * M_sun * beta.
    # Force ratio F_phi / F_N = 6 * beta^2 * epsilon.
    # Gamma - 1 = - (F_phi / F_N) approx - 6 * beta^2 * epsilon.
    
    force_ratio = 6.0 * (BETA**2) * epsilon
    gamma_deviation = force_ratio
    
    print(f"\nPredictions at Solar System Scale:")
    print(f"  Force Ratio F_phi / F_N: {force_ratio:.4e}")
    print(f"  PPN Gamma Deviation |1-gamma|: {gamma_deviation:.4e}")
    
    # Constraints
    # Cassini: |gamma - 1| < 2.3e-5
    limit = 2.3e-5
    
    if gamma_deviation < limit:
        print(f"\n[PASS] The model satisfies Cassini constraints ({gamma_deviation:.2e} < {limit:.2e}).")
        print("Calculation confirms the Thin Shell suppression is sufficient.")
    else:
        print(f"\n[FAIL] The model violates Cassini constraints ({gamma_deviation:.2e} > {limit:.2e}).")
        print("The potential is not steep enough or Lambda is wrong.")

if __name__ == "__main__":
    run_analysis()