# 🎓 Student Life OS - Đồ án Kỹ thuật Lập trình

> **Hệ điều hành cá nhân dành cho sinh viên** - Quản lý học tập, công việc và sức khỏe.
> *Project Leader: Nguyễn Hương Trà*

## 📋 GIỚI THIỆU
Đây là mã nguồn chính thức của đồ án cuối kỳ. Dự án được xây dựng theo mô hình MVC (Model-View-Controller) đơn giản hóa, sử dụng cơ sở dữ liệu SQLite để lưu trữ cục bộ.


## 🚀 HƯỚNG DẪN CÀI ĐẶT (Dành cho thành viên nhóm)

Mọi người làm theo đúng 4 bước sau để môi trường code đồng bộ nha:

### Bước 1: Clone dự án về máy
Mở **PyCharm**, chọn **Get from VCS** và dán đường dẫn sau:

```
https://github.com/nghuongtra/FINAL_KTLT_LIFESTUDENTOS.git
```
### Bước 2: Cài đặt thư viện (QUAN TRỌNG)
Sau khi tải về, PyCharm thường sẽ tự động hỏi tạo môi trường ảo (Virtual Environment), các bạn bấm OK.

Sau đó, mở tab Terminal ở góc dưới bên trái PyCharm (nhìn xem đầu dòng có chữ (.venv) là đúng) và chạy lệnh này để cài môi trường giống máy tui
```
pip install -r requirements.txt
```

### Bước 3: Chạy chương trình
```
python main.py
```
### QUY TẮC LÀM VIỆC (BẮT BUỘC ĐỌC)
Để tránh xung đột code (Conflict), mọi người nên:
1. Quy trình Push Code (4 Bước chuẩn)

B1: Luôn lấy code mới nhất về trước khi làm
```
git pull origin main
```


B2: Thêm các file đã sửa vào danh sách chờ
```
git add .
```
B3: Đóng gói và ghi chú
```
git commit -m "Ghi chú rõ ràng nội dung làm"
```

B4: Đẩy code lên GitHub
```
git push origin main
```
## 🚀Lưu ý:
Sau khi code xong tính năng thì phải TEST trước khi đưa nó vào file main để tránh bị lỗi cả hệ thống nha
### Cảm ơn các bạn nhiều hihi :3333333