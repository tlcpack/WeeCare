import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Prefetch
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.decorators.http import require_http_methods
from .models import Child, Activity, Guardian, Classroom, Visit
from .forms import CommentForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse



# def base
def index(request):

    children = ()
    classroom = ()

    
    children = Child.objects.all()
    children = Child.objects.prefetch_related(
                Prefetch(
                    "visits",
                    queryset=Visit.objects.filter(check_out__isnull=True, check_in__date__lte=datetime.date.today()),
                    to_attr="visit"
                )
            ).order_by('full_name')
        
    

    


    context = {
        'children': children,

        'classrooms' : classroom,
    }

    return render(request, 'index.html', context=context)


def action_list(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    activity = visit.activities
    nap = Activity.objects.filter(visit_id=visit_id, activity_type=Activity.NAP, end_time__isnull=True)
    context = {
        'activity': activity,
        'visit': visit,
        'child': visit.child,
        'visit_id': visit_id,
        'open_nap': nap,
    }
    return render(request, 'action_list.html', context=context)


def action_summary(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    comment = visit.comment
    naps = Activity.objects.filter(visit_id=visit_id, activity_type=Activity.NAP)
    outputs = Activity.objects.filter(visit_id=visit_id, activity_type=Activity.OUTPUT)
    inputs = Activity.objects.filter(visit_id=visit_id, activity_type=Activity.INPUT)
    child = visit.child
    guardians = child.guardians.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            if visit.comment is None:
                visit.comment = " - " + form.cleaned_data['comment']
            else:
                visit.comment += "\n - " + (form.cleaned_data['comment'])
            visit.save()

        return redirect('action_summary', visit_id=visit_id)

    else:
        form = CommentForm()

    context = {
        'form': form,
        'guardians': guardians,
        'naps': naps,
        'visit': visit,
        'child': child,
        'visit_id': visit_id,
        'outputs': outputs,
        'inputs': inputs,
        'comment': comment,
    }

    return render(request, 'action_summary.html', context=context)

def in_list(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    context = {
        'visit_id' : visit_id,
        'visit': visit,
        }
    return render(request, 'in_list.html', context=context)


@require_http_methods(['POST'])
def bottle(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    option = request.POST['bottle_choice']
    bottle = Activity(
        activity_type=Activity.INPUT,
        subtype='bottle',
        subtype_option=option,
        visit=visit,
        child=visit.child,
    )
    bottle.save()
    

    return redirect('index')


@require_http_methods(['POST'])
def diaper(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    option = request.POST['diaper_choice']
    diaper = Activity(
        activity_type=Activity.OUTPUT,
        subtype='diaper',
        subtype_option=option,
        visit=visit,
        child=visit.child,
    )
    diaper.save()
    
   
    return redirect('index')


@require_http_methods(['POST'])
def nurse(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    option = request.POST['nurse_choice']
    nurse = Activity(
        activity_type=Activity.INPUT,
        subtype='nursing',
        subtype_option=option,
        visit=visit,
        child=visit.child
    )
    nurse.save()
    

    return redirect('index')


@require_http_methods(['POST'])
def food(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    option = request.POST['food_choice']
    food = Activity(
        activity_type=Activity.INPUT,
        subtype='food',
        subtype_option=option,
        visit=visit,
        child=visit.child
    )
    food.save()
    

    return redirect('index')


def check_out(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    visit.check_out = timezone.now()
    naps = Activity.objects.filter(visit_id=visit_id, activity_type=Activity.NAP)
    outputs = Activity.objects.filter(visit_id=visit_id, activity_type=Activity.OUTPUT)
    child = visit.child
    
    inputs = Activity.objects.filter(visit_id=visit_id, activity_type=Activity.INPUT)
    comment = visit.comment


    context = {
    'naps': naps,
    'visit': visit,
    'child': child,
    'visit_id': visit_id,
    'outputs': outputs,
    'inputs': inputs,
    'comment': comment,
    } 

    

    return redirect('index')


def check_in(request, child_id):
    child = Child.objects.get(child_id=child_id)
    visit = Visit(
        child=child
    )
    visit.save()
    

    return redirect('index')


def nap_out(request, activity_id):
    nap = Activity.objects.get(id=activity_id)
    nap.end_time = timezone.now()
    nap.save()
    

    return redirect('index')


def nap_in(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    nap = Activity(
        activity_type=Activity.NAP,
        visit=visit,
        child=visit.child,
    )
    nap.save()
    

    return redirect('index')


def change_notification(request):
    visits = Visit.objects.filter(check_out__isnull=True)
    change_list = []
    
    for visit in visits:
        if visit.child in Child.objects:
            activities = visit.activities
            outputs = list(activities.filter(activity_type=Activity.OUTPUT))
            timedelta = datetime.timedelta(seconds=30)
            
            if outputs == []:
                latest_output = visit
                change_timer = timezone.now() - latest_output.check_in


            else:
                latest_output = outputs[-1]
                change_timer = timezone.now() - latest_output.start_time
                
                if latest_output.subtype_option == 'Dry':
                    timedelta = datetime.timedelta(seconds=15)


            if change_timer > timedelta:
                change_list.append(latest_output.child.child_id)

    context = {
        'change_list': change_list,
    }           

    return JsonResponse(context)

def feed_notification(request):
    visits = Visit.objects.filter(check_out__isnull=True)
    feed_list = []

    for visit in visits:
        if visit.child in Child.objects:
            activities = visit.activities
            inputs = list(activities.filter(activity_type=Activity.INPUT))

            if inputs == []:
                latest_input = visit
                feed_timer = timezone.now() - latest_input.check_in

            else:
                latest_input = inputs[-1]
                feed_timer = timezone.now() - latest_input.start_time

            if feed_timer > datetime.timedelta(seconds=30):
                feed_list.append(latest_input.child.child_id)

    context = {
        'feed_list': feed_list,
    }

    return JsonResponse(context)

def nap_notification(request):
    visits=Visit.objects.filter(check_out__isnull=True)
    nap_list = []

    for visit in visits:
        if visit.child in Child.objects:
            naps = visit.activities.filter(activity_type=Activity.NAP)

            for nap in naps:
                if nap.end_time is None:
                    nap_list.append(nap.child.child_id)
                
    context = {
        'nap_list': nap_list,
    }

    return JsonResponse(context)
