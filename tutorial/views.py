from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection


# Create your views here.

def listing(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tutorial, topics WHERE tutorial_topic_id = topics_id")
    tutoriallist = dictfetchall(cursor)

    context = {
        "tutoriallist": tutoriallist
    }

    # Message according medicines Role #
    context['heading'] = "tutorial Details";
    return render(request, 'tutorial-details.html', context)

def lists(request, id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tutorial, topics WHERE tutorial_topic_id = topics_id AND topics_id = " + id)
    tutoriallist = dictfetchall(cursor)

    context = {
        "tutoriallist": tutoriallist
    }

    # Message according medicines Role #
    context['heading'] = "tutorial Details";
    return render(request, 'tutorial-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tutorial WHERE tutorial_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, tutorialId):
    context = {
        "fn": "update",
        "tutorialDetails": getData(tutorialId),
        "topicslist": getDropDown('topics', 'topics_id'),
        "heading": 'Update tutorial',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE tutorial
                   SET tutorial_title=%s, tutorial_description=%s, tutorial_topic_id=%s WHERE tutorial_id = %s
                """, (
            request.POST['tutorial_title'],
            request.POST['tutorial_description'],
            request.POST['tutorial_topic_id'],
            tutorialId
        ))
        context["tutorialDetails"] =  getData(tutorialId)
        messages.add_message(request, messages.INFO, "tutorial updated succesfully !!!")
        return redirect('tutorial-listing')
    else:
        return render(request, 'tutorial.html', context)

def read(request, tutorialId):
    context = {
        "fn": "update",
        "tutorialDetails": getData(tutorialId),
        "topicslist": getDropDown('topics', 'topics_id'),
        "heading": 'Update tutorial',
    }
    return render(request, 'read.html', context)


def add(request):
    context = {
        "fn": "add",
        "topicslist": getDropDown('topics', 'topics_id'),
        "heading": 'Add tutorial'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO tutorial
		   SET tutorial_title=%s, tutorial_description=%s, tutorial_topic_id=%s
		""", (
            request.POST['tutorial_title'],
            request.POST['tutorial_description'],
            request.POST['tutorial_topic_id']))
        return redirect('tutorial-listing')
    return render(request, 'tutorial.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM tutorial WHERE tutorial_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "tutorial Deleted succesfully !!!")
    return redirect('tutorial-listing')

def getDropDown(table, condtion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE " + condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList;