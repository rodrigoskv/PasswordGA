REM ...existing code...
@echo off
REM Run python main.py 100 times
for /L %%i in (1,1,10) do (
  python main.py
)