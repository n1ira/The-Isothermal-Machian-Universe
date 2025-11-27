import numpy as np
from scipy.integrate import quad

# Constants
H0 = 70.0  # km/s/Mpc
c = 299792.458  # km/s
Omega_m = 0.3
Omega_L = 0.7

# Conversion factors
# 1 Mpc = 3.086e19 km
# 1 Gyr = 3.154e16 s
# H0 in 1/Gyr
H0_inv_Gyr = 977.8 / H0 # 1/H0 in Gyr

def get_mass_evolution_factor(z):
    """
    Returns the relative mass m(z)/m0 based on the Isothermal Machian Universe postulate.
    m(z) = m0 / (1 + z)
    """
    if z <= -0.99:
        return float('inf')
    return 1.0 / (1.0 + z)

def hubble_parameter(z):
    """
    Standard LCDM H(z)/H0 for the integral.
    """
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_L)

def lookback_time_machian(z):
    """
    Calculate Lookback Time in the Isothermal Machian Universe.
    t(z) = (1/H0) * Integral[ dz' / E(z') ]
    
    Note: Unlike Standard LCDM, there is NO (1+z) denominator.
    This represents "Machian Time Dilation" where clocks ticked faster in the past.
    """
    def integrand(z_prime):
        # Singularity check
        if z_prime <= -1.0:
            return float('inf')
        return 1.0 / hubble_parameter(z_prime)
    
    # If z is close to -1, we might hit the singularity
    if z <= -0.99:
        return float('inf')

    result, error = quad(integrand, 0, z)
    return result * H0_inv_Gyr

def time_to_singularity():
    """
    Calculates the time remaining until the 'Blue Screen of Death' (z = -1).
    We integrate from z=0 to z=-0.999.
    Since z is negative, dt will be negative (future). We return absolute value.
    """
    # Integrate from 0 to -1
    # dt = dz / H(z)
    # H(z) is positive. dz is negative. Result is negative.
    
    def integrand(z_prime):
        return 1.0 / hubble_parameter(z_prime)
        
    result, error = quad(integrand, 0, -0.999)
    return abs(result * H0_inv_Gyr)

def lookback_time_lcdm(z):
    """
    Standard LCDM Lookback Time for comparison.
    t(z) = (1/H0) * Integral[ dz' / ((1+z') * E(z')) ]
    """
    def integrand(z_prime):
        return 1.0 / ((1 + z_prime) * hubble_parameter(z_prime))
    
    result, error = quad(integrand, 0, z)
    return result * H0_inv_Gyr

def comoving_distance(z):
    """
    Calculate Comoving Distance (Static Euclidean Distance).
    d(z) = c * t_machian(z)
    """
    t_gyr = lookback_time_machian(z)
    # c * t gives distance. 
    # If t is in Gyr, we need c in Mpc/Gyr?
    # Let's stick to Mpc.
    # d_H = c/H0 = 3000 * h^-1 Mpc approx 4285 Mpc for h=0.7
    d_H = c / H0 # Mpc * s/km * km/s = Mpc
    
    # The integral part is dimensionless (if we ignore H0 outside).
    # t(z) returns Gyr.
    # d = c * t
    # c = 306.6 Mpc/Gyr
    c_mpc_gyr = 306.601
    return c_mpc_gyr * t_gyr

def luminosity_distance_machian(z, beta=1.0):
    """
    Luminosity Distance in Machian Universe.
    d_L = d_C * (1+z) (Standard result, derived differently)
    
    Derivation:
    Flux F = L_obs / (4*pi*d^2)
    L_obs = L_int * (1+z)^-beta (Intrinsic Dimming)
    But we also have photon redshift energy loss (1+z) and time dilation (1+z).
    """
    d_c = comoving_distance(z)
    # Standard LCDM: d_L = d_C * (1+z)
    # Machian: If L_int scales as (1+z)^-1, does it match?
    # Let's return the effective d_L for plotting Hubble Diagram.
    return d_c * (1 + z)

def hubble_parameter_machian(z):
    """
    In the Isothermal Machian Universe, the 'expansion' is actually mass evolution.
    If m(t) = m0 * e^(-H0*t), then the fractional rate of change is constant.
    H_machian(z) = H0 (constant).
    
    However, to resolve the tension, we might propose that H_eff evolves differently.
    For this visualization, we show the 'Effective H(z)' if one wrongly assumes expansion.
    """
    # If the universe is static, H_eff should be 0? 
    # No, we observe redshift.
    # Let's return a constant H0 for the 'True' Machian parameter.
    return 1.0
