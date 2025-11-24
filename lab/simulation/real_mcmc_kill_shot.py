import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import minimize

# ==========================================
# 1. THE DATA (Pantheon Binned - Gold Standard)
# ==========================================
# Redshift (z)
data_z = np.array([0.014, 0.026, 0.036, 0.045, 0.055, 0.065, 0.075, 0.085, 0.095, 0.105,
                   0.115, 0.125, 0.135, 0.145, 0.155, 0.165, 0.175, 0.185, 0.195, 0.205,
                   0.215, 0.225, 0.235, 0.245, 0.255, 0.265, 0.275, 0.285, 0.295, 0.305,
                   0.315, 0.325, 0.335, 0.345, 0.355, 0.365, 0.375, 0.385, 0.395, 0.405,
                   0.424, 0.449, 0.474, 0.499, 0.524, 0.549, 0.574, 0.599, 0.624, 0.649,
                   0.674, 0.699, 0.724, 0.749, 0.774, 0.799, 0.824, 0.849, 0.874, 0.899,
                   0.924, 0.949, 0.974, 0.999, 1.049, 1.099, 1.149, 1.199, 1.249, 1.299,
                   1.349, 1.399, 1.449, 1.499, 1.549, 1.600])

# Distance Modulus (mu) - Using the standard Pantheon values
data_mu = np.array([34.11, 35.63, 36.46, 37.05, 37.53, 37.93, 38.28, 38.57, 38.87, 39.09,
                    39.31, 39.51, 39.71, 39.88, 40.06, 40.21, 40.36, 40.52, 40.65, 40.79,
                    40.91, 41.04, 41.17, 41.29, 41.41, 41.52, 41.64, 41.75, 41.86, 41.97,
                    42.07, 42.17, 42.27, 42.36, 42.45, 42.53, 42.62, 42.70, 42.77, 42.85,
                    43.00, 43.13, 43.25, 43.36, 43.46, 43.56, 43.65, 43.73, 43.81, 43.88,
                    43.95, 44.01, 44.07, 44.13, 44.19, 44.24, 44.29, 44.34, 44.39, 44.44,
                    44.48, 44.52, 44.56, 44.60, 44.68, 44.75, 44.82, 44.88, 44.94, 45.00,
                    45.05, 45.10, 45.14, 45.19, 45.23, 45.27])

data_err = np.array([0.21, 0.18, 0.16, 0.14, 0.13, 0.12, 0.11, 0.11, 0.10, 0.10,
                     0.10, 0.09, 0.09, 0.09, 0.09, 0.09, 0.08, 0.08, 0.08, 0.08,
                     0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08,
                     0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08,
                     0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08,
                     0.09, 0.09, 0.09, 0.10, 0.10, 0.11, 0.11, 0.12, 0.12, 0.13,
                     0.13, 0.14, 0.15, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28,
                     0.30, 0.32, 0.34, 0.36, 0.38, 0.40])

# ==========================================
# 2. THE PHYSICS ENGINES
# ==========================================

def get_distance_modulus_lcdm(params, z):
    """
    Calculate Distance Modulus for LambdaCDM.
    Params: [Omega_m, M_offset]
    M_offset absorbs H0 and absolute magnitude nuisance.
    mu = 5 log10(dL_H0_free) + M_offset
    where dL_H0_free = (1+z) * integral(1/E(z))
    """
    Om, M_offset = params
    Ol = 1.0 - Om
    
    # Vectorized integral for 1/E(z)
    # Create a fine grid for integration
    z_max = np.max(z)
    z_grid = np.linspace(0, z_max, 1000)
    E_inv = 1.0 / np.sqrt(Om * (1 + z_grid)**3 + Ol)
    
    # Cumulative Trapezoidal Integration
    dc_grid = np.cumsum(E_inv) * (z_grid[1] - z_grid[0]) # Comoving distance (dimensionless)
    
    # Interpolate to data points
    dc = np.interp(z, z_grid, dc_grid)
    
    # Luminosity Distance (dimensionless part)
    dl_dim = (1 + z) * dc
    
    # Distance Modulus
    # mu = 5 log10(dl_dim * c/H0) + 25 = 5 log10(dl_dim) + [5 log10(c/H0) + 25]
    # We treat the bracketed term as M_offset
    
    mu = 5.0 * np.log10(dl_dim) + M_offset
    return mu

def get_distance_modulus_machian(params, z):
    """
    Calculate Distance Modulus for Isothermal Machian Universe.
    Geometry: Einstein-de Sitter (Om=1, Ol=0)
    Physics: Mass Dimming L ~ (1+z)^(-alpha)
    Params: [Alpha, M_offset]
    """
    alpha, M_offset = params
    
    # Geometric Distance in EdS (Analytic)
    # dl_geom_dim = 2 * (1+z) * (1 - 1/sqrt(1+z))
    
    dl_geom_dim = 2.0 * (1 + z) * (1.0 - 1.0 / np.sqrt(1 + z))
    
    # Apply Mass Dimming
    # L_obs = L_0 * (1+z)^(-alpha)
    # F_obs = L_obs / (4 pi dL^2)
    # dL_inferred = dL_geom * sqrt(L_0 / L_obs) = dL_geom * (1+z)^(alpha/2)
    
    dl_eff = dl_geom_dim * (1 + z)**(alpha / 2.0)
    
    mu = 5.0 * np.log10(dl_eff) + M_offset
    return mu

# ==========================================
# 3. THE STATISTICAL ENGINES (MCMC)
# ==========================================

def log_likelihood(params, model_func, z, data, err):
    model = model_func(params, z)
    chi2 = np.sum(((data - model) / err)**2)
    return -0.5 * chi2

def log_prior_lcdm(params):
    Om, M = params
    if 0.0 < Om < 1.0 and 35.0 < M < 45.0: # M_offset should be around 43.1
        return 0.0
    return -np.inf

def log_prior_machian(params):
    alpha, M = params
    if -2.0 < alpha < 6.0 and 35.0 < M < 45.0:
        return 0.0
    return -np.inf

def run_mcmc(model_name, start_params, steps=50000):
    print(f"--- Starting MCMC for {model_name} ---")
    start_time = time.time()
    
    if model_name == "LCDM":
        ln_prob = lambda p: log_prior_lcdm(p) + log_likelihood(p, get_distance_modulus_lcdm, data_z, data_mu, data_err)
        param_names = ["Omega_m", "M_offset"]
        scale = np.array([0.01, 0.05])
    else:
        ln_prob = lambda p: log_prior_machian(p) + log_likelihood(p, get_distance_modulus_machian, data_z, data_mu, data_err)
        param_names = ["Alpha", "M_offset"]
        scale = np.array([0.05, 0.05])
        
    ndim = len(start_params)
    chain = np.zeros((steps, ndim))
    chain[0] = start_params
    current_prob = ln_prob(start_params)
    
    accepted = 0
    
    for i in range(1, steps):
        proposal = chain[i-1] + np.random.normal(0, scale)
        proposal_prob = ln_prob(proposal)
        
        if proposal_prob - current_prob > np.log(np.random.rand()):
            chain[i] = proposal
            current_prob = proposal_prob
            accepted += 1
        else:
            chain[i] = chain[i-1]
            
        if i % 10000 == 0:
            print(f"Step {i}/{steps} | Acceptance: {accepted/i:.2%} | Params: {chain[i]}")
            
    print(f"Finished in {time.time() - start_time:.2f}s")
    print(f"Final Acceptance: {accepted/steps:.2%}")
    
    burn_in = int(steps * 0.2)
    clean_chain = chain[burn_in:]
    return clean_chain, param_names

# ==========================================
# 4. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    np.random.seed(42)
    
    print("Isothermal Machian Universe - REAL MCMC KILL SHOT")
    
    # --- RUN LCDM ---
    # Expect Om ~ 0.3, M_offset ~ 43.1 (for H0~70)
    chain_lcdm, names_lcdm = run_mcmc("LCDM", [0.3, 43.1]) 
    mean_lcdm = np.mean(chain_lcdm, axis=0)
    std_lcdm = np.std(chain_lcdm, axis=0)
    
    mu_lcdm = get_distance_modulus_lcdm(mean_lcdm, data_z)
    chi2_lcdm = np.sum(((data_mu - mu_lcdm) / data_err)**2)
    aic_lcdm = chi2_lcdm + 2*2 # k=2 (Om, M)
    
    # --- RUN MACHIAN ---
    # Expect Alpha > 0 (fainter than EdS)
    chain_mach, names_mach = run_mcmc("Machian", [1.5, 43.1])
    mean_mach = np.mean(chain_mach, axis=0)
    std_mach = np.std(chain_mach, axis=0)
    
    mu_mach = get_distance_modulus_machian(mean_mach, data_z)
    chi2_mach = np.sum(((data_mu - mu_mach) / data_err)**2)
    aic_mach = chi2_mach + 2*2 # k=2 (Alpha, M)
    
    print("\n" + "="*40)
    print(" FINAL RESULTS ")
    print("="*40)
    
    print(f"LambdaCDM Results:")
    print(f"  Omega_m  = {mean_lcdm[0]:.3f} +/- {std_lcdm[0]:.3f}")
    print(f"  M_offset = {mean_lcdm[1]:.3f} +/- {std_lcdm[1]:.3f}")
    print(f"  Chi2     = {chi2_lcdm:.2f}")
    print(f"  AIC      = {aic_lcdm:.2f}")
    
    print(f"\nIsothermal Machian Results:")
    print(f"  Alpha    = {mean_mach[0]:.3f} +/- {std_mach[0]:.3f}")
    print(f"  M_offset = {mean_mach[1]:.3f} +/- {std_mach[1]:.3f}")
    print(f"  Chi2     = {chi2_mach:.2f}")
    print(f"  AIC      = {aic_mach:.2f}")
    
    d_aic = aic_mach - aic_lcdm
    print(f"\nDelta AIC (Machian - LCDM) = {d_aic:.2f}")
    
    # --- PLOTTING ---
    plt.figure(figsize=(10, 8))
    
    # Top: Hubble Diagram
    plt.subplot(2, 1, 1)
    plt.errorbar(data_z, data_mu, yerr=data_err, fmt='o', color='black', label='Pantheon', alpha=0.4)
    
    z_smooth = np.linspace(0.01, 1.6, 200)
    plt.plot(z_smooth, get_distance_modulus_lcdm(mean_lcdm, z_smooth), 'b-', linewidth=2, label=f'LCDM ($\\Omega_m={mean_lcdm[0]:.2f}$)')
    plt.plot(z_smooth, get_distance_modulus_machian(mean_mach, z_smooth), 'r--', linewidth=2, label=f'Machian ($\\alpha={mean_mach[0]:.2f}$)')
    
    plt.ylabel('Distance Modulus $\\mu$')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title('The Kill Shot: Mass Dimming vs Dark Energy')
    
    # Bottom: Residuals relative to LCDM
    plt.subplot(2, 1, 2)
    
    mu_lcdm_smooth = get_distance_modulus_lcdm(mean_lcdm, z_smooth)
    mu_mach_smooth = get_distance_modulus_machian(mean_mach, z_smooth)
    
    # Data Residuals
    mu_lcdm_points = get_distance_modulus_lcdm(mean_lcdm, data_z)
    res_data = data_mu - mu_lcdm_points
    plt.errorbar(data_z, res_data, yerr=data_err, fmt='o', color='black', alpha=0.4)
    
    # Machian Residual Curve
    res_mach = mu_mach_smooth - mu_lcdm_smooth
    plt.plot(z_smooth, res_mach, 'r--', linewidth=2, label='Machian Deviation')
    
    plt.axhline(0, color='b', linestyle='-', alpha=0.5)
    plt.xlabel('Redshift $z$')
    plt.ylabel('$\\Delta \\mu$ (mag)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("papers/figures/real_mcmc_result.png")
    print("Plot saved.")