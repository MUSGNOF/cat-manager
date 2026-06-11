@echo off
echo 启动猫管家应用本地服务器...
echo.
echo 应用将在浏览器中自动打开
echo 如果未自动打开，请访问: http://localhost:8080
echo.
echo 按 Ctrl+C 停止服务器
echo.

cd /d "%~dp0"
python -m http.server 8080