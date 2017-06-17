!include "MUI.nsh"
!define MUI_ICON "D:\00 eigene Daten\000 FH\S 4\Regelungstechnik\Regelungsversuch\microRay\inkScapeLogos\iconSmall.ico"
!define MUI_UNICON "D:\00 eigene Daten\000 FH\S 4\Regelungstechnik\Regelungsversuch\microRay\inkScapeLogos\iconSmall.ico"

!include "FileAssociation.nsh"

Name "microRay"
!define INSTALLATIONNAME "microRay"
!define VERSION "v5"
OutFile "officialWebsite\microRayInstaller_${VERSION}_win32.exe"
InstallDir $PROGRAMFILES\microRay

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section ""
  SetOutPath $INSTDIR
  File /r "D:\00 eigene Daten\000 FH\S 4\Regelungstechnik\Regelungsversuch\microRay\dist\microRay\*"
  WriteUninstaller $INSTDIR\uninstall.exe
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${INSTALLATIONNAME}" "DisplayName" "microRay"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${INSTALLATIONNAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${INSTALLATIONNAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${INSTALLATIONNAME}" "NoRepair" 1

  ;Create file association
  ${registerExtension} "$INSTDIR\microRay.exe" ".mRay" "mRay_project_file"
  ;WriteRegStr HKCR ".mRay" "" "microRay.exe"
  ;WriteRegStr HKCR "microRay.exe" "" '"\"$INSTDIR\microRay.exe" -f\"%1\""'
  ;WriteRegStr HKCR "microRay.exe\shell\open\command" "" "$\"$INSTDIR\microRay.exe$\" $\"%1$\""

  ;Create desktop shortcut
  CreateShortCut "$DESKTOP\microRay.lnk" "$INSTDIR\microRay.exe" ""
SectionEnd

Section "Start Menu Shortcuts"
  CreateDirectory "$SMPROGRAMS\${INSTALLATIONNAME}"
  CreateShortCut "$SMPROGRAMS\${INSTALLATIONNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\${INSTALLATIONNAME}\microRay.lnk" "$INSTDIR\microRay.exe" "" "$INSTDIR\microRay.exe" 0
SectionEnd


Section "Uninstall"
  ;Delete Start Menu Shortcuts
  Delete "$DESKTOP\microRay.lnk"

  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${INSTALLATIONNAME}"

  ;Delete file association
  ${unregisterExtension} ".mRay" "mRay_project_file"
  ;DeleteRegKey HKCR ".mRay"
  ;DeleteRegKey HKCR "microRay.exe"

  ;Delete /r $INSTDIR\*
  RMDir /r $INSTDIR
  Delete "$SMPROGRAMS\${INSTALLATIONNAME}\*.*"
  RMDir "$SMPROGRAMS\${INSTALLATIONNAME}"
SectionEnd