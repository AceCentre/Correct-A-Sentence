; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "CorrectSentence "
#define MyAppVersion "1.0.0" ; Update with your actual version
#define MyAppPublisher "Ace Centre"
#define MyAppURL "https://acecentre.org.uk" ; Update with your website

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{E38A71DA-9390-48E3-9F70-52D77EE41F98}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\AceCentre\CorrectSentence
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
DisableDirPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=lowest
;PrivilegesRequiredOverridesAllowed=dialog
OutputBaseFilename=CorrectSentence
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs 

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\Correctsentence\correctsentence.exe"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\Correctsentence\correctsentence.exe"; Tasks: desktopicon
Name: "{autodesktop}\client"; Filename: "{app}\client\client.exe"; Tasks: desktopicon
[Run]
Filename: "{app}\CreateGridset.exe"
Filename: "{cmd}"; Parameters: "start""/b""cmd""/c""echo|set /p=Hello World|clip"; Flags: nowait skipifsilent
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked
Filename: "{app}\Correctsentence\correctsentence.exe"; Flags: nowait postinstall skipifsilent
