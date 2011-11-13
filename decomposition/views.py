from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from decomposition.list.models import Assignment, Problem, Note
import datetime

def isAuthUser( request ):
    return request.user if request.user.is_authenticated() else None

def render_to_responseC( request, link, context ):
    context.update( csrf( request ) )
    return render_to_response( link, context )

def dashboard( request ):
    inGuy = isAuthUser( request )
    Activeassignments = Assignment.objects.filter( user=inGuy )
    # assert False, Activeassignments
    return render_to_response( 'dashboard.html', locals() )

def create( request ):
    inGuy = isAuthUser( request )
    if request.method == 'POST' and inGuy:
        AssingmentObj = Assignment( user=inGuy,
                                    title=request.POST['title'],
                                    due=datetime.datetime.now() )
        AssingmentObj.save()
        success = True
    return render_to_responseC( request, 'create.html', locals() )

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
        AssignObject = Assignment( user=UserObject,
                                   title=title,
                                   due=due )
        AssignObject.save()
    return HttpResponse( 'itz done' )
