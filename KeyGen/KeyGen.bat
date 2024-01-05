@echo off
setlocal EnableDelayedExpansion

set "characters=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

:generateKey
set "key=VISION-"

for /l %%i in (1,1,24) do (
    set /a "randomIndex=!random! %% 62"
    for %%j in (!randomIndex!) do set "key=!key!!characters:~%%j,1!"

    if %%i equ 6 (
        set "key=!key!-"
    ) else if %%i equ 12 (
        set "key=!key!-"
    ) else if %%i equ 18 (
        set "key=!key!-"
    ) else if %%i equ 24 (
        set "key=!key!-"
    )
)

echo %key%
timeout /nobreak /t 1 >nul
goto generateKey


echo %key%
pause