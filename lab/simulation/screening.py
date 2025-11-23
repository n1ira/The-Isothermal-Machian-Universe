"""
Screening Check for Isothermal Machian Universe
Goal: Determine if the galactic scalar parameters (R=0.89 kpc, beta=0.98)
are compatible with Solar System constraints via the Chameleon Mechanism.
"""

import numpy as np

# Physical Constants
c = 2.998e10        # cm/s
G = 6.674e-8        # cm^3 / g s^2
hbar = 1.054e-27    # erg s
eV_to_erg = 1.602e-12
M_pl = np.sqrt(hbar * c / (8 * np.pi * G)) # Reduced Planck Mass (g) -> approx 2.4e18 GeV ??
# In cgs: M_pl = sqrt(hbar*c/8piG) = 4.34e-6 g
# Let's stick to standard units carefully.

# Planck Mass in grams
# M_pl_reduced = 2.435e18 GeV / c^2
# 1 GeV = 1.78e-24 g
# M_pl = 4.341e-6 g
M_pl_g = 4.341e-6 

# Parameters from Galaxy Fit
R_gal_kpc = 0.89
beta_gal = 0.98

# Conversions
kpc_to_cm = 3.086e21
R_gal_cm = R_gal_kpc * kpc_to_cm

def check_screening():
    print("Running Solar System Screening Check...")
    print("-" * 60)

    # 1. Define the Galactic Vacuum Field (phi_env)
    # In the galaxy outskirts (vacuum), the field follows phi(r) ~ phi0 * (1 + r/R)^beta
    # Near the Solar System (r ~ 8 kpc), the background density is low (ISM).
    # rho_ism ~ 1 proton / cm^3 ~ 1.67e-24 g/cm^3
    
    rho_ism = 1.67e-24
    rho_sun = 1.41       # g/cm^3 (Average density of Sun)
    Phi_sun = 2e-6       # Newtonian Potential of Sun at surface (dimensionless)
    
    print(f"Environment Density (ISM): {rho_ism:.2e} g/cm^3")
    print(f"Object Density (Sun):      {rho_sun:.2f} g/cm^3")
    
    # 2. The Coupling Strength
    # In Paper 1, we assumed beta ~ 1 for the galaxy fit.
    # This is the coupling to matter: beta_m * phi * T / M_pl
    # Let's assume standard chameleon coupling beta_m ~ 1 ( Planck strength).
    beta_m = 1.0 
    
    # 3. Thin Shell Condition
    # The object (Sun) has a thin shell if:
    # (phi_env - phi_obj) / (6 * beta_m * M_pl * Phi_Newton) << 1
    
    # We need to estimate phi_env and phi_obj.
    # The potential V(phi) = Lambda^4 * (Lambda/phi)^alpha
    # The minimum is at V'(phi) + beta/M_pl * rho = 0
    
    # phi_min = [ alpha * M_pl * Lambda^(4+alpha) / (beta * rho) ] ^ (1/(alpha+1))
    
    # We need to constrain Lambda and alpha using the Galactic Scale R.
    # The Compton wavelength in vacuum (ISM) must be of order R ~ 1 kpc.
    # m_eff^2 = V''(phi_env) ~ 1/R^2
    
    # Let's solve for Lambda assuming alpha=1 (Inverse power law).
    # m_eff^2 = V''(phi) = 2 * Lambda^5 / phi^3
    # And phi_env approx M_pl * (Lambda^5 / rho_ism)^(1/2)
    
    # Combining: m_eff^2 ~ rho_ism / M_pl^2  (If phi is dominated by density)
    # But in the galaxy outskirts, we want long range.
    # m_eff = hbar / (R * c)
    
    mass_scale_inv_cm = 1.0 / R_gal_cm
    # Convert to energy units
    # E = hbar * c / lambda
    # m_eff_energy = hbar * c / R_gal_cm
    
    print(f"Required Range in ISM:     {R_gal_kpc:.2f} kpc")
    print(f"Inverse Length Scale:      {mass_scale_inv_cm:.2e} cm^-1")
    
    # 4. Calculate Effective Mass in the Sun
    # m_sun / m_ism ~ sqrt(rho_sun / rho_ism) for alpha=1?
    # actually m_eff^2 ~ rho^( (alpha+2)/(alpha+1) )
    
    # For alpha = 1: m_eff^2 ~ rho^(3/2)
    # m_eff (Sun) / m_eff (ISM) = (rho_sun / rho_ism)^(3/4)
    
    ratio_rho = rho_sun / rho_ism
    ratio_m = ratio_rho**(0.75)
    
    m_eff_sun_inv_cm = mass_scale_inv_cm * ratio_m
    lambda_sun_cm = 1.0 / m_eff_sun_inv_cm
    
    print(f"Density Ratio:             10^{np.log10(ratio_rho):.1f}")
    print(f"Screening Range in Sun:    {lambda_sun_cm:.2e} cm")
    
    radius_sun = 6.96e10 # cm
    if lambda_sun_cm < radius_sun:
        print("SUCCESS: Field is short-ranged inside the Sun.")
    else:
        print("FAILURE: Field permeates the Sun.")
        
    # 5. Calculate Thin Shell Factor
    # epsilon = (phi_env - phi_sun) / (6 * beta * M_pl * Phi_N)
    # phi ~ 1/rho
    # phi_env >> phi_sun
    # epsilon approx phi_env / (6 * beta * M_pl * Phi_N)
    
    # phi_env = (M_pl * Lambda^5 / rho_ism)^(1/2) 
    # But we know m_eff in vacuum.
    # phi_env ~ Lambda^5 / m_eff^2 ...
    # Simpler: phi_env * m_eff^2 ~ rho_ism / M_pl
    # phi_env ~ rho_ism / (M_pl * m_eff_ism^2)
    
    # In CGS:
    # M_pl has units of mass? In the equation box phi = rho/M, phi has dimensions of mass.
    # In the geometric units (phi dimensionless), phi ~ rho / (m^2 M_pl^2).
    
    # Let's use the dimension where phi has mass dimension (standard QFT).
    # phi_env = rho_ism / (M_pl_g * mass_scale_inv_cm**2) ?
    # Wait, units of rho is g/cm^3. 
    # Units of Box phi is 1/cm^2 * phi.
    # So phi has units of g/cm (linear mass density)? No.
    
    # Standard Canonical Scalar:
    # Box phi = dV/dphi + beta/M_pl T
    # [phi] = Energy (Mass). [Box] = Mass^2. [T] = Mass^4. [M_pl] = Mass.
    # Mass^3 = Mass^4 / Mass. Correct.
    
    # In CGS, we need to be careful with hbar and c.
    # Let's work in mass ratio.
    # phi_env / M_pl = (rho_ism / M_pl^4) / (m_eff / M_pl)^2
    # phi_env / M_pl = rho_ism / (M_pl^2 * m_eff^2)
    
    # rho_ism = 1.67e-24 g/cm^3
    # M_pl_g = 4.34e-6 g
    # But M_pl in the density term is Mass/Volume?
    # In QFT, rho is Energy Density ~ g/cm^3 * c^2.
    rho_energy = rho_ism * c**2
    
    # m_eff^2 needs to be in 1/cm^2 units (inverse length squared)
    # m_eff_sq = (1/R)^2
    
    # The equation: (Nabla^2 - m^2) phi = rho / M
    # phi ~ rho / (m^2 M)
    # Units: (Energy/L^3) / (1/L^2 * Energy) = 1/L.
    # Phi has units of 1/Length.
    # To make it dimensionless (relative to Planck), we multiply by 1/M_pl? No.
    
    # Thin shell factor:
    # epsilon = phi_env / (6 * beta * M_pl * Phi_grav)
    # Phi_grav is dimensionless (GM/r). M_pl is Mass (Energy).
    # We need phi_env to be Energy.
    # The canonical phi has dimensions of Mass (Energy).
    
    # phi_env = rho_energy / (M_pl_g * c^2 * m_eff_sq) 
    # Wait. M_pl in the coupling is usually Reduced Planck Mass in Energy units.
    # Let's trust the ratio:
    # phi / M_pl ~ (rho / M_pl^4) / (m / M_pl)^2
    # This is dimensionless ratio.
    
    # Let's do it in Planck Units (G=c=hbar=1).
    # rho_ism_planck = 10^-120 (Cosmological Constant scale roughly)
    # R_gal_planck = 10^40 (1 kpc)
    # m_eff_planck = 10^-40
    
    # phi_env_planck = rho_planck / (m_eff_planck^2)
    # phi_env_planck ~ 10^-120 / 10^-80 = 10^-40
    
    # Phi_grav_sun = 10^-6
    # epsilon = 10^-40 / (10^-6) = 10^-34
    
    # This looks extremely screened!
    # But rho_ism is NOT 10^-120 (that's dark energy).
    # rho_ism is Baryons. 1 proton / cm^3.
    # rho_crit ~ 10^-29 g/cm^3.
    # rho_ism ~ 10^5 * rho_crit.
    # So rho_ism_planck ~ 10^-115.
    
    # If R ~ 1 kpc (10^21 cm). Planck length ~ 10^-33 cm.
    # R_planck ~ 10^54.
    # m_eff_planck ~ 10^-54.
    
    # phi_env_planck = 10^-115 / (10^-54)^2 = 10^-115 / 10^-108 = 10^-7.
    
    # epsilon = 10^-7 / 10^-6 = 0.1
    
    # This is the danger zone! 
    # If epsilon ~ 0.1, it is NOT screened well.
    # We need epsilon < 10^-7 for Cassini (gamma - 1 < 2e-5).
    # Actually thin shell condition says if epsilon < 1, we have a shell.
    # But the suppression factor is epsilon.
    
    # Let's calculate precisely.
    
    # 1. Convert rho_ism to Planck units (mass^4)
    # rho_cgs = 1.67e-24 g/cm^3
    # Planck Density = M_pl / L_pl^3 = 2e-5 g / (1.6e-33)^3 ~ 10^94 g/cm^3
    # rho_planck = 1.67e-24 / 5e93 = 3e-118.
    
    rho_planck = 3e-118
    
    # 2. Convert m_eff to Planck units (mass)
    # R = 3e21 cm. L_pl = 1.6e-33 cm.
    # R_planck = 2e54.
    # m_eff_planck = 1 / 2e54 = 5e-55.
    
    m_eff_planck = 5e-55
    
    # 3. Calculate phi_env (Planck units)
    phi_env_planck = rho_planck / (m_eff_planck**2)
    # 3e-118 / 2.5e-109 = 1e-9.
    
    print(f"Phi_env (Planck):      {phi_env_planck:.2e}")
    
    # 4. Thin Shell Factor
    # epsilon = phi_env / (6 * beta * Phi_sun)
    # Phi_sun = 2e-6
    epsilon = phi_env_planck / (6 * beta_m * Phi_sun)
    
    print(f"Thin Shell Factor:     {epsilon:.2e}")
    
    if epsilon < 1e-6:
        print("PASS: Solar System is well-screened.")
    elif epsilon < 0.1:
        print("WARNING: Marginal screening. Needs tuning.")
    else:
        print("FAIL: Fifth force is too strong in Solar System.")

if __name__ == "__main__":
    check_screening()
