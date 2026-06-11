#!/usr/bin/env python3
"""
猫管家应用 - 手机端访问服务器
手机访问: http://192.168.2.196:8080
"""
import http.server
import socketserver
import webbrowser
import socket
import os
import sys

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加CORS头，允许手机访问
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def get_local_ip():
    """获取本机局域网IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.2.196"  # 使用已知的IP

def main():
    PORT = 8080
    local_ip = get_local_ip()
    
    # 切换到当前目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 60)
    print("猫管家应用 - 手机端访问服务器")
    print("=" * 60)
    print(f"电脑端访问: http://localhost:{PORT}")
    print(f"手机端访问: http://{local_ip}:{PORT}")
    print("=" * 60)
    print("确保手机和电脑在同一WiFi网络下")
    print("在手机浏览器中打开上面的手机端地址")
    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print()
    
    # 自动在电脑浏览器打开
    try:
        webbrowser.open(f"http://localhost:{PORT}")
        print("已在电脑浏览器中打开应用...")
    except:
        pass
    
    # 启动服务器
    with socketserver.TCPServer(("0.0.0.0", PORT), CORSRequestHandler) as httpd:
        print(f"服务器已启动，监听端口 {PORT}...")
        print("正在等待连接...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
        except Exception as e:
            print(f"服务器错误: {e}")

if __name__ == "__main__":
    main()