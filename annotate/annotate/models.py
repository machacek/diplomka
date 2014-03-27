from django.db import models
from model_utils.managers import InheritanceManager

class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)

    # For selecting subclasses
    objects = InheritanceManager()

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name

