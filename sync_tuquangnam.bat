@echo off
title Git Auto Push - tuquangnam
color 0E

:: Di chuyển vào thư mục repo tuquangnam
cd /d G:\github-git\tuquangnam

echo ========================================
echo    GIT AUTO PUSH - TUQUANGNAM
echo ========================================
echo.

:: Kiểm tra xem thư mục có tồn tại không
if not exist ".git" (
    echo [!] Khong tim thay thu muc .git!
    echo [!] Hay chac chan rang ban dang o dung thu muc repo.
    pause
    exit /b
)

:: Tạo commit message an toàn với ngày tháng năm
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set day=%%a
    set month=%%b
    set year=%%c
)
:: Lấy thời gian để commit message chi tiết hơn
for /f "tokens=1-3 delims=: " %%a in ('echo %time%') do (
    set hour=%%a
    set minute=%%b
)
set commit_msg=Update-%year%%month%%day%_%hour%%minute%

echo [1] Kiem tra trang thai hien tai...
git status

echo.
echo [2] Pull ve truoc de tranh conflict...
git pull origin main --allow-unrelated-histories

if errorlevel 1 (
    echo [!] Pull that bai! Thu voi --rebase...
    git pull origin main --rebase
)

echo.
echo [3] Dang add va commit...
git add .
git commit -m "%commit_msg%"

echo.
echo [4] Dang push len GitHub...
git push origin main

if errorlevel 1 (
    echo.
    echo [!] Push that bai! Thu force push...
    echo [WARNING] Force push se ghi de len remote!
    set /p confirm="Ban co muon force push? (y/n): "
    if /i "%confirm%"=="y" (
        echo Dang thuc hien force push...
        git push origin main --force
        if errorlevel 1 (
            echo [!] Force push that bai!
        ) else (
            echo [OK] Force push thanh cong!
        )
    ) else (
        echo [!] Da huy force push.
    )
)

echo.
echo ========================================
echo    HOAN THANH!
echo ========================================
echo.
echo Commit message: %commit_msg%
echo.
pause