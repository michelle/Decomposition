from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Assignment( models.Model ):
    user = models.ForeignKey( User )
    title = models.CharField(max_length=100)
    due = models.DateTimeField()
    
class Problem( models.Model ):
    Ass = models.ForeignKey( Assignment )
    title = models.CharField( max_length=100 )
    
class Note( models.Model ):
    Prob = models.ForeignKey( Problem )
    text = models.CharField( max_length=100 )
