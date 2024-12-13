# Install dependencies
poetry install

# Export requirements
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --with dev --output requirements-dev.txt

# Activate virtual environment
$venvPath = (poetry env info --path)
& "$venvPath\Scripts\Activate.ps1"

# Create a blank config.ini if it doesn't exist
$configPath = "./config.ini"
if (-Not (Test-Path $configPath)) {
    New-Item -ItemType File -Path $configPath
}

# Run PyInstaller
$packageName = (Select-String -Path "pyproject.toml" -Pattern 'name\s*=\s*"(.*)"').Matches.Groups[1].Value
$distPath = "./dist"
$icoPath = "./AutoClicker.ico"
pyinstaller --onefile --windowed --add-data "config.ini;." --distpath $distPath --icon $icoPath --collect-all $packageName autoclicker.py

# Run Inno Setup to create the installer
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer.iss"