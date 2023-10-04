from app.models import TaskResult

# Creating a new instance and saving
task = TaskResult(task_id='12345', result='Test Result', ip_address='127.0.0.1')
task.save()

# Querying to check
if TaskResult.objects.filter(task_id='12345').exists():
    print("Data saved successfully!")
else:
    print("Data not saved.")
