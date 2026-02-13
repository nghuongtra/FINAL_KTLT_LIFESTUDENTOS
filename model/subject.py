class Subject:
   def __init__(self, Subname, credit=None, scoreProcess=None, scoreMidterm=None, scoreFinal=None):
       self.Subname = Subname
       self.credit = credit
       self.scoreProcess = scoreProcess
       self.scoreMidterm = scoreMidterm
       self.scoreFinal = scoreFinal


   def tinh_diem_gpa(self):
       # Công thức tính GPA hệ 10: (QT*0.2 + GK*0.3 + CK*0.5)
       dtb = (self.scoreProcess * 0.2) + (self.scoreMidterm * 0.3) + (self.scoreFinal * 0.5)
       return round(dtb, 2)


   def tinh_xep_loai(self):
       dtb = self.tinh_diem_gpa()
       if dtb >= 9.0: return "A+ (Xuất Sắc)"
       elif 8.0 <= dtb < 9.0: return "A (Giỏi)"
       elif 7.0 <= dtb < 8.0: return "B+ (Khá)"
       elif 6.0 <= dtb < 7.0: return "B+ (Trung Bình Khá)"
       elif 5.0 <= dtb < 6.0: return "C (Trung Bình)"
       elif 4.0 <= dtb < 5.0: return "D+ (Yếu)"
       else: return "F (Kém)"


   def __str__(self):
       return f"{self.Subname}  {self.tinh_diem_gpa()}"

