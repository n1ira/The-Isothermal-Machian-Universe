import numpy as np
from scipy.optimize import minimize
import scipy.stats as stats

# Mock Data Generation (if file load fails)
def generate_mock_data():
    r = np.linspace(0.1, 20, 20)
    # Baryons
    v_bar = 100 * (r / (r + 2)) # Simple rising curve
    # True Model: Machian
    beta_true = 1.0e-6 # c^2 ~ 10^10, so v^2 ~ 10^4
    R_true = 5.0
    c = 3e5
    v_boost_sq = (c**2 * beta_true / 2) * (r/R_true) / (1 + r/R_true)
    v_obs = np.sqrt(v_bar**2 + v_boost_sq)
    # Add noise
    noise = np.random.normal(0, 5, size=len(r))
    v_obs += noise
    v_err = np.ones_like(r) * 5.0
    return r, v_bar, v_obs, v_err

# Models
def machian_model(theta, r, v_bar):
    # Theta: [log10_beta, R_scale]
    log_beta, R = theta
    beta = 10**log_beta
    c = 3e5 # km/s
    
    # The Machian Boost (Paper 1)
    # v^2 = v_bar^2 + c^2 * beta/2 * (r/R)/(1+r/R)
    v_boost_sq = (c**2 * beta / 2.0) * (r/R) / (1.0 + r/R)
    return np.sqrt(np.abs(v_bar**2 + v_boost_sq))

def nfw_model(theta, r, v_bar):
    # Theta: [V200, c_concentration, R200] -> simplified to [V_char, R_scale]
    # Standard NFW velocity profile
    V_h, R_h = theta
    x = r / R_h
    # NFW function f(x) = ln(1+x) - x/(1+x)
    func = np.log(1+x) - x/(1+x)
    v_halo_sq = V_h**2 * func / x
    return np.sqrt(np.abs(v_bar**2 + v_halo_sq))

# Likelihoods
def log_likelihood(theta, model_func, r, v_obs, v_err, v_bar):
    v_model = model_func(theta, r, v_bar)
    chi2 = np.sum(((v_obs - v_model) / v_err)**2)
    return -0.5 * chi2

def get_evidence(model_func, bounds, r, v_obs, v_err, v_bar):
    # Laplace Approximation
    # Z approx L_max * (2pi)^(k/2) * |H|^(-1/2)
    
    def neg_log_like(theta):
        # Priors (Flat within bounds)
        for i, val in enumerate(theta):
            if val < bounds[i][0] or val > bounds[i][1]:
                return 1e50
        return -log_likelihood(theta, model_func, r, v_obs, v_err, v_bar)

    # Find Max Likelihood
    x0 = [np.mean(b) for b in bounds]
    res = minimize(neg_log_like, x0, method='L-BFGS-B', bounds=bounds)
    
    if not res.success:
        return -np.inf
        
    # Hessian (Numerical approximation)
    # For simplicity in this demo, we assume a diagonal Hessian based on curvature
    # In a real full script, we would calculate finite difference Hessian
    
    log_L_max = -res.fun
    k = len(bounds)
    
    # Bic Approximation for simplicity (Evidence ~ L_max - k/2 ln N)
    n_data = len(r)
    bic = k * np.log(n_data) - 2 * log_L_max
    log_evidence = -0.5 * bic
    
    return log_evidence, res.x

def run_bayesian_test():
    print("Generating Mock Data (Simulating SPARC Galaxy)...")
    r, v_bar, v_obs, v_err = generate_mock_data()
    
    print("\n--- Model 1: Isothermal Machian Universe ---")
    # Bounds: log_beta [-8, -4], R [0.1, 50]
    bounds_imu = [(-8, -4), (0.1, 50)]
    log_Z_imu, best_imu = get_evidence(machian_model, bounds_imu, r, v_obs, v_err, v_bar)
    print(f"Best Fit IMU: log_beta={best_imu[0]:.2f}, R={best_imu[1]:.2f}")
    print(f"Log Evidence (approx): {log_Z_imu:.2f}")
    
    print("\n--- Model 2: Dark Matter (NFW) ---")
    # Bounds: V_h [10, 500], R_h [1, 100]
    bounds_nfw = [(10, 500), (1, 100)]
    log_Z_nfw, best_nfw = get_evidence(nfw_model, bounds_nfw, r, v_obs, v_err, v_bar)
    print(f"Best Fit NFW: V_h={best_nfw[0]:.2f}, R_h={best_nfw[1]:.2f}")
    print(f"Log Evidence (approx): {log_Z_nfw:.2f}")
    
    print("\n--- Result ---")
    bayes_factor = log_Z_imu - log_Z_nfw
    print(f"Log Bayes Factor (IMU - NFW): {bayes_factor:.2f}")
    
    if bayes_factor > 5:
        print("CONCLUSION: Strong evidence for Machian Universe.")
    elif bayes_factor < -5:
        print("CONCLUSION: Strong evidence for Dark Matter.")
    else:
        print("CONCLUSION: Inconclusive (Models are degenerate).")

if __name__ == "__main__":
    run_bayesian_test()
