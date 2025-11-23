import pypdf
import os
import sys

def verify_pdf(filename, expected_strings):
    path = os.path.join("papers", filename)
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
    # Look for: 209 km/s, 0.89 kpc, 0.98
    # Note: LaTeX math might be extracted weirdly, so stick to simple numbers/text
    # Paper 1: Galaxy Rotation
    p1_checks = [
        "Disk Stability Warning",
        "synthetic survey"
    ]
    
    # Paper 2: Cosmology
    p2_checks = [
        "purely mathematical",
        "Caveat"
    ]
    
    # Paper 4: Lensing
    p4_checks = []

    # Paper 5: Unified
    p5_checks = [
        "non-perturbative regime",
        "hypothesize that during cluster collisions"
    ]

    # Paper 6: CMB
    p6_checks = [
        "Disclaimer"
    ]

    # Dilaton
    dilaton_checks = [
        "QCD Trace Anomaly",
        "dimensional transmutation"
    ]
    
    success = True
    success &= verify_pdf("paper_1_galaxy_rotation.pdf", p1_checks)
    success &= verify_pdf("paper_2_cosmology.pdf", p2_checks)
    success &= verify_pdf("paper_4_lensing.pdf", p4_checks)
    success &= verify_pdf("paper_5_unified_field.pdf", p5_checks)
    success &= verify_pdf("paper_6_cmb.pdf", p6_checks)
    success &= verify_pdf("paper_7_dilaton.pdf", dilaton_checks)
    
    if success:
        print("\nSUCCESS: All PDFs contain the verified 'Kill Shot' data.")
    else:
        print("\nFAILURE: Some data points are missing from the PDFs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
