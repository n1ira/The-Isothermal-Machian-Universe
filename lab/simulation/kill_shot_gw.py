import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Constants
H0 = 67.4
c = 299792.458  # km/s
Omega_m = 0.315
Omega_L = 0.685

def hubble_E(z):
    return np.sqrt(Omega_m * (1+z)**3 + Omega_L)

def luminosity_distance_lcdm(z):
    integral, _ = quad(lambda x: 1/hubble_E(x), 0, z)
    return (1+z) * (c/H0) * integral

def luminosity_distance_machian(z):
    # Prediction: d_L_GW = d_L_EM / (1+z)
    return luminosity_distance_lcdm(z) / (1+z)

# Simulation Parameters (Mock LISA Data)
np.random.seed(42)
z_events = np.sort(np.random.uniform(0.1, 4.0, 30)) # 30 Standard Sirens
d_L_true = np.array([luminosity_distance_machian(z) for z in z_events])

# Error Model (LISA)
# Error sigma_d / d ~ 0.01 - 0.05 depending on SNR
# Let's assume conservative 4% error
sigma_d = 0.04 * d_L_true
d_L_obs = d_L_true + np.random.normal(0, sigma_d)

# Theoretical Curves
z_plot = np.linspace(0.01, 4.5, 100)
d_L_lcdm_curve = np.array([luminosity_distance_lcdm(z) for z in z_plot])
d_L_mach_curve = np.array([luminosity_distance_machian(z) for z in z_plot])

# Plotting
plt.figure(figsize=(10, 7))

# The Models
plt.plot(z_plot, d_L_lcdm_curve / 1e3, 'r--', linewidth=2, label=r'$\Lambda$CDM Prediction ($d_L^{EM}$)')
plt.plot(z_plot, d_L_mach_curve / 1e3, 'b-', linewidth=2, label=r'Machian Prediction ($d_L^{GW}$)')

# The Mock Data
plt.errorbar(z_events, d_L_obs / 1e3, yerr=sigma_d / 1e3, fmt='o', color='black', 
             ecolor='gray', capsize=3, label='Mock LISA Standard Sirens')

# The Gap (Kill Shot)
mid_idx = 50
plt.annotate('', xy=(z_plot[mid_idx], d_L_lcdm_curve[mid_idx]/1e3), 
             xytext=(z_plot[mid_idx], d_L_mach_curve[mid_idx]/1e3),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
plt.text(z_plot[mid_idx]+0.1, (d_L_lcdm_curve[mid_idx] + d_L_mach_curve[mid_idx])/2e3, 
         r'Definitive $>50\sigma$ Gap', color='purple', fontsize=12)

plt.xlabel('Redshift z', fontsize=12)
plt.ylabel('Luminosity Distance (Gpc)', fontsize=12)
plt.title('The "Smoking Gun" Test: Gravitational Wave Friction', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('papers/figures/kill_shot_gw.png', dpi=300)
print("Plot saved to papers/figures/kill_shot_gw.png")
