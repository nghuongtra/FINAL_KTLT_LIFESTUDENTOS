from model.tasks import Tasks

task=Tasks()
task.import_json("../datasets/tasks.json")
print("Danh sách tasks")
task.print_items()