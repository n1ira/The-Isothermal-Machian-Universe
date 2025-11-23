import numpy as np
import matplotlib.pyplot as plt
import os

# Constants (Natural Units: GeV = 1)
M_pl = 2.435e18  # Planck Mass in GeV

# Symmetron Parameters (Tunable)
# We need the transition to happen AFTER BBN (T < 10 keV) but BEFORE CMB (T ~ 0.3 eV) or Galaxy formation?
# Actually, standard Symmetron models transition at z ~ 1 (late time). 
# But for Machian mass evolution, we need it to break 'early enough' to give us the "older universe" effect,
# OR we accept standard history until z~1 and only modify late time?
# The IMU claim is m(t) ~ t^-1. This implies broken symmetry for most of history.
# We just need it RESTORED during BBN (T > 1 MeV).

# Let's set the symmetry breaking scale mu such that phase transition happens at T_crit ~ 1 MeV.
# Critical density rho_crit = mu^2 * M^2.
# Radiation density rho_rad = (pi^2/30) * g_star * T^4.

# If we want T_crit = 0.1 MeV (just after BBN to be safe, or just before?)
# Let's aim for T_crit ~ 50 keV to ensure it's safely constant during Deuterium fusion (0.1 MeV).

T_crit = 50e-6 # 50 keV in GeV
g_star = 3.36
rho_crit = (np.pi**2 / 30) * g_star * T_crit**4

# We have free parameter M (coupling strength). Let's pick M ~ M_pl/1000 for gravitational strength.
M = 1e-3 * M_pl 

# Calculate required mu
# rho_crit = mu^2 * M^2  => mu = sqrt(rho_crit) / M
mu = np.sqrt(rho_crit) / M

lambda_self = 1.0 # Self coupling

print(f"--- Symmetron Parameter Setup ---")
print(f"Transition Temperature T_crit: {T_crit*1e6:.2f} keV")
print(f"Coupling Scale M: {M:.2e} GeV")
print(f"Mass Parameter mu: {mu:.2e} GeV")
print(f"Critical Density: {rho_crit:.2e} GeV^4")

def get_rho(T):
    return (np.pi**2 / 30) * g_star * T**4

def solve_phi_min(rho):
    """
    Finds the minimum of V_eff(phi).
    V_eff = 0.5*(rho/M^2 - mu^2)*phi^2 + 0.25*lambda*phi^4
    """
    effective_mass_sq = (rho / M**2) - mu**2
    
    if effective_mass_sq > 0:
        # Symmetry Restored
        return 0.0
    else:
        # Symmetry Broken
        # dV/dphi = (m_eff^2)*phi + lambda*phi^3 = 0
        # phi^2 = -m_eff^2 / lambda
        return np.sqrt(-effective_mass_sq / lambda_self)

# Simulation Range: 10 MeV down to 1 keV
T_range_gev = np.logspace(np.log10(10e-3), np.log10(1e-6), 1000)
phi_evolution = []
mass_evolution = []

for T in T_range_gev:
    rho = get_rho(T)
    phi = solve_phi_min(rho)
    phi_evolution.append(phi)
    
    # Conformal factor A(phi) = 1 + phi^2 / (2 M^2)
    # Particle mass m ~ A(phi) * m_bare
    A = 1 + (phi**2) / (2 * M**2)
    mass_evolution.append(A)

phi_evolution = np.array(phi_evolution)
mass_evolution = np.array(mass_evolution)

# Analyze drift during BBN window (0.8 MeV to 0.01 MeV)
bbn_indices = np.where((T_range_gev < 0.8e-3) & (T_range_gev > 0.01e-3))
mass_bbn = mass_evolution[bbn_indices]
if len(mass_bbn) > 0:
    drift = (np.max(mass_bbn) - np.min(mass_bbn)) / np.mean(mass_bbn)
else:
    drift = 0

print(f"--- Simulation Results ---")
print(f"Mass Drift during BBN window: {drift:.2e}")

# Plot
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(T_range_gev * 1e3, phi_evolution, label='Scalar Field VEV')
plt.xscale('log')
plt.gca().invert_xaxis()
plt.ylabel(r'$\phi$ [GeV]')
plt.title('Symmetron Phase Transition')
plt.axvline(x=T_crit*1e3, color='r', linestyle='--', label='T_crit')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(T_range_gev * 1e3, mass_evolution, color='orange', label='Conformal Factor A(phi)')
plt.xscale('log')
plt.gca().invert_xaxis()
plt.xlabel('Temperature [MeV]')
plt.ylabel(r'$m(T) / m_0$')
plt.axvline(x=T_crit*1e3, color='r', linestyle='--')
plt.legend()

output_path = 'papers/figures/symmetron_bbn_check.png'
plt.savefig(output_path)
print(f"Figure saved to {output_path}")
