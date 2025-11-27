# Build Script for Machian Universe Papers
# Automatically compiles all LaTeX files in papers/source and renames them to the clean format.

$sourceDir = Resolve-Path "papers\source"
$buildDir = Resolve-Path "papers\build"
$figuresDir = Resolve-Path "papers\figures"

# Ensure build directory exists
if (-not (Test-Path -Path $buildDir)) {
    New-Item -ItemType Directory -Path $buildDir | Out-Null
}

# Set TEXINPUTS to include the figures directory
# We add the absolute path to figuresDir to the search path
$env:TEXINPUTS = ".;$figuresDir;"

# Get all .tex files
$texFiles = Get-ChildItem -Path $sourceDir -Filter "*.tex"

foreach ($file in $texFiles) {
    Write-Host "Processing $($file.Name)..." -ForegroundColor Cyan
    
    # Compile with pdflatex (run twice for references)
    # We run from the source directory so relative paths might work better, 
    # but TEXINPUTS should handle the figures.
    Push-Location $sourceDir
    
    pdflatex -interaction=nonstopmode -output-directory=$buildDir $file.Name | Out-Null
    pdflatex -interaction=nonstopmode -output-directory=$buildDir $file.Name | Out-Null
    
    Pop-Location
    
    # Construct new name
    $baseName = $file.BaseName
    
    # Remove "paper_" prefix
    if ($baseName -match "^paper_(.*)") {
        $baseName = $matches[1]
    }
    
    # Capitalize first letter of each word separated by underscores
    $parts = $baseName.Split('_')
    $newParts = @()
    foreach ($part in $parts) {
        $newParts += $part.Substring(0, 1).ToUpper() + $part.Substring(1)
    }
    $newName = $newParts -join "_"
    
    $pdfName = "$newName.pdf"
    
    # Move/Rename the compiled PDF
    $compiledPdf = Join-Path $buildDir "$($file.BaseName).pdf"
    $targetPdf = Join-Path $buildDir $pdfName
    
    if (Test-Path $compiledPdf) {
        Move-Item -Path $compiledPdf -Destination $targetPdf -Force
        Write-Host "  -> Generated: $pdfName" -ForegroundColor Green
    }
    else {
        Write-Host "  -> Error: Compilation failed for $($file.Name)" -ForegroundColor Red
    }
}

# Cleanup aux/log files
Remove-Item "$buildDir\*.aux", "$buildDir\*.log", "$buildDir\*.out" -ErrorAction SilentlyContinue

Write-Host "Build Complete!" -ForegroundColor Yellow
