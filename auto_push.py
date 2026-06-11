#!/usr/bin/env python3
"""
自动推送更新到 GitHub Pages
通过 GitHub API 直接更新文件，无需手动操作
"""
import os
import json
import base64
import requests
import sys

# GitHub 仓库信息
REPO_OWNER = "MUSGNOF"
REPO_NAME = "cat-manager"
BRANCH = "main"  # GitHub Pages 使用 main 分支
FILE_PATH = "index.html"

# 从环境变量或配置文件中获取 GitHub Token
def get_github_token():
    # 尝试从环境变量获取
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    
    # 尝试从配置文件获取
    config_file = os.path.join(os.path.dirname(__file__), "github_token.txt")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            token = f.read().strip()
            if token:
                return token
    
    # 尝试从 git config 获取
    try:
        import subprocess
        result = subprocess.run(
            ["git", "config", "--get", "github.token"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None

def get_file_sha():
    """获取文件当前 SHA"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    token = get_github_token()
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["sha"]
        else:
            print(f"获取文件 SHA 失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"获取文件 SHA 出错: {e}")
        return None

def update_file():
    """更新文件到 GitHub"""
    # 读取本地文件内容
    local_file = os.path.join(os.path.dirname(__file__), FILE_PATH)
    with open(local_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 获取文件当前 SHA
    sha = get_file_sha()
    if sha is None:
        print("无法获取文件 SHA，可能是文件不存在或网络问题")
        return False
    
    # 准备 API 请求
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    token = get_github_token()
    if token:
        headers["Authorization"] = f"token {token}"
    
    # 构建请求数据
    data = {
        "message": "自动更新：修复滑动删除功能",
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "sha": sha,
        "branch": BRANCH
    }
    
    try:
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print("✅ 文件更新成功！")
            print(f"提交信息: {data['message']}")
            print(f"提交 SHA: {response.json()['commit']['sha']}")
            print(f"文件 URL: {response.json()['content']['html_url']}")
            return True
        else:
            print(f"❌ 文件更新失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 更新过程中出错: {e}")
        return False

def setup_github_token():
    """设置 GitHub Token 的说明"""
    print("=" * 60)
    print("GitHub Token 设置说明")
    print("=" * 60)
    print("要自动推送更新，需要 GitHub Personal Access Token")
    print("")
    print("创建步骤:")
    print("1. 登录 GitHub: https://github.com")
    print("2. 点击右上角头像 → Settings → Developer settings")
    print("3. 选择 Personal access tokens → Tokens (classic)")
    print("4. 点击 Generate new token (classic)")
    print("5. 填写 Note: '猫管家自动推送'")
    print("6. 选择权限: repo (全部权限)")
    print("7. 点击 Generate token")
    print("8. 复制生成的 token (只显示一次，请保存好)")
    print("")
    print("设置方法 (任选一种):")
    print("A. 环境变量: set GITHUB_TOKEN=你的token")
    print("B. 配置文件: 在 D:\\CatManager\\gh-pages\\github_token.txt 中写入token")
    print("C. Git配置: git config --global github.token 你的token")
    print("=" * 60)

def main():
    print("🐱 猫管家应用 - 自动推送更新到 GitHub Pages")
    print("=" * 60)
    
    # 检查本地文件是否存在
    local_file = os.path.join(os.path.dirname(__file__), FILE_PATH)
    if not os.path.exists(local_file):
        print(f"❌ 本地文件不存在: {local_file}")
        return
    
    print(f"📁 本地文件: {local_file}")
    print(f"📊 文件大小: {os.path.getsize(local_file)} 字节")
    
    # 检查 GitHub Token
    token = get_github_token()
    if not token:
        print("❌ 未找到 GitHub Token")
        setup_github_token()
        
        # 创建配置文件
        config_file = os.path.join(os.path.dirname(__file__), "github_token.txt")
        if not os.path.exists(config_file):
            with open(config_file, "w") as f:
                f.write("# 请在此处输入你的 GitHub Personal Access Token\n")
                f.write("# 获取方法见上面的说明\n")
                f.write("# 格式: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
            print(f"📄 已创建配置文件: {config_file}")
            print("请编辑该文件，填入你的 GitHub Token")
        
        return
    
    print("✅ 已找到 GitHub Token")
    
    # 尝试更新文件
    print("🔄 正在更新文件到 GitHub...")
    success = update_file()
    
    if success:
        print("=" * 60)
        print("🎉 更新成功！")
        print(f"📱 手机端访问: https://{REPO_OWNER}.github.io/{REPO_NAME}/")
        print("⏱️  GitHub Pages 部署需要 1-3 分钟")
        print("=" * 60)
    else:
        print("=" * 60)
        print("❌ 更新失败")
        print("请检查网络连接和 GitHub Token 权限")
        print("=" * 60)

if __name__ == "__main__":
    main()