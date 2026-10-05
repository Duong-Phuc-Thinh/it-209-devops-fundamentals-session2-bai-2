# Bài tập 2: Cấu hình trang lỗi tùy chỉnh (Custom Error Page 404)

Thư mục này chứa toàn bộ tài nguyên cấu hình trang lỗi 404 tùy biến cho Nginx Web Server theo đúng yêu cầu bảo mật.

## Danh sách tệp tin

1. `404.html`: Tệp tin giao diện HTML báo lỗi thân thiện được thiết kế đẹp mắt.
2. `nginx_server_block.conf`: File mẫu cấu hình Server Block của Nginx bao gồm việc thiết lập trang 404 và khóa chỉ thị `internal`.
3. `deploy.py`: Script Python tự động hóa việc triển khai thư mục gốc và cấu hình tệp tin tĩnh sang `/var/www/my-web/html/`.

## Hướng dẫn triển khai

### Bước 1: Triển khai tệp HTML
Chạy Script Python bằng quyền `root` để khởi tạo thư mục và đưa trang `404.html` vào đúng vị trí:
```bash
sudo python3 deploy.py
```
Hoặc bạn có thể sao chép thủ công:
```bash
sudo mkdir -p /var/www/my-web/html
sudo cp 404.html /var/www/my-web/html/
sudo chmod 644 /var/www/my-web/html/404.html
```

### Bước 2: Cập nhật cấu hình Nginx
Sao chép nội dung cấu hình trong tệp `nginx_server_block.conf` và dán vào file cấu hình Server Block của bạn (thường tại `/etc/nginx/sites-available/default` hoặc file config tương ứng).

### Bước 3: Áp dụng cấu hình
Kiểm tra cú pháp cấu hình Nginx xem có hợp lệ không:
```bash
sudo nginx -t
```
Nếu kết quả trả về thành công (`syntax is ok` / `test is successful`), hãy tiến hành reload dịch vụ Nginx:
```bash
sudo systemctl reload nginx
```

## Kiểm tra cấu hình (Testing)

- **Trường hợp 1: Truy cập đường dẫn không tồn tại**
  ```bash
  curl -I http://localhost/invalid-path-demo
  ```
  *Kết quả mong đợi*: Trả về status code `404 Not Found` đi kèm nội dung trang HTML đã tùy biến.

- **Trường hợp 2: Truy cập trực tiếp file `404.html` qua URL**
  ```bash
  curl -I http://localhost/404.html
  ```
  *Kết quả mong đợi*: Trả về `404 Not Found` (Nginx chặn truy cập trực tiếp nhờ cơ chế chỉ thị `internal`).