import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Constants
c = 299792.458 # km/s
G = 4.30e-6    # kpc km^2/s^2 M_sun^-1
H0 = 70.0      # km/s/Mpc

# Parameters for Lens (Massive Elliptical Galaxy)
sigma_v = 300.0 # km/s
M_vir = 2e13    # Solar Masses
c_conc = 6.0    # Concentration
R_vir = 400.0   # kpc
Rs_nfw = R_vir / c_conc

# Machian Parameters
# Scalar field phi ~ A * ln(1 + r/Rs)
# Refractive index n ~ 1 + K * ln(1 + r/Rs)
# This yields a force F ~ 1/(r(Rs+r)) which mimics Isothermal behavior (1/r) at large radii
# and avoids singularity at r=0.
R_scalar = 2.0 # kpc (Baryonic scale)

# Matching Point (Einstein Radius)
R_match = 8.0 # kpc

def nfw_potential_derivative(r):
    # dPhi/dr = G M(<r) / r^2
    if r < 0.01: return 0
    x = r / Rs_nfw
    f_x = np.log(1+x) - x/(1+x)
    f_c = np.log(1+c_conc) - c_conc/(1+c_conc)
    M_enc = M_vir * f_x / f_c
    return G * M_enc / r**2

def machian_refractive_gradient(r):
    # n = 1 + K * ln(1 + r/R_s) 
    # dn/dr = K / (R_s + r)
    
    # Match Force at R_match
    f_nfw_match = nfw_potential_derivative(R_match)
    
    # We want Gradient ~ 2 * Force_NFW (GR factor 2 included in index)
    # K / (R_scalar + R_match) = 2 * F_nfw
    K = 2 * f_nfw_match * (R_scalar + R_match)
    return K / (R_scalar + r)

def deflection_integrand_nfw(z, b):
    r = np.sqrt(b**2 + z**2)
    return 2 * nfw_potential_derivative(r) * (b/r)

def deflection_integrand_machian(z, b):
    r = np.sqrt(b**2 + z**2)
    return machian_refractive_gradient(r) * (b/r)

def potential_integrand_nfw(z, b):
    # Shapiro ~ Integral 2 * Phi dz
    r = np.sqrt(b**2 + z**2)
    x = r / Rs_nfw
    if x < 1e-6: return -2 * (G * M_vir / Rs_nfw)
    phi = - (G * M_vir / Rs_nfw) * (np.log(1+x)/x)
    return 2 * phi

def potential_integrand_machian(z, b):
    # Shapiro ~ Integral (n-1) dz
    # Primitive of dn/dr = K/(R+r) is K * ln(R+r).
    # This is consistent with previous runs.
    # Note: The absolute value depends on the constant of integration (gauge).
    # But we match the *slope* (deflection) at Re.
    # We also need to anchor the potential levels if we compare absolute delays?
    # Actually, lensing measures *time delay differences* between images.
    # So we care about Delay(b1) - Delay(b2).
    # The constant offset doesn't matter for observables (cancelled in subtraction).
    # However, to plot "Time Delay vs Impact Parameter", we usually define some zero point.
    # Here we match the *values* at R_match just to overlay the curves for visual comparison of shape.
    
    r = np.sqrt(b**2 + z**2)
    f_nfw_match = nfw_potential_derivative(R_match)
    K = 2 * f_nfw_match * (R_scalar + R_match)
    return - K * np.log(R_scalar + r)

# --- GENERATE PLOT ---
impact_params = np.linspace(0.5, 30, 60) 
delays_nfw = []
delays_mach = []

Z_limit = 1000.0 

print(f"Simulating Galaxy Lens: M={M_vir:.1e}, R_match={R_match} kpc")

raw_nfw = []
raw_mach = []

for b in impact_params:
    res_nfw, _ = quad(potential_integrand_nfw, 0, Z_limit, args=(b))
    res_mach, _ = quad(potential_integrand_machian, 0, Z_limit, args=(b))
    raw_nfw.append(res_nfw)
    raw_mach.append(res_mach)

# Calibrate offset to match at R_match
idx_match = np.argmin(np.abs(impact_params - R_match))
offset = raw_nfw[idx_match] - raw_mach[idx_match]

final_mach = np.array(raw_mach) + offset
final_nfw = np.array(raw_nfw)

# Conversion
conv_factor_sec = 2 * (3.086e19 / 1000.0) / (299792.458**3) 
conv_days = conv_factor_sec / 86400.0

final_days_nfw = final_nfw * conv_days
final_days_mach = final_mach * conv_days
diff_days = final_days_nfw - final_days_mach

# Values for paper - Fiducial Pair
b1 = 5.0
b2 = 8.0

idx_b1 = np.argmin(np.abs(impact_params - b1))
idx_b2 = np.argmin(np.abs(impact_params - b2))

dt_nfw_pair = abs(final_days_nfw[idx_b1] - final_days_nfw[idx_b2])
dt_mach_pair = abs(final_days_mach[idx_b1] - final_days_mach[idx_b2])

print(f"Fiducial Pair (b={b1} vs b={b2} kpc):")
print(f"  NFW Delta-t: {dt_nfw_pair:.2f} days")
print(f"  Machian Delta-t: {dt_mach_pair:.2f} days")
print(f"  Difference: {abs(dt_nfw_pair - dt_mach_pair):.2f} days")
print(f"  Percentage Deficit: {100 * (dt_nfw_pair - dt_mach_pair)/dt_nfw_pair:.1f}%")

idx_core = np.argmin(np.abs(impact_params - 1.0))
print(f"Anomaly at b=1 kpc: {diff_days[idx_core]:.2f} days")

plt.figure(figsize=(10, 6))
plt.plot(impact_params, final_days_nfw, 'r--', label='Standard GR (NFW Halo)')
plt.plot(impact_params, final_days_mach, 'c-', label='Machian Scalar (Refractive)')
plt.axvline(R_match, color='k', linestyle=':', alpha=0.5, label='Einstein Radius')
plt.xlabel("Impact Parameter (kpc)")
plt.ylabel("Relative Shapiro Delay (Days)")
plt.title(f"Shapiro Anomaly: Massive Elliptical ($M_{{vir}} = 2\times 10^{{13}} M_{{\odot}}$)")
plt.legend()
plt.grid(True, alpha=0.3)

# Inset
ax2 = plt.axes([0.6, 0.2, 0.25, 0.25])
ax2.plot(impact_params, diff_days, 'k-')
ax2.set_title("Anomaly (NFW - Machian)")
ax2.set_xlabel("b (kpc)")
ax2.set_ylabel("Diff (Days)")
ax2.grid(True)

plt.savefig('papers/figures/fig7_shapiro_anomaly.png')
print("Plot generated.")