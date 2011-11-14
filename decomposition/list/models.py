from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Assignment( models.Model ):
    user = models.ForeignKey( User )
    title = models.CharField(max_length=500)
    due = models.DateTimeField()
    active = models.BooleanField(default=True)
    doneprobs = models.IntegerField(default=0)
    numofprobs = models.IntegerField()

    def calculatePercent(self):
        try:
            return int(self.doneprobs/float(self.numofprobs)*100)
        except:
            return "infinity"

    percent = property(calculatePercent)

class Problem( models.Model ):
    Ass = models.ForeignKey( Assignment )
    title = models.CharField( max_length=500 )
    complete = models.BooleanField(default=False)
    index = models.IntegerField()
    
    def calculateNotes(self):
        return Note.objects.filter(prob=self)

    notes = property(calculateNotes)
    

class Note( models.Model ):
    text = models.CharField( max_length=500 )    
    prob = models.ForeignKey( Problem )
