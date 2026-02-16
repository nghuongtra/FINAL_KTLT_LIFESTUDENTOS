from model.insights import Insights
ins= Insights()
ins.import_json("../datasets/insights.json")
print("In danh sách")
ins.print_items()

