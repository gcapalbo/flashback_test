import pytz
import datetime
from django.db import models

class Log(models.Model):
    timestamp = models.DateTimeField()
    direction = models.CharField(max_length = 50)
    type = models.CharField(max_length = 50)
    number = models.CharField(max_length = 50, blank=True, null=True)
    message = models.CharField(max_length = 160, blank=True, null=True)
    backend = models.CharField(max_length = 50)
    post_data = models.CharField(max_length = 32000, blank=True, null=True)

def log(direction, type, number, backend, post_data=None, message=None):
    l = Log(
        timestamp = datetime.datetime.now(tz=pytz.utc)
       ,direction = direction
       ,type = type
       ,number = number
       ,message = message
       ,backend = backend
       ,post_data = post_data
    )
    l.save()

