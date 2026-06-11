@echo off
echo ============================================
echo 猫管家应用 - 手机端访问服务器
echo ============================================
echo.
echo 正在启动服务器...
echo.
echo 电脑端访问: http://localhost:8080
echo 手机端访问: http://192.168.2.196:8080
echo.
echo 确保手机和电脑在同一WiFi网络下
echo 在手机浏览器中打开上面的手机端地址
echo.
echo 按 Ctrl+C 停止服务器
echo ============================================
echo.

cd /d "%~dp0"
python start_mobile_server.py