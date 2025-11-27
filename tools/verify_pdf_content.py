import pypdf
import os
import sys

def verify_pdf(filename, expected_strings):
    path = os.path.join("papers/build", filename)
    if not os.path.exists(path):
        print(f"FAIL: {filename} not found.")
        return False
    
    print(f"Checking {filename}...")
    try:
        reader = pypdf.PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Normalize text to handle potential encoding/spacing issues
        text = text.replace("\n", " ")
        
        all_found = True
        for s in expected_strings:
            if s in text:
                print(f"  [OK] Found '{s}'")
            else:
                print(f"  [FAIL] Could not find '{s}'")
                # Try a fuzzy check for numbers
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"ERROR reading {filename}: {e}")
        return False

def main():
    print("Verifying PDF Content...")
    
    # Paper 1: Galaxy Rotation
    # Changed "Disk Stability Warning" to "Secular Evolution"
    p1_checks = [
        "Secular Evolution",
        "Ostriker-Peebles",
        "synthetic survey"
    ]
    
    # Paper 2: Cosmology
    # Added "Thermodynamic" arguments
    p2_checks = [
        "Etherington",
        "Topological Invariant",
        "Breaking Conformal Duality"
    ]
    
    # Paper 3: Black Holes
    p3_checks = [
        "Holographic Freezing",
        "Saturation Proof",
        "Perfect Quantum Fluid"
    ]
    
    # Paper 4: Lensing
    # Updated to ensure Universal Coupling is mentioned
    p4_checks = [
        "Universal Conformal Coupling"
    ]

    # Paper 5: Unified
    # Removed "QCD Trigger" (qualitative), added rigorous Thin Shell and DHOST
    p5_checks = [
        "Thin-Shell Screening",
        "DHOST Class I",
        "falsification test",
        "Bohmian Quantum Potential"
    ]

    # Paper 6: CMB
    # Removed "Heisenberg" (qualitative), added "Synchronous Gauge"
    p6_checks = [
        "synchronous gauge",
        "anisotropic stress"
    ]

    # Paper 7: Dilaton
    dilaton_checks = [
        "QCD Trace Anomaly",
        "dimensional transmutation"
    ]
    
    # Paper 8: Cyclic
    p8_checks = [
        "Scale-Dependent Unitarity"
    ]
    
    # Kill Shot Letter
    letter_checks = [
        "Thermodynamic Break",
        "Standard Sirens"
    ]
    
    success = True
    success &= verify_pdf("paper_01_galaxy_rotation.pdf", p1_checks)
    success &= verify_pdf("paper_02_cosmology.pdf", p2_checks)
    success &= verify_pdf("paper_03_black_holes.pdf", p3_checks)
    success &= verify_pdf("paper_04_lensing.pdf", p4_checks)
    success &= verify_pdf("paper_05_unified_field.pdf", p5_checks)
    success &= verify_pdf("paper_06_cmb.pdf", p6_checks)
    success &= verify_pdf("paper_07_dilaton.pdf", dilaton_checks)
    success &= verify_pdf("paper_08_cyclic.pdf", p8_checks)
    success &= verify_pdf("letter_kill_shot.pdf", letter_checks)
    
    if success:
        print("\nSUCCESS: All PDFs contain the verified 'Kill Shot' data.")
    else:
        print("\nFAILURE: Some data points are missing from the PDFs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
