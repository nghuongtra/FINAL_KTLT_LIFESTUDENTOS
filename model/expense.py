import datetime
class Expense:
    def __init__(self,khoan_chi,so_tien,danh_muc,ghi_chu,ngay=None):
        self.ngay=ngay if ngay else datetime.date.today().strftime("%d/%m/%Y")
        self.khoan_chi= khoan_chi
        self.so_tien=so_tien
        self.danh_muc=danh_muc
        self.ghi_chu=ghi_chu
    def to_dict(self):
        return self.__dict__
