class UpcomingEvent:
    def __init__(self, date_month=None,sukien=None):
        self.date_month = date_month
        self.sukien = sukien
    def __str__(self):
        infor=f"{self.date_month}\t{self.sukien}"
        return infor