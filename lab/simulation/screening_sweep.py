"""
Screening Parameter Sweep
Goal: Find a potential slope 'alpha' that satisfies Solar System screening (epsilon < 2e-5)
while maintaining the Galactic Range R ~ 1 kpc.
"""

import numpy as np

# Constants (Planck Units approx)
Phi_sun = 2e-6

def check_alpha(alpha):
    # Physics Logic:
    # 1. We FIX the range in the ISM to be R = 0.89 kpc (to fit Galaxy).
    #    This sets m_eff(ISM).
    # 2. We change alpha. This changes how m_eff scales with density.
    #    m_eff ~ rho^((alpha+2)/(2*alpha+2)) ?
    #    Let's derive for V(phi) = M^(4+alpha) / phi^alpha
    
    # V' = -alpha * M^(4+alpha) / phi^(alpha+1)
    # Minimum: V' + beta*rho = 0
    # alpha * M... / phi^(a+1) = beta * rho
    # phi_min ~ rho^(-1/(alpha+1))
    
    # V'' = alpha(alpha+1) M... / phi^(alpha+2)
    # m_eff^2 ~ 1 / phi^(alpha+2) ~ rho^((alpha+2)/(alpha+1))
    
    # So m_eff ~ rho^( (alpha+2)/(2*alpha+2) )
    # For alpha=1: rho^(3/4) = rho^0.75. (Matches previous script)
    # For alpha=2: rho^(4/6) = rho^0.66.
    # For alpha=large: rho^0.5.
    
    # 3. Calculate phi_env
    # phi ~ rho^(-1/(alpha+1))
    # Ratio phi_env / phi_sun = (rho_ism / rho_sun)^(-1/(alpha+1))
    # This doesn't help directly with epsilon magnitude, but the absolute value does.
    
    # Absolute value of phi_env:
    # m_eff^2 ~ V'' ~ phi^(-(alpha+2))
    # phi ~ m_eff^(-2/(alpha+2))
    
    # We know m_eff(ISM) is fixed by R = 0.89 kpc.
    # R_planck = 2e54 => m_eff_planck = 5e-55.
    m_eff_planck = 5e-55
    
    # phi_env_planck ~ (m_eff_planck)^(-2/(alpha+2)) * (Constants?)
    # Let's do the scaling relative to alpha=1.
    # At alpha=1, phi_env = 1.2e-9.
    # This was calculated as rho / m^2. 
    # Check consistency: phi ~ m^(-2/(1+2)) = m^-0.66?
    # No, phi ~ rho * m^-2 is only true if rho dominates.
    
    # Let's go back to phi ~ rho^(-1/(alpha+1)).
    # And m^2 ~ rho^((alpha+2)/(alpha+1)).
    # So rho ~ m^(2 * (alpha+1)/(alpha+2)).
    # Then phi ~ [m^(...)]^(-1/(alpha+1)) = m^(-2/(alpha+2)).
    
    # So phi_env(alpha) = C_alpha * (m_eff_ism)^(-2/(alpha+2))
    # The constant C_alpha depends on the coupling scale M (Lambda).
    # But M is fixed by the requirement that m_eff = 1/R at rho_ism.
    
    # This implies phi_env is roughly independent of M if we fix m_eff?
    # Actually, phi * m^2 ~ alpha * (alpha+1) * beta * rho_ism (from V'' phi^2 approx V' phi approx rho).
    # phi_env ~ rho_ism / m_eff_ism^2.
    
    # Wait. This result (phi ~ rho/m^2) is universal for power laws!
    # V' + rho = 0 => rho ~ V'.
    # V'' ~ V'/phi ~ rho/phi.
    # m^2 ~ rho/phi => phi ~ rho/m^2.
    
    # RESULT: phi_env is independent of alpha!
    # phi_env depends only on rho_ism and m_eff_ism (which is 1/R).
    # Since R is fixed by the galaxy rotation curve, phi_env is fixed.
    # phi_env ~ 10^-9 (Planck).
    
    # Epsilon = phi_env / (6 * beta * Phi_sun).
    # Epsilon ~ 10^-4.
    
    # CONCLUSION: Changing the potential slope alpha does NOT help screening 
    # if we are constrained to fit the galaxy at R=0.89 kpc.
    
    # The only way to lower epsilon is to:
    # 1. Increase beta (coupling). Epsilon ~ 1/beta.
    # 2. But phi_env might depend on beta?
    # phi ~ rho / (m^2). Independent of beta?
    # V' + beta*rho = 0. V'' = m^2.
    # If V = phi^-n. V' ~ phi^-(n+1).
    # phi ~ (beta*rho)^(-1/n+1).
    # m^2 ~ phi^-(n+2).
    # If we fix m^2 (to 1/R^2), then phi is fixed.
    # Does beta matter?
    # If m^2 is fixed, we must adjust the parameter Lambda in V.
    # So yes, for a fixed R, phi_env is fixed.
    
    # So Epsilon = Constant / beta.
    # To get epsilon < 10^-6 (factor of 100 improvement),
    # we need beta ~ 100.
    
    return 1.0e-4 / beta_val if alpha == 1 else 0 # Dummy return

def run_sweep():
    print("Running Parameter Optimization...")
    print("Constraint: Must maintain R_galaxy = 0.89 kpc (m_eff fixed).")
    print("Target: Thin Shell Factor epsilon < 2e-5.")
    print("-" * 60)
    
    # Analysis from comments:
    # phi_env is fixed by the force range requirement R.
    # phi_env ~ rho_ism * R^2.
    # epsilon ~ phi_env / (beta * Phi_sun).
    
    # Current epsilon (beta=1) ~ 1e-4.
    # We need epsilon ~ 1e-6 (safe).
    # Solution: Increase coupling beta.
    
    betas = [1, 10, 50, 100, 1000]
    
    print(f"{ 'Beta':<10} | { 'Epsilon':<15} | { 'Status'}")
    print("-" * 45)
    
    for b in betas:
        epsilon = 1.0e-4 / b
        status = "PASS" if epsilon < 2e-5 else "FAIL"
        print(f"{b:<10} | {epsilon:.2e}        | {status}")
        
    print("-" * 45)
    print("\nOptimization Result:")
    print("To satisfy Solar System constraints, we need a Stronger Coupling (beta > 5).")
    print("Increasing beta to ~10-100 ensures robust screening.")
    print("Does this break the Galaxy Fit?")
    print("Galaxy Force: F ~ beta * grad(phi).")
    print("phi ~ (beta * rho)^(-1/2) ...")
    print("Actually, the rotation curve fit found a parameter 'coupling' lambda ~ 10^-6.")
    print("Wait. The galaxy paper says lambda ~ 10^-6.")
    print("But the screening check assumed beta ~ 1.")
    
    # Let's re-evaluate the Galaxy Fit Parameter 'coupling'.
    # In experiment_1_galaxy.py:
    # a_machian = (c^2 / 2phi) * dphi/dr * coupling
    # This 'coupling' is effectively alpha_gal.
    # If alpha_gal ~ 10^-6, then beta is TINY.
    # If beta is tiny, epsilon = phi / (beta * Phi) blows up!
    
    # CONTRADICTION FOUND.
    # The galaxy fit requires a weak force (or small gradients).
    # The screening requires a strong coupling (to make the shell thin).
    
    # Resolution:
    # The 'coupling' in the code might be a prefactor for the potential, not beta.
    # Let's clarify the definition of 'coupling' in Paper 1.
if __name__ == "__main__":
    run_sweep()
