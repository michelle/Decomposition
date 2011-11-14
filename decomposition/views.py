from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from decomposition.list.models import Assignment, Problem, Note
from django.utils import simplejson
from ast import literal_eval
import datetime

def isAuthUser( request ):
    return request.user if request.user.is_authenticated() else None

def render_to_responseC( request, link, context ):
    context.update( csrf( request ) )
    return render_to_response( link, context )

def dashboard( request ):
    inGuy = isAuthUser( request )
    All = Assignment.objects.filter( user=inGuy )
    AA = All.filter( active=True )
    iAA = All.filter( active=False )
    if request.method == 'POST' and inGuy:
        kind = request.POST['kind']
        id = request.POST['id']
        if kind == "remo":
            AssignmentObj = iAA.get( id=id )
            AssignmentObj.delete()
        elif kind == "inact":
            AssignmentObj = AA.get( id=id )
            AssignmentObj.active = False
            AssignmentObj.save()
        else:
            assert False
    return render_to_responseC( request, 'dashboard.html', locals() )

def about( request ):
    inGuy = isAuthUser( request )
    return render_to_responseC( request, 'about.html', locals() )

def create( request ):
    inGuy = isAuthUser( request )
    if request.method == 'POST' and inGuy:
        problems = literal_eval(request.POST['problems'])
        title = request.POST['title']
        if not title:
            title = "Untitled"
        AssignmentObj = Assignment( user=inGuy,
                                    title=title,
                                    due=datetime.datetime.now(),
                                    numofprobs=len(problems))
        AssignmentObj.save()
        if not problems: problems = [{}]
        for i, problem in enumerate(problems):
            title = problem[ 'question' ] if problem[ 'question' ] else ( "Problem :" + str( i + 1 ) )
            ProblemObj = Problem( Ass=AssignmentObj,
                                  title=problem[ 'question' ],
                                  index=i+1,
                                  )
            ProblemObj.save()
        return HttpResponse(simplejson.dumps({"success":"Your crap has been successfully saved" }), 'application/json' )
    return render_to_responseC( request, 'create.html', locals() )

def assign( request, id ):
    inGuy = isAuthUser( request )
    if request.method == 'POST':
        kind = request.POST['kind']
        id1 = request.POST['id' ]
        if kind == "minusProb":
            ProblemObj = Problem.objects.get( id=id1 )
            if not ProblemObj.complete:
                AssignmentObj = Assignment.objects.get( id=id )
                AssignmentObj.doneprobs += 1
                AssignmentObj.save()
            ProblemObj.complete = True
            ProblemObj.save()
        elif kind == "plus":
            ProblemObj = Problem.objects.get( id=id1 )
            text = request.POST['text' ]
            NoteObj = Note( prob=ProblemObj,
                            text=text)
            NoteObj.save()
        else:
            assert False, kind
    try:
        assignment = Assignment.objects.get( id=id )
        problems = Problem.objects.filter( Ass=assignment ).order_by( "id" )
    except:
        # Direct to template 404 or something
        assert False
    return render_to_responseC(request, 'assignment.html', locals() )
    

def gen( request ):
    user, password = 'doboy', 'pis321'
    UserObject = None
    if not User.objects.filter( username=user ):
        UserObject = User( username=user, password = password )
        UserObject.save()
    else:
        UserObject = User.objects.get( username=user )
    
    # Create two assignemnts for the user
    for title, numofprobs, due in [ ('Physics 1.2', 3, datetime.datetime.now()),
                                    ('Math 1.2', 4, datetime.datetime.now()),
                                    ]:
        AssignObject = Assignment( user=UserObject,
                                   title=title,
                                   numofprobs=numofprobs,
                                   due=due )
        AssignObject.save()
        for problemi in xrange( numofprobs ):
            ProblemObject = Problem( Ass = AssignObject,
                                     index = problemi)
            ProblemObject.save()
            for notei in xrange( 3 ):
                NoteObject = Note( text="this is a hard problem",
                                   prob=ProblemObject )
                NoteObject.save()
    return HttpResponse( 'itz done' )

def register( request ):
    if request.method == 'POST':
        form = UserCreationForm( request.POST )
        if form.is_valid():
            new_user = form.save()
            success = "Registration successfully, you can login now"
            return render_to_responseC( request, 'success.html', locals() )
    else:
        form = UserCreationForm()
    return render_to_responseC( request, "registration/register.html", locals() )
