# Install dependencies
poetry install

# Export requirements
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --with dev --output requirements-dev.txt

# Run PyInstaller
$distPath = "$env:APPDATA\AutoClicker"
$icoPath = "./AutoClicker.ico"
pyinstaller --onefile --windowed --add-data "config.ini;." --distpath $distPath --icon $icoPath autoclicker.py