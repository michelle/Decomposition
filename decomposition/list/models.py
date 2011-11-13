from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Assignment( models.Model ):
    user = models.ForeignKey( User )
    title = models.CharField(max_length=100)
    due = models.DateTimeField()
    active = models.BooleanField(default=True)
    numofprobs = models.IntegerField()

class Problem( models.Model ):
    Ass = models.ForeignKey( Assignment )
    title = models.CharField( max_length=100 )
    complete = models.BooleanField(default=True)
    text = models.CharField( max_length=100 )    
    index = models.IntegerField()
