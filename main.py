#!/usr/bin/env python3
"""
Script tự động hóa cấu hình User 'devops' và Sudoers trên Ubuntu Server.
"""
import os
import sys
import subprocess

USERNAME = "devops"

def run_command(cmd, check=True):
    print(f"[EXEC] {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"[ERROR] Lỗi khi thực thi lệnh: {cmd}")
        print(f"[STDERR] {result.stderr.strip()}")
        sys.exit(result.returncode)
    return result

def check_root():
    if os.geteuid() != 0:
        print("[ERROR] Rất tiếc, kịch bản này cần quyền root để chạy. Vui lòng thử lại với 'sudo python3 main.py'.")
        sys.exit(1)

def setup_user():
    print(f"=== 1. Khởi tạo người dùng '{USERNAME}' ===")
    user_check = run_command(f"id -u {USERNAME}", check=False)
    if user_check.returncode == 0:
        print(f"[-] Người dùng '{USERNAME}' đã tồn tại.")
    else:
        run_command(f"adduser --disabled-password --gecos '' {USERNAME}")
        print(f"[+] Đã tạo thành công người dùng '{USERNAME}'.")

    print(f"\n=== 2. Thêm '{USERNAME}' vào nhóm sudo ===")
    run_command(f"usermod -aG sudo {USERNAME}")
    print(f"[+] Đã thêm '{USERNAME}' vào nhóm sudo.")

    print(f"\n=== 3. Sao chép và Phân quyền SSH Key ===")
    root_ssh = os.path.expanduser("/root/.ssh")
    user_ssh = f"/home/{USERNAME}/.ssh"
    user_auth_keys = f"{user_ssh}/authorized_keys"

    if os.path.exists(root_ssh):
        run_command(f"rsync --archive --chown={USERNAME}:{USERNAME} {root_ssh}/ {user_ssh}/")
        print(f"[+] Đã sao chép thư mục SSH từ root sang {user_ssh}")
    else:
        os.makedirs(user_ssh, mode=0o700, exist_ok=True)
        run_command(f"chown -R {USERNAME}:{USERNAME} {user_ssh}")
        print(f"[!] Không tìm thấy {root_ssh}. Đã khởi tạo thư mục trống {user_ssh}")

    # Thiết lập phân quyền chuẩn bảo mật SSH
    run_command(f"chmod 700 {user_ssh}")
    if os.path.exists(user_auth_keys):
        run_command(f"chmod 600 {user_auth_keys}")
        run_command(f"chown {USERNAME}:{USERNAME} {user_auth_keys}")
    print(f"[+] Đã phân quyền chuẩn bảo mật: 700 cho {user_ssh} và 600 cho {user_auth_keys}")

def verify_setup():
    print(f"\n=== 4. Kiểm tra cấu hình ===")
    groups_res = run_command(f"groups {USERNAME}", check=False)
    print(f"Nhóm của user: {groups_res.stdout.strip()}")
    
    user_ssh = f"/home/{USERNAME}/.ssh"
    ls_res = run_command(f"ls -ld {user_ssh}", check=False)
    print(f"Thư mục SSH: {ls_res.stdout.strip()}")
    
    print("\n[SUCCESS] Hoàn tất thiết lập tài khoản devops!")

if __name__ == "__main__":
    check_root()
    setup_user()
    verify_setup()
