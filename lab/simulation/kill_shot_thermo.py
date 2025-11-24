import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Constants
H0 = 67.4  # Planck 2018
H0_inv_Gyr = 977.8 / H0 
Omega_m = 0.315
Omega_L = 0.685

# LCDM Functions
def E_lcdm(z):
    return np.sqrt(Omega_m * (1+z)**3 + Omega_L)

def age_lcdm(z):
    def integrand(z_p):
        return 1.0 / ((1+z_p) * E_lcdm(z_p))
    res, _ = quad(integrand, z, np.inf)
    return res * H0_inv_Gyr

# Machian Functions (Static Frame)
def age_machian(z):
    def integrand(z_p):
        return 1.0 / E_lcdm(z_p)
    res, _ = quad(integrand, z, np.inf)
    return res * H0_inv_Gyr

# Generate Data
z_vals = np.linspace(0, 20, 100)
ages_lcdm = np.array([age_lcdm(z) for z in z_vals])
ages_mach = np.array([age_machian(z) for z in z_vals])

# Plotting
plt.figure(figsize=(10, 7))

# Main Age Plot
plt.plot(z_vals, ages_lcdm, 'r--', label='LambdaCDM Age', linewidth=3)
plt.plot(z_vals, ages_mach, 'c-', label='Machian Age (Static Frame)', linewidth=3)

# The "Impossible" Zone
# JWST observes quenched galaxies at z~10 which need ~300-500 Myr to form
formation_time = 0.5 # Gyr
plt.fill_between(z_vals, 0, formation_time, color='gray', alpha=0.3, label='Forbidden Zone (t < 500 Myr)')

# Annotations
plt.axvline(x=10, color='k', linestyle=':', alpha=0.5)
plt.text(10.5, 15, 'JWST Era', rotation=90, fontsize=12)

# Highlight the Crisis
cross_z = z_vals[np.where(ages_lcdm < formation_time)[0][0]]
plt.plot(cross_z, formation_time, 'ro', markersize=10)
plt.annotate(f'LambdaCDM Crisis\n z > {cross_z:.1f}', xy=(cross_z, formation_time), xytext=(cross_z+2, formation_time+2),
             arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12)

plt.xlabel('Redshift z', fontsize=12)
plt.ylabel('Age of Universe (Gyr)', fontsize=12)
plt.title('The Thermodynamic Break: Solving the Early Galaxy Problem', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.ylim(0, 20)
plt.xlim(0, 20)

plt.savefig('papers/figures/kill_shot_thermo.png', dpi=300)
print("Generated Kill Shot Figure: papers/figures/kill_shot_thermo.png")