!include "MUI2.nsh"

!define MyAppName "CorrectSentence"
!define MyAppVersion "1.0.0"
!define MyAppPublisher "Ace Centre"
!define MyAppURL "https://acecentre.org.uk"

Outfile "CorrectSentenceInstaller.exe"
RequestExecutionLevel user ; Request non-elevated installation

; Set the default installation directory
InstallDir "$LOCALAPPDATA\Ace Centre\${MyAppName}"

!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Main Program" SEC01
    SetOutPath "$INSTDIR\correctsentence"
    File /r "dist\correctsentence\*"
    SetOutPath "$INSTDIR\client"
    File /r "dist\client\*"
    SetOutPath "$INSTDIR\CreateGridset"
    File /r "dist\CreateGridset\*"
    SetOutPath "$APPDATA\Ace Centre\CorrectSentence"
    File "assets\CorrectASentenceDemo.gridset"
    ExecWait '"$SYSDIR\cmd.exe" "/c echo|set /p=Hello World|clip"'
    ExecWait '"$INSTDIR\CreateGridset\CreateGridset.exe"'
    ExecWait '"$WINDIR\System32\cmd.exe" "/c start /MIN "" cmd /c "$INSTDIR\correctsentence\correctsentence.exe""'

    WriteUninstaller "$INSTDIR\uninst.exe"
    SetShellVarContext current ; Ensure shortcuts and other context-sensitive actions target the current user
    CreateDirectory "$SMPROGRAMS\${MyAppName}"
    CreateShortCut "$SMPROGRAMS\${MyAppName}\${MyAppName}.lnk" "$INSTDIR\correctsentence\correctsentence.exe"
    CreateShortCut "$DESKTOP\${MyAppName}.lnk" "$INSTDIR\correctsentence\correctsentence.exe"
    CreateShortCut "$DESKTOP\Client.lnk" "$INSTDIR\client\client.exe"
    
    ; Write the uninstall keys for Windows
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}" "DisplayName" "${MyAppName} ${MyAppVersion}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}" "UninstallString" "$\"$INSTDIR\uninst.exe$\""
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}" "Publisher" "${MyAppPublisher}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}" "URLInfoAbout" "${MyAppURL}"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}" "DisplayVersion" "${MyAppVersion}"
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}" "NoModify" 1
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}" "NoRepair" 1
    ; Optionally, set the estimated size of the app, in KB
    WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}" "EstimatedSize" 737280
SectionEnd

Section "Uninstall"
    RmDir /r "$INSTDIR"
    Delete "$SMPROGRAMS\${MyAppName}\*.lnk"
    RmDir "$SMPROGRAMS\${MyAppName}"

    Delete "$DESKTOP\${MyAppName}.lnk"
    Delete "$DESKTOP\Client.lnk"
    
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MyAppName}"
SectionEnd
