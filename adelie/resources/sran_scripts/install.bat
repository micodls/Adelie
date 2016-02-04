@echo OFF

for /f "skip=2 tokens=3*" %%a in ('reg query HKCU\Environment /v PATH') do (
    if [%%b]==[] (
        setx PATH "%%~a;%cd%"
    ) else (
        setx PATH "%%~a %%~b;%cd%"
    )
)