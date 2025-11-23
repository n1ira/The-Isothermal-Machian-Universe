import numpy as np
from scipy.optimize import minimize_scalar

# === Constants (SI) ===
G = 6.674e-11
c = 2.998e8
M_PL = 2.176e-8 # Planck mass (kg) reduced? Usually reduced is used in theory.
# Reduced Planck Mass M_pl = sqrt(hbar*c/8piG) = 4.34e-9 kg. 
# Let's be consistent with the formulation: Laplacian phi = V' ...
# If phi has dimension of mass (standard), then V has dim mass^4.
# Let's use dimensionless units relative to M_PL for phi.
# Then V is dimensionless * M_PL^4? No, let's stick to simple scaling.

# Densities (kg/m^3)
RHO_COSMO = 9.9e-27 # Critical density
RHO_GAL   = 1.0e-24 # ISM (1 proton per cm3 approx)
RHO_SUN   = 1.5e5   # Core density (simplified) or mean density 1400. Let's use mean.
RHO_SUN_MEAN = 1408.0 

# Scales
R_GAL_REQ = 3.086e19 # 1 kpc in meters
PHI_N_SUN = 2.12e-6  # Newtonian potential of Sun

def check_model(params):
    """
    Check if a given (n, Lambda) model satisfies constraints.
    V(phi) = Lambda^(4+n) / phi^n
    """
    n = params[0]
    log10_Lambda = params[1] # Scale in eV? Or SI? 
    
    # Let's work in SI units for V and phi.
    # Phi has units of Mass [kg].
    # V has units of density? Energy density J/m^3?
    # In field theory equation Box phi = V', if phi is mass [kg], 
    # dimensions are weird in SI.
    
    # Let's switch to Natural Units (eV) for the calculation, then convert constraints.
    # 1 kg = 5.6e35 eV
    # 1 m = 5.0e6 1/eV
    # 1 sec = 1.5e15 1/eV
    
    kg_to_eV = 5.61e35
    m_to_inv_eV = 5.07e6
    
    rho_gal_eV = RHO_GAL * kg_to_eV / (m_to_inv_eV**3) # eV^4
    rho_sun_eV = RHO_SUN_MEAN * kg_to_eV / (m_to_inv_eV**3)
    
    M_pl_eV = 2.435e18 * 1e9 # 2.4e27 eV (Reduced Planck Mass)
    
    Lambda_eV = 10**log10_Lambda
    
    # Potential: V(phi) = Lambda^(4+n) / phi^n
    # Effective Potential Min: V_eff' = -n Lambda^(4+n) phi^(-n-1) + rho/M_pl = 0
    # rho/M_pl = n Lambda^(4+n) / phi^(n+1)
    # phi = [ (n M_pl Lambda^(4+n)) / rho ] ^ (1/(n+1))
    
    def get_phi_min(rho):
        term = (n * M_pl_eV * (Lambda_eV**(4+n))) / rho
        return term**(1.0/(n+1.0))
        
    def get_mass_sq(phi):
        # V'' = n(n+1) Lambda^(4+n) phi^(-n-2)
        return n * (n+1) * (Lambda_eV**(4+n)) * (phi**(-n-2.0))
    
    # 1. Galaxy Check
    phi_gal = get_phi_min(rho_gal_eV)
    m_sq_gal = get_mass_sq(phi_gal)
    range_gal_inv_eV = 1.0 / np.sqrt(m_sq_gal)
    range_gal_m = range_gal_inv_eV / m_to_inv_eV
    
    # Constraint: Range should be ~ 1 kpc (3e19 m)
    score_gal = (np.log10(range_gal_m) - 19.5)**2 # Log diff
    
    # 2. Solar System Check
    phi_sun = get_phi_min(rho_sun_eV)
    # Thin Shell Parameter epsilon
    # epsilon = (phi_gal - phi_sun) / (6 * beta * M_pl * Phi_N)
    # Assume beta = 1
    
    delta_phi = phi_gal - phi_sun
    epsilon = delta_phi / (6.0 * 1.0 * M_pl_eV * PHI_N_SUN)
    
    # Constraint: Epsilon < 1e-6
    # We penalize if epsilon > 1e-7
    if epsilon > 1e-6:
        score_sun = (np.log10(epsilon) - (-7.0))**2 * 10.0 # Strong penalty
    else:
        score_sun = 0.0
        
    return score_gal + score_sun

def run_search():
    print("Searching for Viable Chameleon Parameters (n, Lambda)...")
    
    # Grid Search first to find basin
    best_score = 1e9
    best_params = None
    
    for n in [1, 2, 3, 4, 5, 6]:
        for log_L in np.linspace(-10, 5, 20): # eV scale
            score = check_model([n, log_L])
            if score < best_score:
                best_score = score
                best_params = [n, log_L]
                
    print(f"Best Grid Guess: n={best_params[0]}, log_L={best_params[1]:.2f}")
    
    # Refine
    from scipy.optimize import minimize
    res = minimize(check_model, best_params, method='Nelder-Mead', tol=1e-4)
    
    print("\n=== Optimized Parameters ===")
    n_opt = res.x[0]
    L_opt = 10**res.x[1]
    print(f"Power Index n: {n_opt:.4f}")
    print(f"Scale Lambda: {L_opt:.4e} eV")
    
    # Recalculate physicals
    # Re-run the calc logic to print details
    kg_to_eV = 5.61e35
    m_to_inv_eV = 5.07e6
    rho_gal_eV = RHO_GAL * kg_to_eV / (m_to_inv_eV**3)
    rho_sun_eV = RHO_SUN_MEAN * kg_to_eV / (m_to_inv_eV**3)
    M_pl_eV = 2.435e27
    
    def get_phi_min(rho, n, L):
        term = (n * M_pl_eV * (L**(4+n))) / rho
        return term**(1.0/(n+1.0))
    
    def get_range(phi, n, L):
        m_sq = n * (n+1) * (L**(4+n)) * (phi**(-n-2.0))
        return (1.0 / np.sqrt(m_sq)) / m_to_inv_eV
        
    phi_gal = get_phi_min(rho_gal_eV, n_opt, L_opt)
    r_gal = get_range(phi_gal, n_opt, L_opt)
    
    phi_sun = get_phi_min(rho_sun_eV, n_opt, L_opt)
    delta_phi = phi_gal - phi_sun
    epsilon = delta_phi / (6.0 * 1.0 * M_pl_eV * PHI_N_SUN)
    
    print(f"Galaxy Range: {r_gal:.2e} m ({r_gal/3.086e19:.2f} kpc)")
    print(f"Solar System Epsilon: {epsilon:.2e}")
    
    if epsilon < 1e-6 and 0.1 < (r_gal/3.086e19) < 10.0:
        print("SUCCESS: A viable parameter set exists!")
    else:
        print("FAILURE: Could not satisfy both constraints simultaneously.")

if __name__ == "__main__":
    run_search()
