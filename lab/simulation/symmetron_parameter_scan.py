import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Constants (GeV)
M_PL = 2.435e18  # Reduced Planck Mass
EV_TO_GEV = 1e-9
CM_TO_INV_GEV = 5.06e13 
G_TO_GEV4 = 4.3e-18 # Density conversion roughly? 
# 1 g/cm^3 = 4.3e-18 GeV^4 (Need precise conversion)
# 1 GeV = 1.78e-24 g
# 1 cm^-1 = 1.97e-14 GeV
# 1 g/cm^3 = (1/1.78e-24) GeV / ( (1/1.97e-14)^3 GeV^-3 )
# = 0.56e24 * (1.97e-14)^3 GeV^4
# = 0.56e24 * 7.6e-42 = 4.3e-18 GeV^4. Correct.
DENSITY_CONVERSION = 4.3e-18

# Critical Densities
RHO_SUN = 150.0 * DENSITY_CONVERSION # Core is 150 g/cm3
RHO_EARTH = 5.5 * DENSITY_CONVERSION
RHO_ATMOSPHERE = 1e-3 * DENSITY_CONVERSION
RHO_GALAXY = 1e-24 * DENSITY_CONVERSION # ISM
RHO_VACUUM = 1e-29 * DENSITY_CONVERSION # Critical density of universe

# BBN Density (T ~ 0.1 MeV)
# rho = (pi^2/30) * g * T^4
RHO_BBN = (np.pi**2 / 30) * 3.36 * (0.1e-3)**4 

print(f"Density Thresholds (GeV^4):")
print(f"  Sun:      {RHO_SUN:.2e}")
print(f"  BBN:      {RHO_BBN:.2e}")
print(f"  Earth:    {RHO_EARTH:.2e}")
print(f"  Galaxy:   {RHO_GALAXY:.2e}")

# Scan Parameters
# M range: 10^10 GeV to 10^20 GeV (Planck is 10^18)
M_range = np.logspace(14, 20, 100)

# Range Requirement: 
# Force range L ~ 1 kpc to 10 kpc.
# mu = 1/L. 
# 1 kpc = 3e21 cm = 3e21 * 5e13 GeV^-1 = 1.5e35 GeV^-1
# mu = 1 / 1.5e35 = 6e-36 GeV.
MU_GALACTIC = 6e-36 

print(f"Required Mass mu: {MU_GALACTIC:.2e} GeV")

# Calculate Critical Density for each M
# rho_crit = mu^2 * M^2
rho_crit_curve = (MU_GALACTIC**2) * (M_range**2)

plt.figure(figsize=(10, 6))

# Plot Critical Density vs M
plt.loglog(M_range, rho_crit_curve, label=r'$ho_{crit} = μ^2 M^2$', linewidth=2, color='black')

# Fill Regions
# Region where Symmetry is BROKEN (rho < rho_crit) -> Fifth Force Active
# Region where Symmetry is RESTORED (rho > rho_crit) -> Screened

# We want:
# 1. Sun/Earth/BBN to be ABOVE the line (Screened)
# 2. Galaxy to be BELOW the line (Active)

plt.fill_between(M_range, rho_crit_curve, 1e10, color='blue', alpha=0.1, label='Screened (Symmetry Restored)')
plt.fill_between(M_range, 1e-50, rho_crit_curve, color='red', alpha=0.1, label='Active (Symmetry Broken)')

# Plot Constraint Lines
plt.axhline(y=RHO_SUN, color='orange', linestyle='--', label='Solar Core')
plt.axhline(y=RHO_BBN, color='purple', linestyle='--', label='BBN (0.1 MeV)')
plt.axhline(y=RHO_GALAXY, color='green', linestyle='--', label='Galactic ISM')

# Allowed Zone Vertical Lines
# M_min: Where rho_crit = RHO_GALAXY (Intersection)
# M_max: Where rho_crit = RHO_EARTH (or Atmosphere)
M_min = np.sqrt(RHO_GALAXY) / MU_GALACTIC
M_max = np.sqrt(RHO_EARTH) / MU_GALACTIC

plt.axvline(x=M_min, color='k', linestyle=':', label='Min M (Galaxy Active)')
plt.axvline(x=M_max, color='k', linestyle=':', label='Max M (Earth Screened)')

plt.xlabel(r'Symmetry Breaking Scale $M$ [GeV]')
plt.ylabel(r'Critical Density $ho_{crit}$ [GeV$^4$]')
plt.title('Symmetron Parameter Space Scan')
plt.grid(True, which="both", ls="-")
plt.legend(loc='upper left')
plt.xlim(1e14, 1e20)
plt.ylim(1e-45, 1e0)

# Annotate Planck Mass
plt.axvline(x=M_PL, color='grey', linestyle='-', alpha=0.5)
plt.text(M_PL*1.1, 1e-5, 'Planck Mass', rotation=90, color='grey')

output_path = 'papers/figures/symmetron_parameter_scan.png'
plt.savefig(output_path)
print(f"Figure saved to {output_path}")

print(f"--- RESULTS ---")
print(f"Allowed M Range: {M_min:.2e} GeV to {M_max:.2e} GeV")
print(f"Planck Mass: {M_PL:.2e} GeV")
if M_min < M_PL < M_max:
    print("SUCCESS: Planck Mass is inside the Allowed Window!")
    print("Standard Gravity (M ~ M_pl) naturally satisfies the constraints.")
else:
    print("WARNING: Planck Mass is outside the optimal window.")