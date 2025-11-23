import numpy as np
import matplotlib.pyplot as plt
import os

def plot_comparison():
    print("Generating Comparison Plot...")
    
    # Load Data
    try:
        data_pm = np.loadtxt("lab/simulation/matter_power_spectrum.dat")
        data_p3m = np.loadtxt("lab/simulation/p3m_power_spectrum.dat")
    except OSError:
        print("Error: Could not find data files. Run Experiment 7 and 8 first.")
        return

    k_pm = data_pm[:, 0]
    P_pm = data_pm[:, 1]
    
    k_p3m = data_p3m[:, 0]
    P_p3m = data_p3m[:, 1]
    
    plt.figure(figsize=(10, 6))
    
    # Plot PM (Exp 7)
    plt.loglog(k_pm, P_pm, 'r--', linewidth=2, label='Exp 7: PM Only (Resolution Limited)')
    
    # Plot P3M (Exp 8)
    plt.loglog(k_p3m, P_p3m, 'c-', linewidth=3, label='Exp 8: P3M (Isothermal Machian Kill Shot)')
    
    # Plot LCDM expectation (approx slope -3)
    # Anchor at k=1
    # P ~ k^-3
    # k_ref = np.linspace(0.5, 10, 100)
    # P_ref = 100 * (k_ref/1.0)**(-3)
    # plt.loglog(k_ref, P_ref, 'k:', alpha=0.5, label='LCDM Slope ~ -3')
    
    plt.title("The 'Kill Shot': Restoring Small Scale Power", fontsize=14)
    plt.xlabel(r"Wavenumber $k$ [h/Mpc]", fontsize=12)
    plt.ylabel(r"$P(k)$ [(Mpc/h)$^3$]", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3, which='both')
    
    # Annotation
    plt.annotate("P3M restores\nCDM-like clustering", xy=(3, 20), xytext=(5, 100),
                 arrowprops=dict(facecolor='cyan', shrink=0.05))
    
    output_file = "comparison_result.png"
    plt.savefig(output_file, dpi=150)
    print(f"Saved {output_file}")

if __name__ == "__main__":
    plot_comparison()
