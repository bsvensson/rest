@ECHO OFF

@ECHO If needed, change PRO variable according to where you arcpy is...

@REM TODO - check if right python already available...

IF EXIST "%LOCALAPPDATA%\Programs\Pro\bin\Python" (
    SET PRO=%LOCALAPPDATA%\Programs\Pro\bin\Python
) ELSE IF EXIST "%ProgramFiles%\ArcGIS\Pro\bin\Python" (
    SET PRO=%ProgramFiles%\ArcGIS\Pro\bin\Python
) ELSE (
    echo Sorry, not sure where your arcpy is...
)

SET PATH=%PRO%\Scripts;%PRO%\envs\arcgispro-py3;%PATH%

@REM sanity check

python --version

@ECHO ON
