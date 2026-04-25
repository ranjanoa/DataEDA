# Build MSIX Package Script for DataEDA

# Find makeappx.exe dynamically
$makeappx = (Get-ChildItem "C:\Program Files (x86)\Windows Kits\10\bin" -Recurse -Filter "makeappx.exe" | Select-Object -First 1 -ExpandProperty FullName)
if (-not $makeappx) {
    $makeappx = (Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin" -Recurse -Filter "makeappx.exe" | Select-Object -First 1 -ExpandProperty FullName)
}

if (-not $makeappx) {
    Write-Error "makeappx.exe not found."
    exit 1
}

$distDir = "dist"
$packageDir = "package"
$layoutDir = "msix_layout"
$outputFile = "DataEDA.msix"

Write-Host "--- 1. Building Executable ---" -ForegroundColor Cyan
pyinstaller --onefile --noconsole --name "DataEDA" `
    --add-data "frontend;frontend" `
    --paths "backend" `
    backend/main.py

Write-Host "--- 2. Preparing Layout ---" -ForegroundColor Cyan
if (Test-Path $layoutDir) { Remove-Item -Recurse -Force $layoutDir }
New-Item -ItemType Directory -Path $layoutDir
New-Item -ItemType Directory -Path "$layoutDir\Assets"
Copy-Item "$distDir\DataEDA.exe" "$layoutDir\DataEDA.exe"
Copy-Item "$packageDir\AppxManifest.xml" "$layoutDir\AppxManifest.xml"
Copy-Item "$packageDir\Assets\*" "$layoutDir\Assets\" -Recurse

Write-Host "--- 3. Packaging ---" -ForegroundColor Cyan
if (Test-Path $outputFile) { Remove-Item $outputFile }
& $makeappx pack /d $layoutDir /p $outputFile /o

Write-Host "Successfully created $outputFile" -ForegroundColor Green
