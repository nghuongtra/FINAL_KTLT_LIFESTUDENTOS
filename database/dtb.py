import sqlite3
import os


class DatabaseManager:
    def __init__(self, db_name="student_life.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__)) # Đảm bảo file DB luôn nằm cùng cấp với thư mục dự án, không bị chạy lung tung
        db_path = os.path.join(base_dir, "..", db_name) ## Lưu file db ra ngoài thư mục database một cấp để dễ quản lý

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.initialize_tables()

    def initialize_tables(self):
        # 1. Bảng Users (Lưu tên người dùng)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Bảng Tasks (Cho Widget To-Do List)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                deadline TEXT,
                status INTEGER DEFAULT 0, -- 0: Chưa xong, 1: Xong
                category TEXT
            )
        """)

        # 3. Bảng Schedule (Cho Thời khóa biểu)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_name TEXT NOT NULL,
                day_of_week TEXT, -- Mon, Tue, Wed...
                start_time TEXT,
                end_time TEXT,
                color_hex TEXT
            )
        """)

        self.conn.commit()
        print(">>> Database & Tables created successfully!")

    def add_user(self, name):
        try:
            self.cursor.execute("INSERT INTO users (username) VALUES (?)", (name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Tên đã tồn tại

    def close(self):
        self.conn.close()