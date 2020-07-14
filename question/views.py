from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection
import datetime



# Create your views here.

def listing(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM question, topics, course WHERE question_topic_id = topics_id AND course_id = topics_course_id")
    questionlist = dictfetchall(cursor)

    context = {
        "questionlist": questionlist
    }

    # Message according Question #
    context['heading'] = "Quiz Results";
    return render(request, 'question-view.html', context)

def result_view(request):
    user_id = request.session.get('user_id', None)
    user_level_id = request.session.get('user_level_id', None)
    cursor = connection.cursor()
    if(user_level_id == 1):
        cursor.execute("SELECT * FROM quiz, topics, users_user, course WHERE quiz_topic_id = topics_id AND topics_course_id = course_id AND user_id = quiz_user_id")
    else:
        cursor.execute("SELECT * FROM quiz, topics, users_user, course WHERE quiz_topic_id = topics_id AND topics_course_id = course_id AND user_id = quiz_user_id AND user_id = "+str(user_id))
    questionlist = dictfetchall(cursor)

    context = {
        "questionlist": questionlist
    }

    # Message according Question #
    context['heading'] = "Quiz Attempts and Results";
    return render(request, 'result-view.html', context)

def result_answer(request, id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM answer, question WHERE answer_quiz_id = "+id+" AND answer_question_id = question_id")
    questionlist = dictfetchall(cursor)

    context = {
        "questionlist": questionlist
    }

    # Message according Question #
    context['heading'] = "Quiz Results";
    return render(request, 'result-answers.html', context)

def quiz(request, id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM question, topics, course WHERE question_topic_id = topics_id AND topics_course_id = course_id AND topics_id = "+id)
    questionlist = dictfetchall(cursor)
    now = datetime.datetime.now()

    context = {
        "questionlist": questionlist,
        "heading": "Quiz Questions "
    }

    if (request.method == "POST"):
        user_id = request.session.get('user_id', None)
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO quiz
        SET quiz_topic_id=%s, quiz_user_id=%s, quiz_date=%s, quiz_result=%s, quiz_marks=%s		   
        """, (
            request.POST['topic_id'],
            user_id,
            now.strftime("%Y-%m-%d"),
            '',
            ''
        ))
        quiz_id = cursor.lastrowid
        correct_count = 0
        count = int (request.POST['total_question'])

        ### Get all the questions ID ####
        questionIDs = getQuestion(request.POST['topic_id'])
        for key in questionIDs:
            x = key['question_id']
            correct = "0"
            if(request.POST['answer_'+str(x)] == request.POST['correct_'+str(x)]):
                correct_count = correct_count + 1
                correct = "1"
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO answer
            SET answer_quiz_id=%s, answer_question_id=%s, answer_user_answer=%s, answer_correct_answer=%s, answer_status=%s		   
            """, [
                quiz_id,
                request.POST['question_'+str(x)],
                request.POST['answer_'+str(x)],
                request.POST['correct_'+str(x)],
                correct
            ])

            marks = str(correct_count)+" out of "+str(count)
            if(correct_count == count):
                result = "Pass"
            else:
                result= "Fail"
            ### Update the Result Status ###
            cursor = connection.cursor()
            cursor.execute("""
                    UPDATE quiz
                    SET quiz_result=%s, quiz_marks=%s
                    WHERE quiz_id = %s
                    """, (
                result,
                marks,
                quiz_id
            ))
        return redirect('result_answer', id=quiz_id)
    else:
        return render(request, 'quiz.html', context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getDropDown(table, condtion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE " + condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList;

def getQuestion(id):
    cursor = connection.cursor()
    cursor.execute("SELECT question_id FROM question WHERE question_topic_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList;

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM question WHERE question_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, questionId):
    context = {
        "fn": "update",
        "levelslist": getDropDown('level', 'level_id'),
        "topicslist": getDropDown('topics', 'topics_id'),
        "questionDetails": getData(questionId),
        "heading": 'User Question Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE question
                   SET question_topic_id=%s, question_title=%s, question_option1=%s, question_option2=%s, question_option3=%s, question_option4=%s,
		   question_answer=%s
		   WHERE question_id = %s
                """, (
            request.POST['question_topic_id'],
            request.POST['question_title'],
            request.POST['question_option1'],
            request.POST['question_option2'],
            request.POST['question_option3'],
            request.POST['question_option4'],
            request.POST['question_answer'],
            questionId
        ))
        context["questionDetails"] =  getData(questionId)
        messages.add_message(request, messages.INFO, "User Question updated succesfully !!!")
        return redirect('listing')
    else:
        return render(request, 'question.html', context)




def add(request):
    context = {
        "fn": "add",
        "levelslist": getDropDown('level', 'level_id'),
        "topicslist": getDropDown('topics', 'topics_id'),
        "heading": 'Question Details'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO question
		   SET question_topic_id=%s, question_title=%s, question_option1=%s, question_option2=%s, question_option3=%s, question_option4=%s,
		   question_answer=%s		   
		""", (
            request.POST['question_topic_id'],
            request.POST['question_title'],
            request.POST['question_option1'],
            request.POST['question_option2'],
            request.POST['question_option3'],
            request.POST['question_option4'],
            request.POST['question_answer']
           ))
        return redirect('listing')
    return render(request, 'question.html', context)


def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM question WHERE question_id=' + id
    cursor.execute(sql)
    return redirect('listing')
