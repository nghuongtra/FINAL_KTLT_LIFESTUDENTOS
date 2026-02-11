from model.comingevents import Upcomingevents

ucvs=Upcomingevents()
ucvs.import_json("../datasets/upcomingevents.json")
print("Danh sach Asset")
ucvs.print_items()