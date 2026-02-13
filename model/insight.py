class Insight:
    def __init__(self, gpa=None, tien_do=None, so_du=None, short_comment=None, advice=None, tips=None, top_spending=None,ngay_thang=None):
        self.gpa = gpa
        self.tien_do = tien_do
        self.so_du = so_du
        self.short_comment = short_comment
        self.advice = advice
        self.tips = tips
        self.top_spending = top_spending
        self.ngay_thang = ngay_thang
    def __str__(self):
        return f"[{self.short_comment}] GPA: {self.gpa} | Tiền: {self.so_du}"