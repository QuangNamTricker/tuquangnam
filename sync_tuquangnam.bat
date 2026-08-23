@echo off
title Git Auto Push - tuquangnam
color 0E

cd /d G:\github-git\tuquangnam

echo ========================================
echo    GIT AUTO PUSH - TUQUANGNAM
echo ========================================
echo.

:: Tạo commit message an toàn
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set day=%%a
    set month=%%b
    set year=%%c
)
set commit_msg=Update-%year%%month%%day%

echo [1] Pull ve truoc...
git pull origin main --allow-unrelated-histories

if errorlevel 1 (
    echo [!] Pull that bai! Thu voi --rebase...
    git pull origin main --rebase
)

echo.
echo [2] Dang add va commit...
git add .
git commit -m "%commit_msg%"

echo.
echo [3] Dang push len GitHub...
git push origin main

if errorlevel 1 (
    echo.
    echo [!] Push that bai! Thu force push...
    echo [WARNING] Force push se ghi de len remote!
    set /p confirm="Ban co muon force push? (y/n): "
    if /i "%confirm%"=="y" (
        git push origin main --force
    )
)

echo.
echo ========================================
echo    HOAN THANH!
echo ========================================
pause