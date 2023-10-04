# from django.db import models

# class FailedLoginAttempt(models.Model):
#     ip_address = models.GenericIPAddressField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     # Add any other relevant fields



from django.db import models

class TaskResult(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    result = models.TextField(null=True)
    ip_address = models.GenericIPAddressField(default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    xss_number = models.IntegerField(default=0)
