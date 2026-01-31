import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.dtb import DatabaseManager


class TestDatabase(unittest.TestCase):
    def test_connection_and_table_creation(self):
        print("\n--- Đang test khởi tạo Database ---")
        db = DatabaseManager("test_student_app.db")

        # Kiểm tra xem bảng tasks đã được tạo chưa
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks';")
        result = db.cursor.fetchone()
        self.assertIsNotNone(result, "Lỗi: Bảng 'tasks' chưa được tạo!")
        print("[OK] Bảng 'tasks' đã tồn tại.")

        # Kiểm tra thêm user
        print("--- Đang test thêm User ---")
        is_added = db.add_user("TestUser_Leader")
        self.assertTrue(is_added, "Lỗi: Không thêm được user!")
        print("[OK] Thêm User thành công.")

        db.close()
        # Dọn dẹp file test sau khi chạy xong (xóa file db ảo)
        if os.path.exists("../test_student_app.db"):
            os.remove("../test_student_app.db")


if __name__ == '__main__':
    unittest.main()