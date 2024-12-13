; filepath: ./installer.iss
[Setup]
AppName=AutoClicker
AppVersion=1.0
DefaultDirName={commonpf}\AutoClicker
DefaultGroupName=AutoClicker
OutputDir=./dist
OutputBaseFilename=AutoClickerInstaller

[Files]
Source: "dist\AutoClicker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.ini"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AutoClicker"; Filename: "{app}\AutoClicker.exe"
Name: "{group}\Uninstall AutoClicker"; Filename: "{uninstallexe}"