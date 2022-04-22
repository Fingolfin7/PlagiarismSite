from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class History(models.Model):
    doc1 = models.TextField()
    doc2 = models.TextField()
    similarity = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "History"

    """def __str__(self):
        return f"Date: {self.date}"""


