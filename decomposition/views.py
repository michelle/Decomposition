from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from decomposition.list.models import Assignment, Problem, Note
import datetime

def isAuthUser( request ):
    return request.user if request.user.is_authenticated() else None

def dashboard( request ):
    inGuy = isAuthUser( request )
    Activeassignments = Assignment.objects.filter( user=inGuy )
    # assert False, Activeassignments
    return render_to_response( 'dashboard.html', locals() )

def gen( request ):
    user, password = 'doboy', 'pis321'
    UserObject = None
    if not User.objects.filter( username=user ):
        UserObject = User( username=user, password = password )
        UserObject.save()
    else:
        UserObject = User.objects.get( username=user )
    
    # Create two assignemnts for the user
    for title, due in [ ('Physics 1.2', datetime.datetime.now()),
                        ('Math 1.2', datetime.datetime.now()),
                        ]:
        AssignObject = Assignment( User=UserObject,
                                   title=title,
                                   due=due )
        AssignObject.save()
