from django.db import models

# Create your models here.
class Report(models.Model):
    pantip_id = models.CharField(max_length=50)
    report_data = models.CharField(max_length=255)
    status = models.CharField(max_length=20,default='wait')
    edit_user = models.CharField(max_length=50,default='-')
    
