import numpy as np
from scipy.constants import G, c, parsec, au, year

# === Constants ===
M_sun = 1.989e30 # kg
R_sun = 6.96e8 # m
AU = 1.496e11 # m
M_pl = 2.176e-8 # kg (Planck mass)
# But we usually work in reduced Planck units in cosmology: M_pl_red = sqrt(hbar*c/8piG) = 2.4e18 GeV.
# Let's stick to SI where possible or consistent units.
# In the paper, phi is often dimensionless or scaled.
# Let's use the paper's parameters.

# === Theory Parameters ===
# From Paper 1 (Galaxies): R_gal = 0.89 kpc, beta = 0.98
# From Paper 5 (Unified): lambda_gamma = 1.134 (Photon coupling)
LAMBDA_GAMMA = 1.134

def analysis_ppn_solar_system():
    """
    Analyze PPN Gamma constraint using Chameleon Screening.
    """
    print("=== PPN Analysis: Solar System Constraints ===")
    
    # 1. Define Potentials
    # V_eff(phi) = V(phi) + rho * e^(beta * phi / M_pl)
    # We need the 'beta' coupling to matter.
    # In Paper 1, we found 'beta' (power law index) ~ 1.0.
    # But the coupling in the Lagrangian is m(phi) ~ phi^eps?
    # Paper 5 Eq 1: m(phi) * psi * psi_bar.
    # Paper 1 Eq 7: m(r) = m0 * exp(-r/R).
    # This implies phi(r) varies.
    
    # Screening condition: The scalar field inside the Sun must be frozen.
    # phi_in (inside Sun) vs phi_out (galaxy).
    
    # Let's estimate the Thin Shell Factor (epsilon).
    # epsilon = (phi_out - phi_in) / (6 * beta * M_pl * Phi_N)
    # where Phi_N is Newtonian potential = GM/R.
    
    # Newtonian Potential of Sun at surface:
    Phi_N = G * M_sun / (R_sun * c**2) # Dimensionless
    print(f"Solar Newtonian Potential Phi_N: {Phi_N:.2e}")
    
    # If epsilon < 10^-6, we are safe (Cassini).
    # This requires (phi_out - phi_in) < 10^-6 * Phi_N * ...
    
    # In our model, phi is of order unity (background) or ln(phi) ~ 1.
    # If phi ~ 1 (in Planck units), then delta_phi ~ 1.
    # Phi_N ~ 2e-6.
    # Epsilon ~ 1 / 10^-6 = 10^6 !!! 
    # This implies NO SCREENING unless phi is tiny or coupling is huge.
    
    # CHECK: Paper 5 says "beta function coefficient b0 ~ 400".
    # If the coupling strength beta_matter is large, screening is easier?
    # No, usually large coupling makes the force stronger, but mass m_phi higher?
    # Chameleon Mass: m_eff^2 ~ rho * beta^2 ...
    
    print("Result: Without a specific mechanism to force delta_phi < 10^-12,")
    print("the theory likely violates Solar System bounds (Gamma - 1 ~ O(1)).")
    print("The 'Chameleon' defense requires phi to change by < 10^-15 across the Solar System.")

def analysis_gw_vs_photon():
    """
    Compare Gravitational Lensing for Photons vs Gravitational Waves.
    """
    print("\n=== Multi-Messenger Analysis: GW vs Photon Lensing ===")
    
    # Scenario: Lensing by a Galaxy (Isothermal Halo)
    # Mass M = 10^12 M_sun at distance D_L = 1 Gpc.
    # Impact parameter b = 5 kpc.
    
    # 1. Photon Lensing (Refractive)
    # Deflection alpha_gamma = 4GM/bc^2 (Predicted to match GR)
    # This comes from n(r) = 1 + 2*Phi_DM.
    
    # 2. GW Lensing (Metric Only)
    # GWs follow geodesics of g_uv.
    # In IMU, does the metric g_uv contain the Dark Matter potential?
    # NO. The "Dark Matter" is a scalar field effect on Inertia (matter) and Refraction (light).
    # The actual energy density of the scalar field rho_phi is small (usually).
    # If rho_phi << rho_DM_standard, then the metric curvature is determined ONLY by Baryons.
    
    # Baryon Fraction f_b = 0.16 (approx).
    # So the metric potential Phi_metric ~ f_b * Phi_total_GR.
    
    # Deflection alpha_GW ~ f_b * alpha_gamma.
    
    print(f"Baryon Fraction f_b assumed: 0.16")
    print("Prediction: Photons feel 'Dark Matter' (Refraction). GWs feel only Baryons (Metric).")
    print("Result: GW deflection angle is ~16% of Photon deflection angle.")
    
    # 3. Time Delay Difference (Shapiro)
    # Shapiro delay is proportional to the potential depth.
    # Delta_t_gamma ~ (1 + gamma) * M_total
    # Delta_t_GW    ~ (1 + gamma) * M_baryon
    
    # For a strong lens (quasar/galaxy), the Shapiro delay is days/months.
    # Let's say Delta_t_gamma = 30 days.
    # Delta_t_GW = 0.16 * 30 days = 4.8 days.
    # Arrival Time Difference: ~25 days.
    
    print("Observational Consequence:")
    print("If a GW source (like a merger) is strongly lensed by a galaxy,")
    print("the GWs and the EM counterpart (GRB) would arrive weeks apart.")
    
    # Check GW170817
    # Was it lensed? No, it was in NGC 4993 (local).
    # So this is not ruled out by GW170817 directly (unless it passed through structure).
    # But it is a DEVASTATING prediction for future lensed GW detections.
    
    print("Verdict: This is a definitive 'Smoking Gun' that distinguishes IMU from GR.")

if __name__ == "__main__":
    analysis_ppn_solar_system()
    analysis_gw_vs_photon()
