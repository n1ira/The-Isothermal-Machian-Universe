import numpy as np
import scipy.constants as const

# === Constants ===
M_PL = 2.435e27 # eV
KG_TO_EV = 5.609e35
M_TO_INV_EV = 5.067e6

# === Model ===
N_POWER = 3.0
LAMBDA_EV = 11.7e3
BETA = 1.0

# === Earth ===
M_EARTH_KG = 5.972e24
R_EARTH_M = 6.371e6
R_ORBIT_M = R_EARTH_M + 700e3 # 700 km
# Newtonian Potential (Dimensionless)
# Phi = GM/Rc^2
PHI_EARTH = (const.G * M_EARTH_KG) / (R_EARTH_M * const.c**2)
# Potential at Orbit
PHI_ORBIT = (const.G * M_EARTH_KG) / (R_ORBIT_M * const.c**2)

# === Background Field ===
# Assumed Galactic Vacuum (worst case for screening)
RHO_GAL_EV4 = 1.0e-24 * KG_TO_EV / (M_TO_INV_EV**3)
PHI_BG = ( (N_POWER * M_PL * LAMBDA_EV**(4+N_POWER)) / (BETA * RHO_GAL_EV4) )**(1.0/(N_POWER+1.0))

# === Core Field ===
# Earth Mean Density
RHO_EARTH_EV4 = 5515.0 * KG_TO_EV / (M_TO_INV_EV**3)
PHI_CORE = ( (N_POWER * M_PL * LAMBDA_EV**(4+N_POWER)) / (BETA * RHO_EARTH_EV4) )**(1.0/(N_POWER+1.0))

def run_analysis():
    print("\n=== MICROSCOPE Analytical Test ===")
    print(f"Model: n={N_POWER}, Lambda={LAMBDA_EV/1e3:.2f} keV")
    print(f"Earth Potential (Surface): {PHI_EARTH:.2e}")
    print(f"Earth Potential (Orbit):   {PHI_ORBIT:.2e}")
    print(f"Background Field: {PHI_BG:.2e} eV")
    
    # Thin Shell Parameter epsilon
    # epsilon = (phi_bg - phi_core) / (6 * beta * M_pl * Phi_N)
    # Use Phi_N at surface for the screening of the object
    
    epsilon = (PHI_BG - PHI_CORE) / (6.0 * BETA * M_PL * PHI_EARTH)
    
    print(f"Thin Shell Parameter epsilon: {epsilon:.2e}")
    
    # Suppression Factor at Orbit
    # The scalar force is suppressed by epsilon inside the shell?
    # Outside the shell, the profile is Q / r.
    # Q_eff = M_eff * epsilon ? 
    # Acceleration ratio F_phi / F_N = 6 beta^2 * epsilon * (R_Earth / r)^2 / (R_Earth / r)^2 ?
    # No, both scale as 1/r^2 outside.
    # So Ratio is constant = 6 * beta^2 * epsilon.
    
    force_ratio = 6.0 * (BETA**2) * epsilon
    print(f"Force Ratio F_phi / F_G: {force_ratio:.2e}")
    
    # Eotvos Parameter
    # eta = d_acc / acc = (beta_A - beta_B) * F_phi / F_G / beta
    # If we assume non-universality delta_beta = |beta_A - beta_B|
    # Standard assumption for composition dependence (if not protected by symmetry): 
    # delta_beta ~ 10^-3 (electromagnetic contribution difference)
    
    eta_predicted_weak = 1e-3 * force_ratio
    eta_predicted_strong = 1.0 * force_ratio # If beta varies by O(1) - unlikely
    
    print(f"Predicted eta (assuming delta_beta ~ 10^-3): {eta_predicted_weak:.2e}")
    print("MICROSCOPE Limit: 1e-15")
    
    if eta_predicted_weak < 1e-15:
        print("PASS: Theory is safe.")
    else:
        print("FAIL: Theory violates MICROSCOPE unless delta_beta is tiny.")
        req_delta = 1e-15 / force_ratio
        print(f"Required Universality: delta_beta < {req_delta:.2e}")
        print("Conclusion: The theory MUST enforce strict Conformal Symmetry to survive.")

if __name__ == "__main__":
    run_analysis()