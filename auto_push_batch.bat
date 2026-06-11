@echo off
cd /d "D:\CatManager\gh-pages"
"C:\Program Files\Git\bin\git.exe" add -A
"C:\Program Files\Git\bin\git.exe" commit -m "历史记录页添加批量选择删除功能（含全选）"
"C:\Program Files\Git\bin\git.exe" pull --rebase origin main
"C:\Program Files\Git\bin\git.exe" push origin main
pause