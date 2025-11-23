"""
EXPERIMENT 12: LENSING COUPLING SWEEP
-------------------------------------
Goal: Find a photon coupling L_int that satisfies BOTH Rotation Curves and Lensing.

Problem: 
- Rotation requires phi ~ r^1.0
- Gradient Coupling (grad phi)^2 F^2 requires phi ~ r^1.5 (to get n ~ ln r)

Hypothesis:
- Try Direct Coupling: L_int ~ phi^k * F^2
- If n(r) ~ 1 + phi^k
- We need n ~ ln(r).
- If phi ~ r, then k must be such that r^k ~ ln(r). Impossible for power law.
- But maybe phi isn't exactly linear?

Let's test different coupling forms f(phi) where n = 1 + f(phi).
We need dn/dr ~ 1/r (for constant deflection).
dn/dr = f'(phi) * phi'.
From Rotation, phi' ~ 1 (since phi ~ r).
So we need f'(phi) ~ 1/r ~ 1/phi.
Integration gives f(phi) ~ ln(phi).

PROPOSED FIX:
Use a Dilaton-like coupling L_int ~ ln(phi) * F^2.
Or simply L_int ~ phi^0 * F^2 ?? No.

If L_int ~ ln(phi) F^2:
n(r) = 1 + lambda * ln(phi).
If phi ~ r (from rotation), then n(r) ~ ln(r).
dn/dr ~ 1/r.
Deflection ~ Integral (1/r) dz ~ Constant.
MATCH!

Verification:
1. Does L_int ~ ln(phi) F^2 make sense?
   - Dimensionless field? phi is mass dimension 1?
   - Standard Dilaton is e^(-phi).
   - If phi is "Mass", then ln(phi) is dimensionless?
   - Or perhaps V(phi) is different?

Let's simulate the "Log-Coupling" model.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def check_coupling_model():
    print("Testing 'Logarithmic Coupling' Hypothesis...")
    
    # 1. Scalar Profile from Rotation Curves
    # phi(r) = phi0 * (1 + r/R)
    # Force ~ phi'/phi ~ 1/(R+r) ~ 1/r at large radii. (Correct)
    
    R = 1.0
    def phi(r): return 1.0 + r/R
    def dphi_dr(r): return 1.0/R
    
    # 2. Proposed Coupling: n(r) = 1 + lambda * ln(phi)
    lam = 0.1
    
    def n_log(r):
        return 1.0 + lam * np.log(phi(r))
        
    def dn_dr_log(r):
        # dn/dr = lam * (1/phi) * phi'
        # = lam * (1 / (1+r)) * (1) ~ 1/r
        return lam / phi(r) * dphi_dr(r)
    
    # 3. Compute Deflection Angle
    # Theta = Integral (grad_perp n) dz
    # grad_perp n = (b/r) * dn/dr
    
    b_vals = np.linspace(1, 20, 20)
    theta_vals = []
    
    print(f"{'b':<5} | {'Theta':<10}")
    print("-" * 20)
    
    for b in b_vals:
        def integrand(z):
            r = np.sqrt(b**2 + z**2)
            grad_n = (b/r) * dn_dr_log(r)
            return grad_n
            
        theta, _ = quad(integrand, 0, 1000.0)
        theta *= 2
        theta_vals.append(theta)
        print(f"{b:<5.1f} | {theta:<10.4f}")
        
    # Check flatness
    # If theta is constant, it mimics SIS (Dark Matter).
    
    theta_mean = np.mean(theta_vals[5:]) # average outer values
    theta_std = np.std(theta_vals[5:])
    flatness = theta_std / theta_mean
    
    print("-" * 20)
    print(f"Flatness Variation: {flatness*100:.2f}%")
    
    if flatness < 0.05:
        print(">>> SUCCESS: Log-Coupling produces Flat Lensing Profile.")
    else:
        print(">>> FAIL: Lensing profile is not flat.")

if __name__ == "__main__":
    check_coupling_model()
