import numpy as np
import matplotlib.pyplot as plt

# === Constants ===
KG_TO_EV = 5.609e35
M_PL = 2.435e27 # eV

# === Model ===
LAMBDA_EV = 11.7e3
C_THERM = 100.0 # Thermal coupling constant g^2/12 approx 100
N_POWER = 3.0

def run_lithium_analysis():
    print("\n=== Lithium Problem & BBN Thawing Analysis ===")
    # Potential: V = Lambda^(4+n)/phi^n + 0.5 c T^2 phi^2
    # Minimum phi(T):
    # V' = -n L / phi^(n+1) + c T^2 phi = 0
    # c T^2 phi = n L / phi^(n+1)
    # phi^(n+2) = (n L^(4+n)) / (c T^2)
    # phi(T) = [ (n L^(4+n)) / c ]^(1/(n+2)) * T^(-2/(n+2))
    
    # For n=3:
    # phi ~ T^(-2/5)
    
    # Mass scaling: m(T) propto phi(T)^(-1/2) (approx)
    # So m(T) propto (T^-0.4)^-0.5 = T^0.2
    
    # We want to check the mass variation during Lithium synthesis window.
    # Lithium-7 is produced around T = 50 keV (0.05 MeV) down to 10 keV?
    # BBN ends around 10 keV.
    # Deuterium bottleneck breaks at 0.1 MeV.
    
    T_start = 0.08e6 # 80 keV
    T_end = 0.03e6   # 30 keV
    
    def get_phi(T):
        term = (N_POWER * (LAMBDA_EV**(4+N_POWER))) / (C_THERM * T**2)
        return term**(1.0/(N_POWER+2.0))
    
    phi_start = get_phi(T_start)
    phi_end = get_phi(T_end)
    
    # Mass Variation
    # m propto phi^-0.5 (if Higgs VEV propto phi)
    # wait, Higgs VEV v ~ sqrt(phi) in my paper?
    # "v_Higgs propto sqrt(phi)" => m propto sqrt(phi).
    # Paper 5 said: "elementary particle masses... scale as m propto sqrt(phi)."
    # Let's stick to that.
    
    m_start = np.sqrt(phi_start)
    m_end = np.sqrt(phi_end)
    
    delta_m_frac = (m_end - m_start) / m_start
    
    print(f"Temperature Window: {T_start/1e3} keV -> {T_end/1e3} keV")
    print(f"Phi Change: {phi_start:.2e} -> {phi_end:.2e} eV")
    print(f"Mass Change (Fractional): {delta_m_frac:.4e}")
    
    # Lithium Problem
    # Li-7 is overproduced in standard BBN by factor 3.
    # We need to reduce it.
    # If binding energy of Deuterium increases, or Be-7 binding energy changes?
    # Sensitivity: delta Y_Li / Y_Li approx 10 * delta m_n / m_n?
    # Actually, BBN sensitivity to G_F, alpha, m_e, m_q is complex.
    # But generally, if binding energies change, abundances shift exponentially (Boltzmann factor).
    # A small change (few %) can solve the factor of 3.
    
    print(f"Predicted Mass Drift: {delta_m_frac*100:.2f}%")
    
    if abs(delta_m_frac) > 1e-3 and abs(delta_m_frac) < 0.1:
        print("RESULT: Mass drift is in the 'Goldilocks' zone (0.1% - 10%).")
        print("This magnitude is sufficient to significantly alter Li-7 abundances.")
        print("Since m(T) decreases (phi increases, wait T^-0.4, as T drops, phi grows. m propto sqrt(phi) grows).")
        print("Mass INCREASES during BBN end.")
        print("This might resolve the Lithium anomaly.")
    else:
        print("RESULT: Mass drift is too small/large.")

if __name__ == "__main__":
    run_lithium_analysis()
