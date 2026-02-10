from model.subject import Subject
from model.subjects import Subjects

sub=Subjects()
sub1=Subject("sub1","Toán cao cấp",4, 9,9,10)
sub2=Subject("sub2","Lập trình hướng đối tượng",3,8,7,9)
sub3=Subject("sub3","Nền tảng công nghệ",2,7,8,9)
sub4=Subject("sub4","Kinh tế vĩ mô",3,6,7,8)
sub5=Subject("sub5","Kinh tế vi mô",3,8,9,9)
sub6=Subject("sub6","năng lực số ",2,9,7,9)
sub.add_items([sub1,sub2,sub3,sub4,sub5,sub6])
print("Danh sách môn học")
sub.print_items()
print("Xuất assets ra Json:")
sub.export_json("../datasets/subjects.json")