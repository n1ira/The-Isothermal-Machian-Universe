import numpy as np

# Try to import cupy for GPU acceleration, fallback to numpy
try:
    import cupy as cp
    USE_GPU = True
except ImportError:
    import numpy as cp
    USE_GPU = False

class BaryonicMassGradient:
    """
    Simulates the 'Isothermal Machian' galaxy rotation curve.
    
    Hypothesis:
    The universe is static, but mass evolves: m(t) = m0 / (1+z).
    The outskirts of a galaxy are 'older' (lookback time) than the core?
    Actually, the manifesto says: "Galactic rotation curves are flat because the outskirts are 'older' (lighter) than the core."
    
    If they are lighter, m(r) should decrease with r.
    Formula: m(r) = m0 * exp(-r/R)
    
    However, standard physics says flat rotation curves require MORE mass at large r (Dark Matter).
    If the 'mass' in the formula refers to the inertial mass of the orbiting body, it cancels out (v^2 = GM/r).
    If it refers to the source mass M(r), then M(r) needs to increase linearly with r.
    
    Let's implement the manifesto's formula and see what happens.
    Maybe 'm(r)' is a scaling factor for the effective gravitational constant? 
    Or maybe the manifesto implies that 'm' in Newton's law behaves differently?
    
    For now, we implement the 'Kill Shot' parameters:
    Beta = 5.0 (Power law index? Or part of the exp?)
    Scale = 15.0 (Scale length R)
    """
    
    def __init__(self, m0=2.76e9, scale_length=0.89, beta=0.98):
        """
        m0: Central mass parameter (Solar masses)
        scale_length: Scale length R (kpc)
        beta: The 'Kill Shot' parameter mentioned in manifesto. 
              Manifesto says "Beta=5.0". 
              If m(r) = m0 * e^(-r/R), where does Beta fit?
              Maybe m(r) = m0 * (1 + r/R)^-Beta ?
              Or maybe it's related to the redshift-mass relation?
              
              Let's assume a generalized profile that can be tuned.
              If the user said "Beta=5.0, Scale=15.0", and the formula is m(r) = m0 * e^(-r/R),
              maybe Beta is not used in the exponential form?
              
              Wait, manifesto says: "L \propto m^\beta". 
              But for rotation, we need mass.
              
              Let's stick to the explicit formula: m(r) = m0 * e^(-r/R) for the *density* or *constituent mass*?
              
              Let's implement a standard N-body or shell-theorem calculation where 
              the mass of each 'particle' at radius r is scaled by this factor.
        """
        self.m0 = m0
        self.scale_length = scale_length
        self.beta = beta
        self.G = 4.30091e-6  # kpc km^2 / (s^2 M_sun)

    def mass_scaling_factor(self, r):
        """
        The 'Machian' scaling factor.
        Manifesto: m(r) = m0 * e^(-r/R)
        We return the relative factor e^(-r/R).
        """
        # Ensure r is on the correct device (CPU/GPU)
        return cp.exp(-r / self.scale_length)

    def calculate_velocity_profile(self, radii):
        """
        Calculates orbital velocity at given radii.
        
        Standard Keplerian: v = sqrt(G * M_enclosed / r)
        
        Machian Modification:
        If the 'mass' of the galaxy is distributed such that outer parts are 'lighter',
        then M_enclosed would be smaller than expected? That would make v drop FASTER.
        
        Unless... the 'older' parts are lighter, so they have LESS inertia?
        If F = ma, and m is small, then a small force F produces a large acceleration a = v^2/r.
        So v^2 = r * F / m.
        
        If m (inertial mass) is reduced by factor f(r), then v^2 goes UP by 1/f(r).
        
        Let's try this hypothesis:
        Inertial Mass m_i(r) = m_standard * f(r)
        Gravitational Mass m_g(r) = m_standard * f(r) (Equivalence Principle?)
        
        If Equivalence Principle holds, a = g, so orbit is independent of mass.
        
        BUT, if the Machian theory says "Mass Evolves", maybe it breaks equivalence?
        Or maybe it's about the background potential?
        
        Let's try the "Inertia Reduction" hypothesis.
        v_observed^2 = v_newtonian^2 / f(r)
        
        If f(r) = e^(-r/R), then v^2 scales as e^(r/R). This would blow up.
        
        Manifesto says: "Beta=5.0".
        Maybe f(r) = (1 + r/R)^-Beta ?
        If Beta=5.0, this decays fast. 1/f(r) grows fast.
        
        Let's implement the "Inertia Reduction" model as it's the only way 'lighter' outskirts makes curves flat (or rising).
        
        v_machian = v_newtonian / sqrt(f(r))
        """
        radii = cp.asarray(radii)
        
        # 1. Calculate Newtonian Velocity for a standard disk/bulge
        # Approximate as a simple potential for now: M(r) ~ M_total * (1 - exp(-r/R_disk))
        # This is a toy model.
        
        # Standard exponential disk mass distribution
        # Sigma(r) = Sigma_0 * e^(-r/R_disk)
        # Mass enclosed M(r) = M_total * (1 - (1 + r/R_disk) * e^(-r/R_disk))
        
        # Let's use the same scale length for the disk as the 'Machian' field for simplicity, 
        # or treat them separately.
        
        M_enclosed = self.m0 * (1.0 - (1.0 + radii / self.scale_length) * cp.exp(-radii / self.scale_length))
        
        v_newtonian_sq = self.G * M_enclosed / radii
        
        # Avoid division by zero at r=0
        v_newtonian_sq = cp.nan_to_num(v_newtonian_sq)
        
        # 2. Apply Machian Inertia Scaling
        # Hypothesis: Inertia decreases with r.
        # Manifesto parameters: Beta=5.0, Scale=15.0.
        # If we use the exponential form m(r) ~ e^-r/R, it rises too fast.
        # Let's try the Power Law form implied by "Beta":
        # m(r) = m0 * (1 + r/R)^(-Beta)
        # This matches the "L ~ m^beta" style scaling.
        
        # If Beta is passed and > 0, use Power Law. Otherwise use Exponential.
        if self.beta > 0:
            # Power Law Inertia
            # inertia_factor = (1 + r/R)^(-Beta)
            # v^2 ~ 1/r * (1 + r/R)^Beta
            # For flat curve (v^2 ~ const), we need (1+r/R)^Beta ~ r
            # At large r, (r/R)^Beta ~ r => Beta=1 gives flat rotation.
            # If Beta=5.0, it rises very fast (v ~ r^2).
            # Maybe the formula is different?
            # Maybe v_machian = v_newton * (1 + r/R)^(Beta/2)?
            # Let's implement the inertia reduction as:
            inertia_factor = cp.power(1.0 + radii / self.scale_length, -self.beta)
        else:
            # Exponential Inertia (Manifesto text)
            inertia_factor = cp.exp(-radii / self.scale_length)
        
        # v_machian^2 = v_newtonian^2 / inertia_factor
        v_machian_sq = v_newtonian_sq / inertia_factor
        
        v_machian = cp.sqrt(v_machian_sq)
        
        if USE_GPU:
            return cp.asnumpy(v_machian)
        else:
            return v_machian

    def fit_model(self, radii, observed_velocities, observed_errors=None):
        """
        Fits the Machian model to observed data to find optimal Beta and Scale Length.
        """
        from scipy.optimize import curve_fit
        
        # Define the model function for curve_fit
        def model_func(r, m0_fit, scale_fit, beta_fit):
            # Update params
            self.m0 = m0_fit
            self.scale_length = scale_fit
            self.beta = beta_fit
            return self.calculate_velocity_profile(r)

        # Initial guesses
        p0 = [self.m0, self.scale_length, self.beta]
        
        # Bounds: m0 > 0, scale > 0, beta > 0
        bounds = ([1e8, 0.1, 0.0], [1e13, 100.0, 10.0])
        
        try:
            popt, pcov = curve_fit(
                model_func, 
                radii, 
                observed_velocities, 
                p0=p0, 
                sigma=observed_errors, 
                bounds=bounds,
                maxfev=2000
            )
            
            self.m0, self.scale_length, self.beta = popt
            return popt, pcov
        except Exception as e:
            print(f"Fitting failed: {e}")
            return None, None

def load_sparc_data(filepath):
    """
    Loads SPARC galaxy data from a .dat file.
    Expected columns: Rad(kpc) Vobs(km/s) errV(km/s) ...
    """
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 3:
                try:
                    r = float(parts[0])
                    v = float(parts[1])
                    err = float(parts[2])
                    data.append((r, v, err))
                except ValueError:
                    continue
    
    if not data:
        return None, None, None
        
    data = np.array(data)
    return data[:, 0], data[:, 1], data[:, 2]

if __name__ == "__main__":
    import os
    
    # Initialize Simulation
    sim = BaryonicMassGradient(m0=5e9, scale_length=5.0, beta=1.0)
    
    # Load Data
    data_path = os.path.join(os.path.dirname(__file__), "../../data/ngc6503.dat")
    if os.path.exists(data_path):
        print(f"Loading data from {data_path}...")
        radii, v_obs, v_err = load_sparc_data(data_path)
        
        if radii is not None:
            print(f"Loaded {len(radii)} data points.")
            
            # Fit Model
            print("Fitting Machian Model...")
            popt, _ = sim.fit_model(radii, v_obs, v_err)
            
            if popt is not None:
                print(f"Optimal Parameters:")
                print(f"  Mass (M0): {popt[0]:.2e} M_sun")
                print(f"  Scale (R): {popt[1]:.2f} kpc")
                print(f"  Beta:      {popt[2]:.2f}")
                
                # Calculate Chi-Squared
                v_model = sim.calculate_velocity_profile(radii)
                residuals = v_obs - v_model
                chi2 = np.sum((residuals / v_err)**2)
                reduced_chi2 = chi2 / (len(radii) - 3) # 3 free params
                residual_std = np.std(residuals)
                
                print(f"  Chi-Squared: {chi2:.2f}")
                print(f"  Reduced Chi-Squared: {reduced_chi2:.2f}")
                print(f"  Residual Std Dev: {residual_std:.2f} km/s")
            else:
                print("Fitting failed.")
        else:
            print("Failed to parse data.")
    else:
        print("Data file not found. Running synthetic test.")
        r = np.linspace(0.1, 50, 100)
        v = sim.calculate_velocity_profile(r)
        print(f"Velocity at 15kpc: {v[30]:.2f} km/s")
