from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import User


# Create your models here.

class Box(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.FloatField()
    volume = models.FloatField()

