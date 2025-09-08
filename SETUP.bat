@echo off
echo 🎁 Starting GiftNest E-commerce Platform Setup...
echo.

REM Check if we're in a virtual environment and warn user
if defined VIRTUAL_ENV (
    echo ⚠️  WARNING: You are currently in a virtual environment!
    echo Please deactivate first by running: deactivate
    echo Or close this terminal and open a new one.
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
    echo.
)

python setup.py
echo.
echo Setup completed! Check the instructions above.
pause