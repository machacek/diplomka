from django.db import models
from model_utils.managers import InheritanceManager
from annotate.models import Project
from django.contrib.auth.models import User

class RankProject(Project):
    instructions = models.TextField()

class Item(models.Model):
    project = models.ForeignKey(RankProject, related_name='items')
    sentence_id = models.IntegerField()
    source_sen = models.TextField()
    source_seg = models.TextField()
    candidate_segs = models.TextField()

class Annotation(models.Model):
    annotated_item = models.ForeignKey(Item, related_name='annotations')
    ranks = models.TextField()
    annotator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)    
