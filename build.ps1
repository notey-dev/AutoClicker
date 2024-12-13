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
$distPath = "$env:APPDATA\AutoClicker"
$icoPath = "./AutoClicker.ico"
pyinstaller --onefile --windowed --add-data "config.ini;." --distpath $distPath --icon $icoPath --collect-all autoclicker autoclicker.py