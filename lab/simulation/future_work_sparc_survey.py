import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

# Constants
G_GRAV = 4.30091e-6  # kpc km^2 / (s^2 M_sun)

class GalaxySurveySimulator:
    def __init__(self, n_galaxies=20):
        self.n_galaxies = n_galaxies
        self.galaxies = []
        
    def generate_sample(self):
        """Generate a sample of N galaxies with realistic properties."""
        np.random.seed(42) # Reproducibility
        
        for i in range(self.n_galaxies):
            # 1. Baryonic Mass (M_star + M_gas)
            # Range: 10^8 to 10^11 M_sun
            mass_log = np.random.uniform(8.0, 11.0)
            M_b = 10**mass_log
            
            # 2. Disk Scale Length R_d
            # Scaling relation: R_d \propto M_b^0.4 (approx)
            # Normalization: M=10^10 => R_d ~ 2-3 kpc
            R_d = 2.5 * (M_b / 1e10)**0.4
            R_d *= np.random.normal(1.0, 0.2) # Scatter
            
            # 3. Generate "Observed" Rotation Curve
            # We use a Standard NFW Dark Matter profile to generate "Truth"
            # This represents the "Observation" we are trying to fit with Machian physics.
            radii = np.linspace(0.1, 10 * R_d, 30) # Out to 10 scale lengths
            
            # Baryon Contribution (Exponential Disk)
            # V_bar^2 = (G M_b / R_d) * y^2 * [I0K0 - I1K1] ... let's approximate
            # Approx: V_bar^2 = G M(r) / r
            M_bar_r = M_b * (1 - (1 + radii/R_d) * np.exp(-radii/R_d))
            v_bar_sq = G_GRAV * M_bar_r / radii
            
            # Dark Matter Contribution (NFW)
            # V_dm^2 = V_200^2 * [ln(1+cx) - cx/(1+cx)] / [ln(1+c) - c/(1+c)]
            # V_200 derived from M_200. M_200 derived from M_b via abundance matching.
            # Approx M_200 ~ 50 * M_b (Stellar-to-halo mass relation)
            M_halo = 50 * M_b
            R_200 = (M_halo / (100 * 2.77e-7))**(1/3) # rough viral radius
            c = 10.0 * (M_halo / 1e12)**(-0.1) # Concentration
            R_s = R_200 / c
            
            x = radii / R_s
            v_vir_sq = G_GRAV * M_halo / R_200
            def nfw_func(x): return np.log(1+x) - x/(1+x)
            v_dm_sq = v_vir_sq * (R_200/radii) * (nfw_func(x) / nfw_func(c))
            
            v_total_sq = v_bar_sq + v_dm_sq
            v_obs = np.sqrt(v_total_sq)
            
            # Add observational noise
            v_obs += np.random.normal(0, 5.0, len(v_obs)) # 5 km/s noise
            v_err = np.ones_like(v_obs) * 5.0
            
            self.galaxies.append({
                'id': i,
                'M_b': M_b,
                'R_d': R_d,
                'radii': radii,
                'v_obs': v_obs,
                'v_err': v_err
            })
            
    def machian_model(self, r, M_fit, R_phi, beta):
        """
        The Machian Velocity Model:
        v^2 = (G M_bar(r) / r) * (1 + r/R_phi)^beta
        
        Here M_bar(r) is fixed by the 'M_fit' parameter which scales the baryonic mass.
        R_phi is the scalar field scale length.
        beta is the coupling index.
        """
        # Assume disk profile is known (fixed shape), just scaling M_fit
        # We use the stored R_d for the shape
        # Note: In a real survey, we fit M/L ratio. Here M_fit is effectively M_b.
        
        # This implies we need to know R_d inside this function. 
        # curve_fit doesn't support extra args easily that vary per call unless we wrap.
        # We will handle this in the loop.
        pass

    def run_survey_fit(self):
        print("Running Synthetic SPARC Survey (N=20)...")
        results = []
        
        for g in self.galaxies:
            # Define wrapper for this galaxy
            def fit_func(r, M_f, R_p, b):
                # Baryonic Contribution
                M_enclosed = M_f * (1 - (1 + r/g['R_d']) * np.exp(-r/g['R_d']))
                v_newt_sq = G_GRAV * M_enclosed / r
                v_newt_sq = np.nan_to_num(v_newt_sq)
                
                # Machian Boost
                # v^2 = v_newt^2 * (1 + r/R_phi)^beta
                boost = (1 + r/R_p)**b
                return np.sqrt(v_newt_sq * boost)
            
            # Initial Guesses - Start with Beta=1.0 (Flat curve)
            p0 = [g['M_b'], g['R_d']*5, 1.0] 
            # Bounds: Constrain Beta to be physical (0.5 to 1.5) to force flat-ish behavior
            # R_phi can be large (up to 500 kpc)
            bounds = ([1e7, 0.1, 0.5], [1e12, 500.0, 2.0])
            
            try:
                popt, _ = curve_fit(fit_func, g['radii'], g['v_obs'], p0=p0, bounds=bounds, maxfev=5000)
                
                if g['id'] == 0:
                    # Debug Plot for first galaxy
                    plt.figure()
                    plt.plot(g['radii'], g['v_obs'], 'ko', label='Observed (NFW)')
                    plt.plot(g['radii'], fit_func(g['radii'], *popt), 'r-', label='Machian Fit')
                    
                    # Show Newtonian
                    M_enclosed = popt[0] * (1 - (1 + g['radii']/g['R_d']) * np.exp(-g['radii']/g['R_d']))
                    v_newt = np.sqrt(G_GRAV * M_enclosed / g['radii'])
                    plt.plot(g['radii'], v_newt, 'b--', label='Newtonian (Baryon)')
                    
                    plt.title(f"Galaxy 0 Debug: R_phi={popt[1]:.1f}, Beta={popt[2]:.2f}")
                    plt.legend()
                    plt.savefig('papers/figures/survey_debug.png')
                    print("Saved debug plot.")

                results.append({
                    'M_b_true': g['M_b'],
                    'R_d_true': g['R_d'],
                    'M_fit': popt[0],
                    'R_phi': popt[1],
                    'beta': popt[2]
                })
            except Exception as e:
                print(f"Failed to fit galaxy {g['id']}: {e}")
                
        return results

    def analyze_results(self, results):
        M_b = np.array([r['M_b_true'] for r in results])
        R_d = np.array([r['R_d_true'] for r in results])
        R_phi = np.array([r['R_phi'] for r in results])
        beta = np.array([r['beta'] for r in results])
        
        print("\n--- Survey Analysis ---")
        print(f"Mean Coupling Beta: {np.mean(beta):.2f} +/- {np.std(beta):.2f}")
        
        # Check Scaling Relation R_phi vs R_d
        ratio = R_phi / R_d
        print(f"Mean Scale Ratio (R_phi/R_d): {np.mean(ratio):.2f} +/- {np.std(ratio):.2f}")
        
        # Plot R_phi vs R_d
        plt.figure(figsize=(10,5))
        plt.subplot(1,2,1)
        plt.scatter(R_d, R_phi, c='blue')
        plt.plot(R_d, 3.0*R_d, 'k--', label='R_phi = 3 R_d')
        plt.xlabel('Baryonic Scale Length R_d [kpc]')
        plt.ylabel('Scalar Scale Length R_phi [kpc]')
        plt.title('Scalar-Baryon Scaling Relation')
        plt.legend()
        
        # Plot Beta vs Mass
        plt.subplot(1,2,2)
        plt.scatter(np.log10(M_b), beta, c='red')
        plt.xlabel('Log Baryonic Mass [M_sun]')
        plt.ylabel('Coupling Beta')
        plt.title('Universality of Coupling')
        plt.axhline(1.0, color='k', linestyle='--')
        
        plt.tight_layout()
        plt.savefig('papers/figures/future_work_survey.png')
        print("Saved survey plot to papers/figures/future_work_survey.png")

if __name__ == "__main__":
    sim = GalaxySurveySimulator(n_galaxies=20)
    sim.generate_sample()
    res = sim.run_survey_fit()
    sim.analyze_results(res)
