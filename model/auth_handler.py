import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


load_dotenv()


class AuthManager:
   def __init__(self):
       pass


   def send_password_to_mail(self, receiver_email, username, password_to_send):
       #Hàm gửi trực tiếp mật khẩu cũ cho người dùng qua Email
       sender = os.getenv("EMAIL_USER")
       sender_password = os.getenv("EMAIL_PASS")


       if not sender or not sender_password:
           print("Lỗi cấu hình")
           return False


       body = f"""
       Chào {username},
       Bạn vừa yêu cầu lấy lại mật khẩu từ hệ thống LifeStudentOS.
       Mật khẩu của bạn là: {password_to_send}
       Vui lòng dùng mật khẩu này để đăng nhập và bảo mật thông tin!
       """


       msg = MIMEText(body)
       msg['Subject'] = 'Lay lai mat khau tai khoan - LifeStudentOS'
       msg['From'] = f"LifeStudentOS <{sender}>"
       msg['To'] = receiver_email


       try:
           server = smtplib.SMTP('smtp.gmail.com', 587)
           server.starttls()
           server.login(sender, sender_password)
           server.send_message(msg)
           server.quit()
           return True
       except Exception as e:
           print(f"Lỗi gửi mail: {e}")
           return False

