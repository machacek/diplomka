from django.db import models
from model_utils.managers import InheritanceManager
from annotate.models import Project
from django.contrib.auth.models import User

class RankProject(Project):
    instructions = models.TextField()

class Sentence(models.Model):
    project = models.ForeignKey(RankProject, related_name='sentences')
    sentence_id = models.IntegerField()
    source_str = models.TextField()
    reference_str = models.TextField()

class Segment(models.Model):
    sentence = models.ForeignKey(Sentence, related_name='segments')
    segment_str = models.TextField()
    candidates_str = models.TextField()

class Annotation(models.Model):
    annotated_segment = models.ForeignKey(Segment, related_name='annotations')
    ranks = models.TextField()
    annotator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)    
