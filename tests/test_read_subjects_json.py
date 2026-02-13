from model.subjects import Subjects
subs = Subjects()
subs.import_json("../datasets/subjects.json")
print("Danh sách môn học và điểm số:")
subs.print_items()

