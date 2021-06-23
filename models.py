from django.db import models

class IDGenieSession(models.Model):
    code = models.CharField(max_length=36)
    is_valid = models.BooleanField(default=False)
