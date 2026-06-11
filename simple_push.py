#!/usr/bin/env python3
"""
简单推送脚本 - 使用 subprocess 执行 Git 命令
"""
import subprocess
import sys
import os

def run_git_command(args):
    """运行 Git 命令"""
    git_path = r"C:\Program Files\Git\bin\git.exe"
    cmd = [git_path] + args
    
    try:
        print(f"执行命令: {' '.join(cmd)}")
        
        # 使用 subprocess.run 并设置超时
        result = subprocess.run(
            cmd,
            cwd=r"D:\CatManager\gh-pages",
            capture_output=True,
            text=True,
            timeout=30,  # 30秒超时
            encoding='utf-8',
            errors='ignore'
        )
        
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出: {result.stdout}")
        if result.stderr:
            print(f"错误: {result.stderr}")
        
        return result.returncode == 0, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print("❌ 命令执行超时 (30秒)")
        return False, "", "超时"
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False, "", str(e)

def main():
    print("🐱 猫管家应用 - 简单推送脚本")
    print("=" * 60)
    
    # 检查当前状态
    print("1. 检查当前状态...")
    success, output, error = run_git_command(["status"])
    if not success:
        print("❌ 无法获取 Git 状态")
        return
    
    # 检查是否有需要推送的提交
    print("\n2. 检查待推送的提交...")
    success, output, error = run_git_command(["log", "--oneline", "origin/main..main"])
    if success and output.strip():
        print(f"待推送的提交:\n{output}")
    else:
        print("没有需要推送的提交")
    
    # 尝试推送
    print("\n3. 尝试推送...")
    print("注意: 如果网络连接有问题，这可能会超时")
    
    # 先尝试 HTTPS
    print("\n尝试 HTTPS 方式...")
    run_git_command(["remote", "set-url", "origin", "https://github.com/MUSGNOF/cat-manager.git"])
    success, output, error = run_git_command(["push", "origin", "main"])
    
    if success:
        print("\n✅ 推送成功！")
        print(f"📱 手机端访问: https://musgnof.github.io/cat-manager/")
        print("⏱️  GitHub Pages 部署需要 1-3 分钟")
    else:
        print("\n❌ HTTPS 推送失败，尝试 SSH 方式...")
        run_git_command(["remote", "set-url", "origin", "git@github.com:MUSGNOF/cat-manager.git"])
        success, output, error = run_git_command(["push", "origin", "main"])
        
        if success:
            print("\n✅ SSH 推送成功！")
            print(f"📱 手机端访问: https://musgnof.github.io/cat-manager/")
            print("⏱️  GitHub Pages 部署需要 1-3 分钟")
        else:
            print("\n❌ 推送失败")
            print("可能的原因:")
            print("1. 网络连接问题")
            print("2. GitHub 认证问题")
            print("3. 仓库权限问题")
            print("\n建议:")
            print("1. 检查网络连接")
            print("2. 使用以下命令手动推送:")
            print("   cd D:\\CatManager\\gh-pages")
            print("   \"C:\\Program Files\\Git\\bin\\git.exe\" push origin main")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()