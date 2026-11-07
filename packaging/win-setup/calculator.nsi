; calculator.nsi установочный пакет (setup) для Windows
; Сборка: makensis calculator.nsi
; Требование на целевой системе: Python 3 с модулем Tkinter (python.org)

!define APPNAME    "Calculator"
!define APPVERSION "1.0"
!define PUBLISHER  "deuf00"
!define APPDIR     "calculator"

Unicode true
RequestExecutionLevel admin
InstallDir "$PROGRAMFILES64\${APPNAME}"

!include "MUI2.nsh"
!include "LogicLib.nsh"

!define MUI_ABORTWARNING

Name    "${APPNAME}"
OutFile "calculator-1.0-setup.exe"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "README.md"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Russian"

; проверяем наличие Python до начала установки
Function .onInit
    nsExec::ExecToStack "python --version"
    Pop $0
    Pop $1
    ${If} $0 != 0
        MessageBox MB_YESNO|MB_ICONEXCLAMATION \
            "Python не найден в PATH.$\nДля работы калькулятора требуется Python 3 (с Tkinter) с python.org.$\n$\nПродолжить установку?" \
            IDYES ok
        Abort
    ${EndIf}
    ok:
FunctionEnd

Section "Установка"
    SetOutPath "$INSTDIR"
    File /r "app\${APPDIR}"

    ; добавляем папку приложения в PYTHONPATH и запускаем модуль
    FileOpen $0 "$INSTDIR\${APPDIR}.cmd" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 "set PYTHONPATH=$INSTDIR$\r$\n"
    FileWrite $0 "python -m ${APPDIR}.main %*$\r$\n"
    FileClose $0

    ; Ярлыки в меню пуск и на рабочем столе
    CreateShortcut "$SMPROGRAMS\${APPNAME}.lnk" "$INSTDIR\${APPDIR}.cmd" "" "$INSTDIR\${APPDIR}\main.py"
    CreateShortcut "$DESKTOP\${APPNAME}.lnk"    "$INSTDIR\${APPDIR}.cmd" "" "$INSTDIR\${APPDIR}\main.py"

    ; Деинсталлятор
    WriteUninstaller "$INSTDIR\uninstall.exe"

    ; Запись в Установку и удаление программ
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
        "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
        "DisplayVersion" "${APPVERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
        "Publisher" "${PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
        "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
        "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
        "NoRepair" 1
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\${APPDIR}.cmd"
    Delete "$INSTDIR\uninstall.exe"
    RMDir /r "$INSTDIR\${APPDIR}"
    RMDir "$INSTDIR"

    Delete "$SMPROGRAMS\${APPNAME}.lnk"
    Delete "$DESKTOP\${APPNAME}.lnk"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd
