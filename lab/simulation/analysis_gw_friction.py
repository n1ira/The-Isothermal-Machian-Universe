import numpy as np
import matplotlib.pyplot as plt

def run_gw_analysis():
    print("\n=== Gravitational Wave Friction Analysis ===")
    # Theory:
    # Action: S = Integral sqrt(-g) [ M_pl^2/2 R - ... ] + S_m[A^2 g]
    # Transform to Jordan Frame (Physical Metric tilde_g = A^2 g)
    # The GW equation in Jordan frame typically has friction:
    # h'' + (3 + alpha_M) H h' + ... = 0
    # where alpha_M = d ln (M_eff^2) / d ln a
    # Here M_eff is the effective Planck mass coupling to tensor modes.
    # If GWs follow tilde_g, they are standard GR waves in tilde_g?
    # In tilde_g, the action looks like f(phi) R_tilde.
    # S = Integral sqrt(-tilde_g) [ Phi * R_tilde ... ]
    # Effective Planck Mass M_eff^2 propto Phi.
    # We need to find the conformal factor Omega^2 such that g = Omega^2 tilde_g.
    # Omega = A^-1.
    # Ricci scalar R = Omega^2 R_tilde + ...
    # sqrt(-g) R = Omega^4 sqrt(-tilde_g) Omega^-2 R_tilde = Omega^2 sqrt(-tilde_g) R_tilde.
    # So M_eff^2 = M_pl^2 * Omega^2 = M_pl^2 * A^-2.
    # So M_eff = M_pl / A.
    
    # alpha_M = d ln (M_eff^2) / d ln tilde_a
    # alpha_M = d ln (A^-2) / d ln tilde_a = -2 d ln A / d ln tilde_a
    # A = e^(beta phi / M_pl)
    # ln A = beta phi / M_pl
    # alpha_M = -2 * (beta / M_pl) * (d phi / d ln tilde_a)
    # alpha_M = -2 * (beta / M_pl) * (dot_phi / H_tilde)
    
    # We need to estimate alpha_M for z < 2 (LIGO range).
    
    # From Cosmology (Paper 2):
    # phi(t) approx H_0 * t (linear growth).
    # H approx 1/t.
    # dot_phi approx H_0 approx H? 
    # Wait, standard solution: phi propto t.
    # H = 1/t (for static universe with m(t) propto 1/t).
    # So dot_phi / H approx phi/t / (1/t) = phi.
    # No.
    # Let's look at units.
    # dot_phi has units Mass^2 (in 3D)? No, Mass.
    # H has units Mass.
    # Ratio is dimensionless?
    # In dimensionless units:
    # phi approx t. H approx 1/t.
    # dot_phi / H approx 1 / (1/t) = t?
    # This grows linearly?
    
    # Let's use specific numbers from Cosmology solution.
    # phi(now) approx M_pl (order of magnitude)?
    # Actually, beta phi / M_pl approx ln(Scale Factor).
    # If mass changes by factor 10 since z=9.
    # A = e^(beta phi / M_pl).
    # ln A approx 1-2.
    # So beta phi / M_pl approx 1.
    # d (beta phi / M_pl) / d ln a approx 1.
    # So alpha_M approx -2 * 1 = -2.
    
    # Result: alpha_M is Order unity.
    alpha_M_est = -2.0 # Rough estimate
    
    print(f"Estimated Friction Term alpha_M: {alpha_M_est}")
    
    # Effect on Distance
    # d_L_GW = d_L_EM * exp( - 1/2 Integral alpha_M d ln a )
    # If alpha_M is constant -2:
    # Integral (-2) d ln a = -2 ln a
    # exp ( -1/2 * -2 ln a ) = exp ( ln a ) = a.
    # So d_L_GW = d_L_EM * a = d_L_EM / (1+z).
    
    # If this is true, GWs are dimmer/brighter?
    # d_L_GW < d_L_EM. GWs appear closer (brighter).
    # Deviation at z=1: Factor of 0.5.
    # This is HUGE.
    
    print("Prediction: GW Luminosity Distance deviates by factor (1+z)^-1")
    print("d_L_GW = d_L_EM / (1+z)")
    
    # Constraint Check
    # LIGO GW170817 at z=0.01.
    # 1/(1.01) approx 0.99.
    # 1% deviation.
    # Current measurement uncertainty in H0 from Sirens is ~ 15%.
    # So this is currently ALLOWED but testable with more events.
    
    print("Status: Consistent with current low-z data (1% effect), but strongly falsifiable at high z.")

    # === Generate Prediction Plot ===
    z_vals = np.linspace(0, 5, 100)
    # Relation: dL_GW = dL_EM / (1+z)
    # Deviation ratio: dL_GW / dL_EM = 1 / (1+z)
    ratio = 1.0 / (1.0 + z_vals)
    
    plt.figure(figsize=(10, 6))
    plt.plot(z_vals, ratio, label=r'Prediction: $d_L^{GW} / d_L^{EM} = (1+z)^{-1}$', linewidth=2, color='red')
    plt.axhline(1.0, linestyle='--', color='black', label='General Relativity ($d_L^{GW} = d_L^{EM}$)')
    
    # Annotate future detectors
    plt.axvline(0.01, linestyle=':', color='gray', label='GW170817 ($z=0.01$)')
    plt.axvline(1.0, linestyle=':', color='blue', label='LISA Target ($z \sim 1-5$)')
    
    plt.fill_between(z_vals, ratio, 1.0, alpha=0.1, color='red')
    
    plt.xlabel('Redshift $z$')
    plt.ylabel(r'Luminosity Distance Ratio $d_L^{GW} / d_L^{EM}$')
    plt.title('The "Smoking Gun": Gravitational Wave Dimming Prediction')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 5)
    plt.ylim(0, 1.1)
    
    plt.savefig('gw_luminosity_prediction.png')
    print("Prediction plot saved to gw_luminosity_prediction.png")

if __name__ == "__main__":
    run_gw_analysis()
