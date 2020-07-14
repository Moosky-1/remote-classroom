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
    cursor.execute("SELECT * FROM course")
    courselist = dictfetchall(cursor)

    context = {
        "courselist": courselist
    }

    # Message according medicines Role #
    context['heading'] = "Course Details";
    return render(request, 'course-details.html', context)

def lists(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course")
    courselist = dictfetchall(cursor)

    context = {
        "courselist": courselist
    }

    # Message according medicines Role #
    context['heading'] = "Course Details";
    return render(request, 'course-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course WHERE course_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, courseId):
    context = {
        "fn": "update",
        "courseDetails": getData(courseId),
        "heading": 'Update Course',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE course
                   SET course_name=%s, course_desc=%s WHERE course_id = %s
                """, (
            request.POST['course_name'],
            request.POST['course_desc'],
            courseId
        ))
        context["courseDetails"] =  getData(courseId)
        messages.add_message(request, messages.INFO, "Course updated succesfully !!!")
        return redirect('course-listing')
    else:
        return render(request, 'course.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Course'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO course
		   SET course_name=%s, course_desc=%s
		""", (
            request.POST['course_name'],
            request.POST['course_desc']))
        return redirect('course-listing')
    return render(request, 'course.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM course WHERE course_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Course Deleted succesfully !!!")
    return redirect('course-listing')
