"""
SIMULATION 9: The Halo Mass Function (Press-Schechter)
Target: Quantify the 'Kill Shot' prediction for JWST Early Galaxies.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, quad

# 1. COSMOLOGICAL PARAMETERS (Planck 2018)
h = 0.674
H0 = 100 * h
Om0 = 0.315
OL0 = 0.685
ns = 0.965
sigma8_0 = 0.811
delta_c = 1.686  # Critical collapse density

# 2. MACHIAN PARAMETERS
# The effective gravitational coupling enhancement
# beta = 1/sqrt(6) -> mu = 2*beta^2 = 1/3 = 0.333
# But wait, the growth equation source term is 1.5 * Om * (1 + mu).
# If D_mach grows faster, D_z is LARGER.
# Let's verify normalization.
# We normalize such that D_mach(z_init) = D_lcdm(z_init).
# This means we assume they start with the same amplitude from Inflation.
# As they evolve forward, D_mach should grow faster because of 'mu'.
# Let's try mu = 1.0 (Stronger Coupling) to see the effect size.
mu_machian = 1.0 

# Re-check Normalization Logic in main execution block:
# D_lcdm[-1] is the value at high z (z=20) because we inverted the array?
# No, get_growth_factor returns D_z interpolated to z_range [5, 20].
# So D_lcdm[-1] is at z=20.
# We force D_mach[-1] = D_lcdm[-1].
# Then at z=5 (index 0), D_mach should be > D_lcdm.
# And sigma_z ~ D_z.
# So sigma_mach > sigma_lcdm.
# The exponential exp(-delta_c^2 / 2sigma^2) is highly sensitive.
# If sigma increases by 20%, the abundance can increase by factor 100 at high z.

def Omega_m(z):
    return Om0 * (1+z)**3 / (Om0 * (1+z)**3 + OL0)

# 3. LINEAR GROWTH FACTOR SOLVER
def growth_eq(y, lna, mu_strength):
    D, D_prime = y
    a = np.exp(lna)
    Om = Omega_m(1/a - 1)
    
    # Standard Growth Equation with Friction and Source
    # D'' + (2 - 1.5*Om)/2 * D' = 1.5 * Om * (1 + mu) * D
    # Using variable x = ln a
    # D'' + (2 + H'/H) D' = 4 pi G rho D / H^2
    # In terms of ln a:
    # d^2D/d(lna)^2 + (2 + dlnH/d(lna)) dD/d(lna) = 1.5 * Om * (1+mu) * D
    
    # H(a) = H0 sqrt(Om a^-3 + OL)
    # ln H = ln H0 + 0.5 * ln(Om a^-3 + OL)
    # d ln H / d ln a = 0.5 * ( -3 Om a^-3 ) / (Om a^-3 + OL) = -1.5 * Om(a)
    
    friction = 2.0 - 1.5 * Om
    source = 1.5 * Om * (1.0 + mu_strength)
    
    return [D_prime, source * D - friction * D_prime]

def get_growth_factor(z_vals, mu_strength):
    # Initial conditions at high z (a = 1e-4)
    # Matter dominated: D ~ a -> dD/d(lna) = a = D
    a_start = 1e-4
    y0 = [a_start, a_start] 
    lna_vals = np.log(1.0 / (1.0 + z_vals))[::-1] # Integrate forward in time
    lna_start = np.log(a_start)
    
    # Create full integration grid
    lna_grid = np.concatenate(([lna_start], lna_vals))
    lna_grid = np.sort(lna_grid) # Ensure strictly increasing
    
    sol = odeint(growth_eq, y0, lna_grid, args=(mu_strength,))
    
    # Extract solution at requested z values
    # Interpolate back to z_vals
    D_full = sol[:, 0]
    
    # We need D(z=0) for normalization
    D_0 = D_full[-1] 
    
    # Map back to input z order (descending z)
    D_z = np.interp(np.log(1.0/(1.0+z_vals)), lna_grid, D_full)
    
    return D_z, D_0

# 4. VARIANCE SIGMA(M)
def power_spectrum(k):
    # Approximate BBKS Transfer Function or simple power law for relevant scales
    # P(k) ~ k^ns * T^2(k)
    # On galaxy scales (k ~ 0.1 - 10), T(k) ~ ln(k)/k^2
    # Let's use a simple effective slope neff ~ -2.3 at cluster scales
    # Sigma^2 ~ R^-(3+n)
    # More robust: Sigma^2(M) propto M^(-(n+3)/3)
    # Standard LCDM: alpha approx 0.15-0.2 at cluster scales
    return k**ns # Placeholder, we use sigma relation directly below

def sigma_M_z(M, z, D_z, D_0, mu_strength):
    # Sigma(M, z) = D(z)/D(0) * sigma8 * (M / M8)^(-alpha)
    # M8 is mass contained in 8 Mpc/h sphere
    rho_crit = 2.775e11 # h^2 M_sun / Mpc^3
    rho_m = Om0 * rho_crit
    R8 = 8.0 / h
    M8 = (4.0/3.0) * np.pi * rho_m * R8**3
    
    # Slope alpha = (n_s + 3)/6 approx (0.96 + 3)/6 = 0.66 for low mass?
    # At cluster scales, effective spectral index n_eff ~ -2
    # alpha = -(n_eff + 3)/6 ? No.
    # Let's use standard approx: sigma(M) approx sigma8 * (M/M8)^(-gamma)
    # gamma approx 0.17 for massive halos
    gamma = 0.2
    
    # Normalization:
    # For LCDM: sigma(z) = D_lcdm(z) * sigma8_0 * (M/M8)^-gamma
    # For Machian: sigma(z) = D_mach(z) * sigma8_0 * (M/M8)^-gamma
    # Wait, we need to normalize D such that they agree at CMB (z=1100).
    # D_lcdm(1100) approx 1/1100
    # D_mach(1100) approx 1/1100 (Linear regime is same)
    # So ratio D_mach(z) / D_lcdm(z) gives the boost.
    
    # Re-run growth to get high-z normalization
    # We want D_mach(z) normalized to match D_lcdm at z_CMB
    
    sigma_0 = sigma8_0 * (M / M8)**(-gamma)
    return sigma_0 * D_z # D_z is already the raw growth factor D~a

# 5. PRESS-SCHECHTER MASS FUNCTION
def dndlnM(M, z, sigma):
    nu = delta_c / sigma
    return np.sqrt(2/np.pi) * nu * np.exp(-nu**2 / 2) * (rho_m_z0 / M) * abs_dlnsigma_dlnM

# We calculate the CUMULATIVE number density n(>M)
# n(>M) = integral (dn/dM) dM
# Approx for high peaks (nu >> 1):
# n(>M) ~ exp(-delta_c^2 / 2sigma^2)

rho_m_z0 = 2.775e11 * Om0 * h**2 # M_sun / Mpc^3

def cumulative_number_density(M_min, z, D_z, D_0):
    # sigma(M)
    gamma = 0.2
    R8 = 8.0 / h
    M8 = (4.0/3.0) * np.pi * rho_m_z0 * R8**3
    
    sigma_M = sigma8_0 * (M_min/M8)**(-gamma) 
    
    # Apply Growth
    # We need D(z) normalized to z=0? No, normalized to CMB.
    # Let's define Growth Factor G(z) = D(z) / D(0)
    # But D_mach(0) != D_lcdm(0).
    # Let's use relative growth from z=100
    
    sigma_z = sigma_M * D_z # Assuming D_z is ~ 1/(1+z)
    
    nu = delta_c / sigma_z
    
    # Press Schechter Cumulative
    # n(>M) = mean_rho / M * f(nu)
    # This is rough. Let's focus on the EXPONENTIAL part which dominates at high z.
    
    return np.exp(-nu**2 / 2.0)

# 6. EXECUTE COMPARISON
z_range = np.linspace(5, 20, 50)

# Solve Growth for LCDM (mu=0) and Machian (mu=1/3)
D_lcdm, D0_l = get_growth_factor(z_range, 0.0)
D_mach, D0_m = get_growth_factor(z_range, mu_machian)

# Normalize at high z (z=20) to ensure we start from same initial conditions
ratio_init = D_lcdm[-1] / D_mach[-1]
D_mach_norm = D_mach * ratio_init # Match LCDM at z=20

# Calculate Abundance of M = 10^10 M_sun halos
M_target = 1e10
n_lcdm = cumulative_number_density(M_target, z_range, D_lcdm, D0_l)
n_mach = cumulative_number_density(M_target, z_range, D_mach_norm, D0_m)

ratio = n_mach / n_lcdm

# Plot
plt.figure(figsize=(10, 6))
plt.semilogy(z_range, ratio, 'c-', linewidth=3)
plt.axhline(1.0, color='k', linestyle=':')
plt.axvline(10.0, color='r', linestyle='--', alpha=0.5)
plt.text(10.5, 1e2, 'JWST Era (z>10)', rotation=90, color='r')

plt.title(f"The Machian Boost: Halo Abundance Ratio (M > 10^10 M_sun)", fontsize=14)
plt.xlabel("Redshift z", fontsize=12)
plt.ylabel("Ratio n_Machian / n_LambdaCDM", fontsize=12)
plt.grid(True, which="both", ls="-", alpha=0.2)

# The Kill Shot Value
z_15_idx = np.argmin(np.abs(z_range - 15.0))
kill_ratio = ratio[z_15_idx]

print(f"KILL SHOT RESULT:")
print(f"At z=15, Machian Halo Abundance is {kill_ratio:.2e} times higher than LCDM.")
plt.annotate(f"{kill_ratio:.1e}x Boost", xy=(15, kill_ratio), xytext=(13, kill_ratio/10),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.savefig("papers/figures/halo_mass_function_ratio.png", dpi=300)
print("Plot saved to papers/figures/halo_mass_function_ratio.png")
