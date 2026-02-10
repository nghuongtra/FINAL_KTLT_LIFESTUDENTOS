class Subject:
    def __init__(self,Subid=None, Subname=None, credit=None, scoreProcess=None, socreMidterm=None, scoreFinal=None):
        self.Subid = Subid
        self.Subname = Subname
        self.credit = credit
        self.scoreProcess = scoreProcess
        self.scoreMidterm = socreMidterm
        self.scoreFinal = scoreFinal

    def __str__(self):
        infor=(f"{self.Subid}\t{self.Subname}\t{self.credit}\t"
               f"{self.scoreProcess}\t{self.scoreMidterm}\t{self.scoreFinal}")
        return infor