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
    p1_checks = [
        "209", # Velocity
        "0.89", # Scale length
        "0.98", # Beta
        "coupling constant"
    ]
    
    # Paper 2: Cosmology
    # Look for: 30.8 Billion, 15.92 Billion
    p2_checks = [
        "30.8 Billion Years",
        "15.92 Billion Years",
        "Blue Screen of Death"
    ]
    
    # Paper 3: Black Holes
    # Look for: Holographic Freezing, 10^5 (might be 105 or 10 5), 1.51
    p3_checks = [
        "Holographic Freezing",
        "Alice",
        "Bob"
    ]
    
    success = True
    success &= verify_pdf("paper_1_galaxy_rotation.pdf", p1_checks)
    success &= verify_pdf("paper_2_cosmology.pdf", p2_checks)
    success &= verify_pdf("paper_3_black_holes.pdf", p3_checks)
    
    if success:
        print("\nSUCCESS: All PDFs contain the verified 'Kill Shot' data.")
    else:
        print("\nFAILURE: Some data points are missing from the PDFs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
