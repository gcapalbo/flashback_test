import pytz
import datetime
from django.db import models

class Log(models.Model):
    timestamp = models.DateTimeField()
    direction = models.CharField(max_length = 50)
    type = models.CharField(max_length = 50)
    number = models.CharField(max_length = 50)
    message = models.CharField(max_length = 160, blank=True, null=True)

def log(direction, type, number, message=None):
    l = Log(
        timestamp = datetime.datetime.now(tz=pytz.utc)
       ,direction = direction
       ,type = type
       ,number = number
       ,message = message
    )
    l.save()

