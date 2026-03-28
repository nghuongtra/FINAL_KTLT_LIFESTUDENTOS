# class Subject:
#    def __init__(self, Subname, credit=None, scoreProcess=None, scoreMidterm=None, scoreFinal=None):
#        self.Subname = Subname
#        self.credit = credit
#        self.scoreProcess = scoreProcess
#        self.scoreMidterm = scoreMidterm
#        self.scoreFinal = scoreFinal
#
#
#    def tinh_diem_gpa(self):
#        # Công thức tính GPA hệ 10: (QT*0.2 + GK*0.3 + CK*0.5)
#        dtb = (self.scoreProcess * 0.3) + (self.scoreMidterm * 0.2) + (self.scoreFinal * 0.5)
#        return round(dtb, 2)
#
#
#    def tinh_xep_loai(self):
#        dtb = self.tinh_diem_gpa()
#        if dtb >= 9.0: return "A+"
#        elif 8.0 <= dtb < 9.0: return "A"
#        elif 7.0 <= dtb < 8.0: return "B+"
#        elif 6.0 <= dtb < 7.0: return "B"
#        elif 5.0 <= dtb < 6.0: return "C"
#        elif 4.0 <= dtb < 5.0: return "D"
#        else: return "F"
#
#
#    def __str__(self):
#        return f"{self.Subname}  {self.tinh_diem_gpa()}"
#
class Subject:
    def __init__(self, Subname, credit=0, components=None):
        self.Subname = Subname
        self.credit = credit
        # components sẽ lưu danh sách các cột điểm:
        # VD: [{"name": "QT", "weight": 30, "score": 8.0}, {"name": "CK", "weight": 70, "score": 9.0}]
        self.components = components if components is not None else []

    def tinh_diem_gpa(self):
        if not self.components:
            return 0.0

        dtb = 0.0
        # Công thức tự động: Tổng của (Điểm * Trọng số / 100)
        for comp in self.components:
            dtb += comp['score'] * (comp['weight'] / 100.0)

        return round(dtb, 2)

    def tinh_xep_loai(self):
        dtb = self.tinh_diem_gpa()
        if dtb >= 9.0:
            return "A+"
        elif 8.0 <= dtb < 9.0:
            return "A"
        elif 7.0 <= dtb < 8.0:
            return "B+"
        elif 6.0 <= dtb < 7.0:
            return "B"
        elif 5.0 <= dtb < 6.0:
            return "C"
        elif 4.0 <= dtb < 5.0:
            return "D"
        else:
            return "F"

    def __str__(self):
        return f"{self.Subname} - Tín chỉ: {self.credit} - GPA: {self.tinh_diem_gpa()}"