@echo off
setlocal

set GIT_INSTALLER_URL=https://github.com/git-for-windows/git/releases/download/v2.33.0.windows.2/Git-2.33.0.2-64-bit.exe
set INSTALLER_FILENAME=Git-Installer.exe
set GIT_INSTALL_DIR=C:\Git

rem Check if Git is already installed
if exist "%GIT_INSTALL_DIR%\bin\git.exe" (
    echo Git is already installed in %GIT_INSTALL_DIR%
    goto AddToPath
)

echo Downloading Git installer...
curl -L -o %INSTALLER_FILENAME% %GIT_INSTALLER_URL%

echo Installing Git...
%INSTALLER_FILENAME% /VERYSILENT /DIR="%GIT_INSTALL_DIR%"

rem Add Git to system's PATH environment variable
:AddToPath
echo Adding Git to system's PATH...
setx PATH "%GIT_INSTALL_DIR%\bin;%PATH%" /M

echo Cleaning up...
del %INSTALLER_FILENAME%

echo Git installation completed.

endlocal
