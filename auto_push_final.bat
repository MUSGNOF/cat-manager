@echo off
chcp 65001 >nul
echo ============================================================
echo 猫管家应用 - 自动推送更新到 GitHub Pages
echo ============================================================
echo.

:: 设置路径
set GIT_PATH="C:\Program Files\Git\bin\git.exe"
set REPO_PATH="D:\CatManager\gh-pages"
set GITHUB_URL=https://github.com/MUSGNOF/cat-manager.git

:: 检查网络连接
echo [检查网络连接...]
ping -n 2 github.com >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 网络连接失败，无法连接到 GitHub
    echo 请检查网络连接后重试
    pause
    exit /b 1
)
echo [成功] 网络连接正常

:: 进入仓库目录
cd /d %REPO_PATH%
if %errorlevel% neq 0 (
    echo [错误] 无法进入仓库目录: %REPO_PATH%
    pause
    exit /b 1
)

:: 检查当前状态
echo [检查 Git 状态...]
%GIT_PATH% status
echo.

:: 检查是否有未提交的更改
%GIT_PATH% diff --quiet index.html
if %errorlevel% equ 0 (
    echo [信息] index.html 文件没有更改
) else (
    echo [信息] index.html 有未提交的更改
    %GIT_PATH% add index.html
    %GIT_PATH% commit -m "自动更新：滑动删除功能修复"
    echo [成功] 已提交更改
)

:: 尝试推送
echo [尝试推送更新到 GitHub...]
echo 这可能需要一些时间，请耐心等待...

:: 设置超时和重试机制
set MAX_RETRIES=3
set RETRY_DELAY=10
set RETRY_COUNT=0

:push_retry
echo.
echo 尝试推送 (第 %RETRY_COUNT% 次)...
%GIT_PATH% push origin main

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo [成功] 推送成功！
    echo 手机端访问: https://musgnof.github.io/cat-manager/
    echo GitHub Pages 部署需要 1-3 分钟
    echo ============================================================
    pause
    exit /b 0
) else (
    set /a RETRY_COUNT+=1
    if %RETRY_COUNT% lss %MAX_RETRIES% (
        echo [错误] 推送失败，%RETRY_DELAY% 秒后重试...
        timeout /t %RETRY_DELAY% /nobreak >nul
        goto push_retry
    ) else (
        echo.
        echo ============================================================
        echo [错误] 推送失败，已重试 %MAX_RETRIES% 次
        echo.
        echo 可能的原因:
        echo 1. 网络连接问题
        echo 2. GitHub 认证问题
        echo 3. 仓库权限问题
        echo.
        echo 解决方案:
        echo 1. 检查网络连接
        echo 2. 使用以下命令手动推送:
        echo    cd %REPO_PATH%
        echo    %GIT_PATH% push origin main
        echo ============================================================
        pause
        exit /b 1
    )
)