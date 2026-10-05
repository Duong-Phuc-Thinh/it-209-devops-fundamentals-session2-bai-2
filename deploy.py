import os
import sys
import shutil
import subprocess

HTML_SRC = "404.html"
CONF_SRC = "nginx_server_block.conf"
HTML_DEST_DIR = "/var/www/my-web/html"

def setup_environment():
    print("[+] Bắt đầu thiết lập trang lỗi 404 tùy chỉnh...")
    
    # 1. Tạo thư mục chứa html nếu chưa tồn tại
    if not os.path.exists(HTML_DEST_DIR):
        try:
            os.makedirs(HTML_DEST_DIR, exist_ok=True)
            print(f"[-] Đã tạo thư mục: {HTML_DEST_DIR}")
        except PermissionError:
            print(f"[ERROR] Không có quyền tạo thư mục {HTML_DEST_DIR}. Vui lòng chạy bằng quyền root (sudo).")
            sys.exit(1)

    # 2. Sao chép tệp 404.html
    try:
        shutil.copy(HTML_SRC, os.path.join(HTML_DEST_DIR, "404.html"))
        print(f"[-] Đã sao chép {HTML_SRC} -> {HTML_DEST_DIR}/404.html")
        os.chmod(os.path.join(HTML_DEST_DIR, "404.html"), 0o644)
    except PermissionError:
        print("[ERROR] Không có quyền sao chép file. Vui lòng chạy bằng quyền root (sudo).")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[ERROR] Không tìm thấy file nguồn {HTML_SRC}.")
        sys.exit(1)

    print("\n[+] Cấu hình thành công mã HTML.")
    print(f"Vui lòng áp dụng cấu hình trong file '{CONF_SRC}' vào Server Block của Nginx.")
    print("Thực hiện kiểm tra cú pháp Nginx và khởi động lại:")
    print("  sudo nginx -t")
    print("  sudo systemctl reload nginx\n")

if __name__ == "__main__":
    setup_environment()