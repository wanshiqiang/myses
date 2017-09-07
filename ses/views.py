# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.forms.models import model_to_dict
from StringIO import StringIO
from xlwt import *

import json
# from django.utils import simplejson

# Create your views here.
from . import models
import copy


def index(request):
    # students = []
    # for i in range(1, 48):
    # #    print models.Student('ss',11).age
    #     name = '_'.join(['stu',str(i)])
    #     age = '_'.join(['age',str(i)])
    #     students.append(models.Student(name,age))

    username = ''
    if "username" in request.session:
        username = request.session["username"]
        # print '============================'
        # print type(username)
        # print username
    else:
        return render(request, 'ses/login.html', {})

    # classrooms = models.Classroom.objects.all()
    # subjects = models.Subject.objects.all()

    courses = models.Course.objects.filter(teacher__name=username)

    classrooms = []
    subjects = []
    for course in courses:
        if course.classroom not in classrooms:
            classrooms.append(course.classroom)
        if course.subject not in subjects:
            subjects.append(course.subject)

    print '========================================', classrooms, subjects

    selectedClassID = 0
    selectedSubjectID = 0

    if classrooms:
        selectedClassID = classrooms[0].id

    if subjects:
        selectedSubjectID = subjects[0].id

    if 'selectCla' in request.GET:
        # selectedClassID = request.GET['selectCla'].encode('utf-8')
        selectedClassID = int(request.GET['selectCla'].encode('utf-8'))

        # message = '你搜索的内容为: ' + request.GET['q'].encode('utf-8')
    if 'selectSub' in request.GET:
        # selectedSubjectID = request.GET['selectSub'].encode('utf-8')
        selectedSubjectID = int(request.GET['selectSub'].encode('utf-8'))

    # print selectedSubjectName.decode('utf-8')
    # print selectedClassName.decode('utf-8')
    print selectedClassID
    print selectedSubjectID

    # scoreRules = models.ScoreRule.objects.filter(topTitle__type=0)
    scoreRules = models.Score.objects.values_list('scoreRule__id', 'scoreRule__title').filter(
        subject__id=selectedSubjectID, student__classroom__id=selectedClassID, scoreRule__topTitle__type=0).distinct()

    # titleList = models.Score.objects.values_list('student__classroom', 'student__classroom__name', 'scoreRule__title',
    #                                              'scoreRule__isCount', 'scoreRule__topTitle__name').distinct().order_by(
    #     "student__classroom", "scoreRule__topTitle__name")
    # print titleList

    print scoreRules
    if scoreRules:
        selectedScoreRuleID = scoreRules[0][0]
    else:
        selectedScoreRuleID = 0

    if 'selectScoreRule' in request.GET:
        selectedScoreRuleID = int(request.GET['selectScoreRule'].encode('utf-8'))

    # try:
    #     selectedClassroom = models.Classroom.objects.get(id=selectedClassID)
    #     selectedSubject = models.Subject.objects.get(id=selectedSubjectID)
    # except Exception as err:
    #     print(err)

    # selectedScoreTopScore = models.ScoreTopTitle.objects.get(id=selectedScoreRuleID)

    seats = models.Seat.objects.filter(subject__id=selectedSubjectID, student__classroom__id=selectedClassID).order_by(
        "seatNo")
    # scores = models.Score.objects.filter(subject=selectedSubject,student__classroom=selectedClassroom,scoreRule__topTitle=selectedScoreTopScore).order_by("student__id")
    scores = models.Score.objects.filter(subject__id=selectedSubjectID, student__classroom__id=selectedClassID,
                                         scoreRule__id=selectedScoreRuleID,
                                         scoreRule__createTeacher__name=username).order_by("student__id")

    # students = models.Course.objects.get(classroom=selectedClassroom)
    print seats
    # students = selectedClassroom.student_set.all()
    students = models.Student.objects.filter(classroom__id=selectedClassID)

    newSeats = []
    for seatIndex, seat in enumerate(seats):
        if seatIndex > 0 and seat.seatNo != seats[seatIndex - 1].seatNo + 1:
            # noStudent = copy.copy(seat.student)
            for count in range(seat.seatNo - seats[seatIndex - 1].seatNo - 1):
                noStudent = models.Student()
                noStudent.name = '空'
                noSeat = models.Seat()
                noSeat.seatNo = seat.seatNo - count - 1
                noSeat.student = noStudent
                newSeats.append(noSeat)
        newSeats.append(seat)

    # return HttpResponse('hello,world')
    return render(request, 'ses/model_clr.html',
                  {'seats': newSeats, 'classrooms': classrooms, 'subjects': subjects,
                   'selectClassroomID': selectedClassID,
                   'selectSubjectID': selectedSubjectID, 'scores': scores, 'scoreRules': scoreRules,
                   'selectedScoreRuleID': selectedScoreRuleID, })


def index2(request):
    username = ''
    if "username" in request.session:
        username = request.session["username"]
        # print '============================'
        # print type(username)
        # print username
    else:
        return render(request, 'ses/login.html', {})

    courses = models.Course.objects.filter(teacher__name=username)

    classrooms = []
    subjects = []
    for course in courses:
        if course.classroom not in classrooms:
            classrooms.append(course.classroom)
        if course.subject not in subjects:
            subjects.append(course.subject)

    print '========================================', classrooms, subjects

    selectedClassID = 0
    selectedSubjectID = 0

    if classrooms:
        selectedClassID = classrooms[0].id

    if subjects:
        selectedSubjectID = subjects[0].id

    if 'selectCla' in request.GET:
        selectedClassID = int(request.GET['selectCla'].encode('utf-8'))

    if 'selectSub' in request.GET:
        selectedSubjectID = int(request.GET['selectSub'].encode('utf-8'))

    print selectedClassID
    print selectedSubjectID

    # scoreRules = models.ScoreRule.objects.filter(topTitle__type=0)
    scoreRules = models.Score.objects.values_list('scoreRule__id', 'scoreRule__title').filter(
        subject__id=selectedSubjectID, student__classroom__id=selectedClassID, scoreRule__topTitle__type=0).distinct()

    print scoreRules

    if scoreRules:
        selectedScoreRuleID = scoreRules[0][0]
    else:
        selectedScoreRuleID = 0

    if 'selectScoreRule' in request.GET:
        selectedScoreRuleID = int(request.GET['selectScoreRule'].encode('utf-8'))

    seats = models.Seat.objects.filter(subject__id=selectedSubjectID, student__classroom__id=selectedClassID).order_by(
        "seatNo")

    scores = models.Score.objects.filter(subject__id=selectedSubjectID, student__classroom__id=selectedClassID,
                                         scoreRule__id=selectedScoreRuleID,
                                         scoreRule__createTeacher__name=username).order_by("student__id")

    print seats

    seatListByRowCol = []

    colSum = 6
    for seatIndex, seat in enumerate(list(seats)):
        seatNo = seat.seatNo - 1
        rowIndex = seatNo / colSum + 1
        colIndex = seatNo % colSum + 1
        print seatIndex
        # if seatIndex > 0 and seat.seatNo != seat[seatIndex-1].seatNo+1:
        if seatIndex > 0 and seat.seatNo != seats[seatIndex - 1].seatNo + 1:
            noStudent = copy.copy(seat.student)
            noStudent.name = '空'
            noSeat = models.Seat()
            noSeat.seatNo = seat.seatNo - 1
            noSeat.student = noStudent
            noSeat.student.name = '空'
            seatByRowCol = {'seat': noSeat, 'rowIndex': 0, 'colIndex': 0}
            seatListByRowCol.append(seatByRowCol)

        seatByRowCol = {'seat': seat, 'rowIndex': rowIndex, 'colIndex': colIndex}
        seatListByRowCol.append(seatByRowCol)

    # return HttpResponse(seatListByRowCol)
    return render(request, 'ses/model_clr2.html',
                  {'seatListByRowCol': seatListByRowCol, 'classrooms': classrooms, 'subjects': subjects,
                   'selectClassroomID': selectedClassID,
                   'selectSubjectID': selectedSubjectID, 'scores': scores, 'scoreRules': scoreRules,
                   'selectedScoreRuleID': selectedScoreRuleID, })


def editSeat(request):
    if 'selectCla' in request.GET:
        # selectedClassID = request.GET['selectCla'].encode('utf-8')
        selectedClassID = int(request.GET['selectCla'].encode('utf-8'))

        # message = '你搜索的内容为: ' + request.GET['q'].encode('utf-8')
    if 'selectSub' in request.GET:
        # selectedSubjectID = request.GET['selectSub'].encode('utf-8')
        selectedSubjectID = int(request.GET['selectSub'].encode('utf-8'))

    selectedClassroom = models.Classroom.objects.get(name='五8班')
    selectedSubject = models.Subject.objects.get(name='信息')

    print selectedClassID
    print selectedSubjectID

    selectedClassroom = models.Classroom.objects.get(id=selectedClassID)
    selectedSubject = models.Subject.objects.get(id=selectedSubjectID)

    seats = models.Seat.objects.filter(subject=selectedSubject, student__classroom=selectedClassroom).order_by("seatNo")

    students = selectedClassroom.student_set.all()

    newSeats = []
    for seatIndex, seat in enumerate(seats):
        if seatIndex > 0 and seat.seatNo != seats[seatIndex - 1].seatNo + 1:
            # noStudent = copy.copy(seat.student)
            for count in range(seat.seatNo - seats[seatIndex - 1].seatNo - 1):
                noStudent = models.Student()
                # noStudent.number = seats[seatIndex-1].seatNo + count + 1
                noStudent.number = 0
                noStudent.name = '空'
                noSeat = models.Seat()
                noSeat.seatNo = seat.seatNo - count - 1
                noSeat.student = noStudent
                newSeats.append(noSeat)
        newSeats.append(seat)

    return render(request, 'ses/edit_seat.html',
                  {'students': students, 'seats': newSeats, 'selectedClassroom': selectedClassroom,
                   'selectedSubject': selectedSubject, })


def changeSeat(request):
    # try:
    #     seat1 = 0
    #     seat2 = 0
    #     selectedClassID = 16
    #     selectedSubjectID = 7
    #
    #     if 'seat1' in request.GET:
    #         seat1 = int(request.GET['seat1'].encode('utf-8'))
    #
    #     if 'seat2' in request.GET:
    #         seat2 = int(request.GET['seat2'].encode('utf-8'))
    #
    #     if 'selectCla' in request.GET:
    #         selectedClassID = int(request.GET['selectCla'].encode('utf-8'))
    #
    #     if 'selectSub' in request.GET:
    #         selectedSubjectID = int(request.GET['selectSub'].encode('utf-8'))
    #     # print "seat1"+str(seat1)+" "+ "seat2" +str(seat2) +"classroom"+str(selectedClassID)+"subject:"+str(selectedSubjectID)
    #
    #     # models.Seat.objects.filter(SUBJECT__)
    #     selectedClassroom = models.Classroom.objects.get(id=selectedClassID)
    #     selectedSubject = models.Subject.objects.get(id=selectedSubjectID)
    #
    #     seats = models.Seat.objects.filter(subject=selectedSubject, student__classroom=selectedClassroom)
    #     # seats = models.Seat.objects.filter(subject=selectedSubject, student__classroom=selectedClassroom,seatNo__in=[seat1,seat2])
    #     print "====seats====="+seats
    #
    # except:
    #     data = {}
    #     data['result'] = 'fail'
    #     # data['message'] = '更新页面吧'
    #     return HttpResponse(json.dumps(data), content_type="application/json")
    # else:
    #     data = {}
    #     data['result'] = 'success'
    #     # data['message'] = '更新页面吧'
    #     return HttpResponse(json.dumps(data), content_type="application/json")

    seat1 = 0
    seat2 = 0
    selectedClassID = 16
    selectedSubjectID = 7

    if 'seat1' in request.GET:
        seat1 = int(request.GET['seat1'].encode('utf-8'))

    if 'seat2' in request.GET:
        seat2 = int(request.GET['seat2'].encode('utf-8'))

    if 'selectCla' in request.GET:
        selectedClassID = int(request.GET['selectCla'].encode('utf-8'))

    if 'selectSub' in request.GET:
        selectedSubjectID = int(request.GET['selectSub'].encode('utf-8'))
    # print "seat1"+str(seat1)+" "+ "seat2" +str(seat2) +"classroom"+str(selectedClassID)+"subject:"+str(selectedSubjectID)

    # models.Seat.objects.filter(SUBJECT__)
    print "selectCla", selectedClassID, "selectSub", selectedSubjectID
    selectedClassroom = models.Classroom.objects.get(id=selectedClassID)
    selectedSubject = models.Subject.objects.get(id=selectedSubjectID)

    seats = models.Seat.objects.filter(subject=selectedSubject, student__classroom=selectedClassroom,
                                       seatNo__in=[seat1, seat2])
    for seat in seats:
        print "====seats===111==" + str(seat.seatNo) + "\n"

    if len(seats) == 2:
        tempNO = seats[0].seatNo
        seats[0].seatNo = seats[1].seatNo
        seats[1].seatNo = tempNO

    if len(seats) == 1:
        if seats[0].seatNo == seat1:
            seats[0].seatNo = seat2
        else:
            seats[0].seatNo = seat1

    for seat in seats:
        print "====seats===222==" + str(seat.seatNo) + "\n"
        seat.save()

    data = {}
    data['result'] = 'success'
    # data['message'] = '更新页面吧'
    return HttpResponse(json.dumps(data), content_type="application/json")


def editScore(request):
    data = {}
    stuNumber = 0
    selectedClassID = 16
    selectedSubjectID = 7
    type = 1
    selectScoreRuleID = 1

    if 'selectCla' in request.GET:
        selectedClassID = int(request.GET['selectCla'].encode('utf-8'))
        # selectedClassID = int(request.GET['selectCla'])

    if 'selectSub' in request.GET:
        selectedSubjectID = int(request.GET['selectSub'].encode('utf-8'))
        # selectedSubjectID = int(request.GET['selectSub'])

    if 'selectScoreRule' in request.GET:
        selectScoreRuleID = int(request.GET['selectScoreRule'].encode('utf-8'))
        # selectedSubjectID = int(request.GET['selectSub'])

    if 'studentNO' in request.GET:
        stuNumber = request.GET['studentNO'].encode('utf-8').strip()
        # stuNumber = request.GET['studentNO'].strip()

    if 'type' in request.GET:
        scoreType = int(request.GET['type'].encode('utf-8').strip())
        # scoreType = int(request.GET['type'].strip())

    print u'stuNumber,selectedClassID,selectedSubjectID=', stuNumber, selectedClassID, selectedSubjectID

    # selectedClassroom = models.Classroom.objects.get(id=selectedClassID)
    selectedSubject = models.Subject.objects.get(id=selectedSubjectID)

    # student = models.Student.objects.get(number=stuNumber)

    score = models.Score.objects.get(subject=selectedSubject, student__number=stuNumber,
                                     scoreRule__id=selectScoreRuleID)
    print u'score 1 ====', score.score
    if scoreType == 1:
        score.score += 5
        score.save()
        data['result'] = 'success'
    elif scoreType == 2:
        score.score -= 5
        score.save()
        data['result'] = 'success'
    else:
        data['result'] = 'fail'
    print u'score 2 ====;', score.score
    data['score'] = str(score.score)

    # data['message'] = '更新页面吧'
    # print json.dumps(data)

    return HttpResponse(json.dumps(data), content_type="application/json")


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


def login(request):
    # if 'ur' in request.GET:
    #     username = request.GET['ur'].encode('utf-8')
    # else:
    #     return render(request, 'ses/login.html', {})
    #
    # if 'pwd' in request.GET:
    #     pwd = request.GET['pwd'].encode('utf-8')
    # else:
    #     return render(request, 'ses/login.html', {})
    #
    # if username=="" or pwd=='':
    #     # print 'is \'\''
    #     return render(request, 'ses/login.html', {})



    # teacher = models.Teacher.objects.get(name=username)

    if request.method == 'GET':
        userform = UserForm(request.GET)
    if userform.is_valid():
        username = userform.cleaned_data['username']
        password = userform.cleaned_data['password']
        teacher = models.Teacher.objects.filter(name__exact=username, pwd__exact=password)

        if teacher:
            request.session['username'] = username
            print "save session username!!!!!!"
            # return render(request, 'ses/model_clr.html', {'userform': userform})
            return HttpResponseRedirect('/ses/index/')
        else:
            return HttpResponse('用户名或密码错误,请重新登录')
    else:
        userform = UserForm()

    # return render_to_response('login.html', {'userform': userform})
    return render(request, 'ses/login.html', {'userform': userform})


def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass

    return HttpResponseRedirect('/ses/login/')


def subjectManage(request):
    username = ''
    whichPanel = "#p1"

    if "username" not in request.session:
        return render(request, 'ses/login.html', {})
    else:
        username = request.session["username"]

    if 'whichPanel' in request.GET:
        whichPanel = "#" + request.GET['whichPanel'].encode('utf-8')

    # classrooms = models.Course.objects.values("classroom").filter(teacher__name=username)
    # print classrooms
    courses = models.Course.objects.filter(teacher__name=username)

    classrooms = []
    subjects = []
    for course in courses:
        if course.classroom not in classrooms:
            classrooms.append(course.classroom)
        if course.subject not in subjects:
            subjects.append(course.subject)
    print classrooms

    # 查询当前老师账号下的评价Score。
    # values_list与values类似，只是前者返回元祖，后者是字典列表
    # titleList = models.Score.objects.values_list('subject__name','student__classroom__name','scoreRule__title','scoreRule__isCount','scoreRule__topTitle__name').distinct().order_by("subject__name","student__classroom","scoreRule__topTitle__name")
    titleList = models.Score.objects.values('subject__name', 'student__classroom__name', 'scoreRule__title',
                                            'scoreRule__isCount', 'scoreRule__topTitle__name', 'subject__id',
                                            'student__classroom__id', 'scoreRule__id').filter(
        scoreRule__createTeacher__name=username).distinct().order_by("subject__name", "student__classroom",
                                                                     "scoreRule__topTitle__name")
    print titleList

    # scoreRuleList = models.ScoreRule.objects.all()
    scoreRuleList = models.ScoreRule.objects.filter(createTeacher__name=username)
    # 待修改，根据创建者来。
    scoreTopTitleList = models.ScoreTopTitle.objects.all()

    allClassroomList = models.Classroom.objects.all();
    allSubjectList = models.Subject.objects.all();
    # 集合取差集
    withoutClassroomList = list(set(allClassroomList) ^ set(classrooms))
    withoutSubjectList = list(set(allSubjectList) ^ set(subjects))
    # print set(allClassroomList),"===================\n",set(classrooms),"-----------------\n",withoutClassroomList
    # allGradeList = models.Course.objects.values('classroom__grade').filter(teacher__name=username).distinct()
    allGradeList = models.Classroom.objects.values('grade').distinct()
    allSubjectList = models.Subject.objects.all()

    return render(request, 'ses/subject_manage.html',
                  {"whichPanel": whichPanel, "classrooms": classrooms, 'subjects': subjects, 'titleList': titleList,
                   'scoreTopTitleList': scoreTopTitleList, 'scoreRuleList': scoreRuleList,
                   'withoutClassroomList': withoutClassroomList, 'withoutSubjectList': withoutSubjectList,
                   'courses': courses, 'allGradeList': allGradeList, 'allSubjectList': allSubjectList, })


def giveScoreRule(request):
    whichPanel = "p2"
    selectedSubjectID = 0
    titlescore = 0
    selectedClassroomIDList = []

    if 'selectSub' in request.GET:
        selectedSubjectID = int(request.GET['selectSub'].encode('utf-8'))

    if 'scoreRuleID' in request.GET:
        scoreRuleID = int(request.GET['scoreRuleID'].encode('utf-8'))

    if 'score' in request.GET:
        titlescore = int(request.GET['score'].encode('utf-8'))

    if 'selectedClassroomIDList' in request.GET:
        selectedClassroomIDList = request.GET.getlist('selectedClassroomIDList')

    print '====================', selectedSubjectID, selectedClassroomIDList, scoreRuleID, titlescore

    # students = models.Student.objects.filter(classroom_id=selectedClassID)



    subject = models.Subject.objects.get(id=selectedSubjectID)
    scoreRule = models.ScoreRule.objects.get(id=scoreRuleID)

    for claID in selectedClassroomIDList:
        students = models.Student.objects.filter(classroom_id=claID)
        isHasScoreList = models.Score.objects.filter(student__classroom_id=claID, subject__id=selectedSubjectID,
                                                     scoreRule__id=scoreRuleID)

        if len(isHasScoreList) != 0:
            return HttpResponse(u"已经存在了")

        for student in students:
            score = models.Score()
            score.student = student
            score.subject = subject
            # score.title = title
            score.scoreRule = scoreRule
            score.score = titlescore
            score.save()
            print student.number, '---------------------------------------is saved\n'

    return HttpResponseRedirect('/ses/subjectManage?whichPanel=' + whichPanel)


def addScoreRule(request):
    title = ''
    scoreTopTitleID = 0
    iscount = 0
    selectedSubjectIDList = []
    selectedClassroomIDList = []

    username = ''
    if "username" not in request.session:
        return render(request, 'ses/login.html', {})
    else:
        username = request.session["username"]

    if 'title' in request.GET:
        title = request.GET['title'].encode('utf-8')

    if 'scoreTopTitle' in request.GET:
        scoreTopTitleID = int(request.GET['scoreTopTitle'].encode('utf-8'))

    if 'iscount' in request.GET:
        iscount = int(request.GET['iscount'].encode('utf-8'))

    if 'selectedSubjectIDList' in request.GET:
        selectedSubjectIDList = request.GET.getlist('selectedSubjectIDList')

    if 'selectedClassroomIDList' in request.GET:
        selectedClassroomIDList = request.GET.getlist('selectedClassroomIDList')

    print '===============', title, scoreTopTitleID, iscount, selectedSubjectIDList, selectedClassroomIDList

    scoreTopTitle = models.ScoreTopTitle.objects.get(id=scoreTopTitleID)
    createTeacher = models.Teacher.objects.get(name=username)

    scoreRule = models.ScoreRule()
    scoreRule.title = title
    scoreRule.topTitle = scoreTopTitle
    scoreRule.isCount = iscount
    scoreRule.createTeacher = createTeacher
    scoreRule.save()

    for selectedSubjectID in selectedSubjectIDList:
        for selectedClassID in selectedClassroomIDList:
            students = models.Student.objects.filter(classroom_id=selectedClassID)
            subject = models.Subject.objects.get(id=selectedSubjectID)
            for student in students:
                score = models.Score()
                score.student = student
                score.subject = subject
                # score.title = title
                score.scoreRule = scoreRule
                score.score = 0
                score.save()

    return HttpResponseRedirect('/ses/subjectManage/')


def scoreListQuery(request):
    subjectID = 0
    classroomID = 0
    scoreList = []
    titleList = ['姓名', ]
    studentScore = []

    username = ''
    if "username" not in request.session:
        return render(request, 'ses/login.html', {})
    else:
        username = request.session["username"]

    # classrooms = models.Course.objects.values("classroom").filter(teacher__name=username)
    # print classrooms
    courses = models.Course.objects.filter(teacher__name=username)

    classrooms = []
    subjects = []
    for course in courses:
        if course.classroom not in classrooms:
            classrooms.append(course.classroom)
        if course.subject not in subjects:
            subjects.append(course.subject)
    print classrooms

    if classrooms:
        classroomID = classrooms[0].id

    if subjects:
        subjectID = subjects[0].id

    if 'selectCla' in request.GET:
        # selectedClassID = request.GET['selectCla'].encode('utf-8')
        classroomID = int(request.GET['selectCla'].encode('utf-8'))

        # message = '你搜索的内容为: ' + request.GET['q'].encode('utf-8')
    if 'selectSub' in request.GET:
        # selectedSubjectID = request.GET['selectSub'].encode('utf-8')
        subjectID = int(request.GET['selectSub'].encode('utf-8'))

    print "~~~~~~~~~~~~~~", classroomID, subjectID

    scoreQuery = models.Score.objects.filter(subject__id=subjectID, student__classroom_id=classroomID,
                                             scoreRule__isCount=1)
    # titleList = models.Score.objects.values("title").distinct()
    # titleList = models.Score.objects.values("scoreRule__title").distinct()
    studentIdList = models.Classroom.objects.filter(id=classroomID).values("student__id")

    hasStuID = []
    for stuID in studentIdList:
        sumScore = 0
        for score in scoreQuery:
            if score.student.id == stuID['student__id']:
                if stuID['student__id'] not in hasStuID:
                    print "------------------"
                    studentScore.append(score.student.name)
                    hasStuID.append(stuID['student__id'])
                # 在移动API中可以返回json格式
                # studentScore.append({score.title:score.score})
                if score.scoreRule.title not in titleList:
                    titleList.append(score.scoreRule.title)
                studentScore.append(int(score.score))
                sumScore = sumScore + int(score.score)
            else:
                pass
                # print "++++++++++++++++++++"

        print '+++++++', studentScore
        studentScore.append(sumScore)
        scoreList.append(studentScore)
        studentScore = []

    # print '======================',scoreQuery
    # print '======================scoreList',scoreList
    titleList.append("总积分")

    return render(request, 'ses/scoreListQuery.html',
                  {'scoreList': scoreList, 'titleList': titleList, "classrooms": classrooms, 'subjects': subjects,
                   'selectClassroomID': classroomID, 'selectSubjectID': subjectID, })

def  scoreListQueryByStu(request):
    subjectID = 0
    classroomID = 0
    scoreList = []
    titleList = ['姓名', ]
    studentScore = []

    username = ''
    if "username" not in request.session:
        return render(request, 'ses/login.html', {})
    else:
        username = request.session["username"]

    # classrooms = models.Course.objects.values("classroom").filter(teacher__name=username)
    # print classrooms
    courses = models.Course.objects.filter(teacher__name=username)

    classrooms = []
    subjects = []
    for course in courses:
        if course.classroom not in classrooms:
            classrooms.append(course.classroom)
        if course.subject not in subjects:
            subjects.append(course.subject)
    print classrooms

    if classrooms:
        classroomID = classrooms[0].id

    if subjects:
        subjectID = subjects[0].id

    if 'selectCla' in request.GET:
        # selectedClassID = request.GET['selectCla'].encode('utf-8')
        classroomID = int(request.GET['selectCla'].encode('utf-8'))

        # message = '你搜索的内容为: ' + request.GET['q'].encode('utf-8')
    if 'selectSub' in request.GET:
        # selectedSubjectID = request.GET['selectSub'].encode('utf-8')
        subjectID = int(request.GET['selectSub'].encode('utf-8'))

    print "~~~~~~~~~~~~~~", classroomID, subjectID

    scoreQuery = models.Score.objects.filter(subject__id=subjectID, student__classroom_id=classroomID,
                                             scoreRule__isCount=1)
    # titleList = models.Score.objects.values("title").distinct()
    # titleList = models.Score.objects.values("scoreRule__title").distinct()
    studentIdList = models.Classroom.objects.filter(id=classroomID).values("student__id")

    hasStuID = []
    for stuID in studentIdList:
        sumScore = 0
        for score in scoreQuery:
            if score.student.id == stuID['student__id']:
                if stuID['student__id'] not in hasStuID:
                    print "------------------"
                    studentScore.append(score.student.name)
                    hasStuID.append(stuID['student__id'])
                # 在移动API中可以返回json格式
                # studentScore.append({score.title:score.score})
                if score.scoreRule.title not in titleList:
                    titleList.append(score.scoreRule.title)
                studentScore.append(int(score.score))
                sumScore = sumScore + int(score.score)
            else:
                pass
                # print "++++++++++++++++++++"

        print '+++++++', studentScore
        studentScore.append(sumScore)
        scoreList.append(studentScore)
        studentScore = []

    # print '======================',scoreQuery
    # print '======================scoreList',scoreList
    titleList.append("总积分")

    return render(request, 'ses/scoreListQueryByStu.html',
                  {'scoreList': scoreList, 'titleList': titleList, "classrooms": classrooms, 'subjects': subjects,
                   'selectClassroomID': classroomID, 'selectSubjectID': subjectID, })

def getScoreRules(request):
    # data={}
    selectedClassID = 0
    selectedSubjectID = 0

    if 'selectCla' in request.GET:
        # selectedClassID = request.GET['selectCla'].encode('utf-8')
        selectedClassID = int(request.GET['selectCla'].encode('utf-8'))

        # message = '你搜索的内容为: ' + request.GET['q'].encode('utf-8')
    if 'selectSub' in request.GET:
        # selectedSubjectID = request.GET['selectSub'].encode('utf-8')
        selectedSubjectID = int(request.GET['selectSub'].encode('utf-8'))

    # print selectedSubjectName.decode('utf-8')
    # print selectedClassName.decode('utf-8')
    print selectedClassID
    print selectedSubjectID

    # scoreRules = models.ScoreRule.objects.filter(topTitle__type=0)
    scoreRules = models.Score.objects.values('scoreRule__id', 'scoreRule__title').filter(
        subject__id=selectedSubjectID, student__classroom__id=selectedClassID, scoreRule__topTitle__type=0).distinct()

    return HttpResponse(json.dumps(list(scoreRules)), content_type="application/json")


def getNotClaSubByScoreRule(request):
    scoreRuleID = 0
    selectSubID = 0
    outputClassroomList = []
    if "username" not in request.session:
        return render(request, 'ses/login.html', {})
    else:
        username = request.session["username"]

    if 'scoreRuleID' in request.GET:
        scoreRuleID = int(request.GET['scoreRuleID'].encode('utf-8'))

    if 'selectSubID' in request.GET:
        selectSubID = int(request.GET['selectSubID'].encode('utf-8'))

    classroomHasRuleList = models.Score.objects.values('student__classroom__id', 'student__classroom__name').filter(
        scoreRule__id=scoreRuleID, subject__id=selectSubID).distinct()

    allclassroomList = models.Course.objects.values('classroom__id', 'classroom__name').filter(
        teacher__name=username).distinct()
    print "---------------", classroomHasRuleList
    print "++++++++++++++++", allclassroomList

    classroomHasRuleIDList = []
    for item in classroomHasRuleList:
        classroomHasRuleIDList.append(item['student__classroom__id'])

    for classroom in allclassroomList:
        if classroom['classroom__id'] in classroomHasRuleIDList:
            outputClassroomList.append(
                {'id': classroom['classroom__id'], 'name': classroom['classroom__name'], 'isHas': 1})
        else:
            outputClassroomList.append(
                {'id': classroom['classroom__id'], 'name': classroom['classroom__name'], 'isHas': 0})

    return HttpResponse(json.dumps(list(outputClassroomList)), content_type="application/json")


def deleteScore(request):
    subjectID = 0
    classroomID = 0
    scoreRuleID = 0
    if 'subjectID' in request.GET:
        subjectID = int(request.GET['subjectID'].encode('utf-8'))
    if 'classroomID' in request.GET:
        classroomID = int(request.GET['classroomID'].encode('utf-8'))
    if 'scoreRuleID' in request.GET:
        scoreRuleID = int(request.GET['scoreRuleID'].encode('utf-8'))

    models.Score.objects.filter(subject__id=subjectID, student__classroom__id=classroomID,
                                scoreRule__id=scoreRuleID).delete()

    return HttpResponseRedirect('/ses/subjectManage')


def sortSeat(request):
    col = 6
    classroomID = 16
    subjectID = 7
    sortType = 2

    if 'selectCla' in request.GET:
        classroomID = int(request.GET['selectCla'].encode('utf-8'))

    if 'selectSub' in request.GET:
        subjectID = int(request.GET['selectSub'].encode('utf-8'))

    if 'col' in request.GET:
        col = int(request.GET['col'].encode('utf-8'))

    if 'sortType' in request.GET:
        sortType = int(request.GET['sortType'].encode('utf-8'))

    seats = models.Seat.objects.filter(subject__id=subjectID, student__classroom__id=classroomID).order_by(
        "student__number")
    seatSum = max(len(seats), 48)
    print '===================', 'col=', col, 'seatSum=', seatSum

    seatNoList = []
    # colList = []


    # if sortType == 1:
    #     # 生成按照每一列排序的座位号
    #     for j in range(int(col)):
    #         # 多计算1行
    #         # for i in range(1,int(seatSum/col+1)):
    #         for i in range(int(seatSum / col + 1)):
    #             seatNo = (i + 1 - 1) * col + j + 1
    #             # colList.append(seatNo)
    #             if seatNo <= seatSum:
    #                 seatNoList.append(seatNo)
    #         # seatNoList.append(colList)
    #         colList = []
    #
    #     for index, seat in enumerate(seats):
    #         seat.seatNo = seatNoList[index]
    #         seat.save()

    if sortType == 1:
        # 行列改进算法
        for j in range(int(col)):
            # 先按照正好不多人算,再算多的人
            for i in range(int(seatSum / col)):
                seatNo = (i + 1 - 1) * col + j + 1
                seatNoList.append(seatNo)

        hasCount = int(seatSum / col) * col
        for k in range(int(seatSum - hasCount)):
            seatNoList.append(hasCount + k + 1)

        for index, seat in enumerate(seats):
            seat.seatNo = seatNoList[index]
            seat.save()

    # if sortType == 2:
    #     # 生成按照每一列排序的座位号
    #     for j in range(int(col)):
    #         # 多计算1行
    #         # for i in range(1,int(seatSum/col+1)):
    #         for i in range(int(seatSum / col + 1), 1 - 1, -1):
    #             seatNo = (i - 1) * col + j + 1
    #             # colList.append(seatNo)
    #             if seatNo <= seatSum:
    #                 seatNoList.append(seatNo)
    #         # seatNoList.append(colList)
    #         colList = []
    #
    #     for index, seat in enumerate(seats):
    #         seat.seatNo = seatNoList[index]
    #         seat.save()

    if sortType == 2:
        # 生成按照每一列排序的座位号
        for j in range(int(col)):
            # #先按照正好不多人算,再算多的人
            # for i in range(1,int(seatSum/col+1)):
            for i in range(int(seatSum / col), 1 - 1, -1):
                seatNo = (i - 1) * col + j + 1
                # colList.append(seatNo)
                if seatNo <= seatSum:
                    seatNoList.append(seatNo)
                    # seatNoList.append(colList)

        hasCount = int(seatSum / col) * col
        for k in range(int(seatSum - hasCount)):
            seatNoList.append(hasCount + k + 1)

        for index, seat in enumerate(seats):
            seat.seatNo = seatNoList[index]
            seat.save()

    return HttpResponseRedirect("/ses/editSeat/?selectCla=" + str(classroomID) + "&selectSub=" + str(subjectID))


def outputScoreListByExcel(request):
    scoreList = []
    titleList = ['姓名', ]
    studentScore = []

    username = ''
    if "username" not in request.session:
        return render(request, 'ses/login.html', {})
    else:
        username = request.session["username"]

    # courses = models.Course.objects.filter(teacher__name=username)

    if 'selectCla' in request.GET:
        classroomID = int(request.GET['selectCla'].encode('utf-8'))

    if 'selectSub' in request.GET:
        subjectID = int(request.GET['selectSub'].encode('utf-8'))

    print "~~~~~~~~~~~~~~", classroomID, subjectID

    scoreQuery = models.Score.objects.filter(subject__id=subjectID, student__classroom_id=classroomID,
                                             scoreRule__isCount=1)
    # titleList = models.Score.objects.values("title").distinct()
    # titleList = models.Score.objects.values("scoreRule__title").distinct()
    studentIdList = models.Classroom.objects.filter(id=classroomID).values("student__id")

    hasStuID = []
    for stuID in studentIdList:
        sumScore = 0
        for score in scoreQuery:
            if score.student.id == stuID['student__id']:
                if stuID['student__id'] not in hasStuID:
                    print "------------------"
                    studentScore.append(score.student.name)
                    hasStuID.append(stuID['student__id'])
                # 在移动API中可以返回json格式
                # studentScore.append({score.title:score.score})
                if score.scoreRule.title not in titleList:
                    titleList.append(score.scoreRule.title)
                studentScore.append(int(score.score))
                sumScore = sumScore + int(score.score)
            else:
                pass
                # print "++++++++++++++++++++"

        print '+++++++', studentScore
        studentScore.append(sumScore)
        scoreList.append(studentScore)
        studentScore = []

    # print '======================',scoreQuery
    # print '======================scoreList',scoreList
    titleList.append("总积分")

    ws = Workbook(encoding='utf-8')
    w = ws.add_sheet(u"数据报表第一页")
    # w.write(0, 0, "id")
    # w.write(0, 1, u"用户名")
    # w.write(0, 2, u"发布时间")
    # w.write(0, 3, u"内容")
    # w.write(0, 4, u"来源")

    # excel_row = 1
    # for obj in titleList:
    #     data_id = obj[0]
    #     data_user = obj[1]
    #     # data_time = obj[2]
    #     # data_content = obj[3]
    #     # dada_source = obj[4]
    #
    #     w.write(excel_row, 0, data_id)
    #     w.write(excel_row, 1, data_user)
    #     # w.write(excel_row, 2, data_time)
    #     # w.write(excel_row, 3, data_content)
    #     # w.write(excel_row, 4, dada_source)
    #     excel_row += 1
    for index, title in enumerate(titleList):
        w.write(0, index, title)

    excel_col = 0
    for rowIndex, stuScore in enumerate(scoreList):
        for colIndex, score in enumerate(stuScore):
            w.write(rowIndex + 1, colIndex, score)

    # sio = StringIO.StringIO()
    sio = StringIO()
    ws.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=test.xls'
    response.write(sio.getvalue())

    return response
    # return HttpResponseRedirect("/ses/scoreListQuery")


def addClassroom(request):
    whichPanel = "p4"
    selectSubID = 0
    selectedClassroomIDList = []

    username = ''
    if "username" not in request.session:
        return render(request, 'ses/login.html', {})
    else:
        username = request.session["username"]

    if 'selectSub' in request.GET:
        selectSubID = int(request.GET['selectSub'].encode('utf-8'))

    if 'selectedClassroomIDList' in request.GET:
        selectedClassroomIDList = request.GET.getlist('selectedClassroomIDList')

    for classroomID in selectedClassroomIDList:
        # 查询该班级该学科是否已经有人教了
        isHasClassroomList = models.Course.objects.filter(subject__id=selectSubID, classroom__id=classroomID)
        if isHasClassroomList:
            return HttpResponse(
                "班级" + isHasClassroomList[0].classroom.name + '已经添加' + isHasClassroomList[0].subject.name + "课程")
        else:
            classroom = models.Classroom.objects.get(id=classroomID)
            subject = models.Subject.objects.get(id=selectSubID)
            teacher = models.Teacher.objects.get(name=username)
            homework = models.Homework.objects.get(id=1)
            course = models.Course()
            course.classroom = classroom
            course.subject = subject
            course.teacher = teacher
            course.homework = homework
            course.save()
            print '==========add couse==========', course

            students = models.Student.objects.filter(classroom=classroom)
            for student in students:
                seat = models.Seat()
                seat.student = student
                seat.subject = course.subject
                seat.seatNo = student.stuNO
                seat.save()
                print '============add seat by course=================', seat

                # return HttpResponse("add:添加" + course.subject.name+course.classroom.name)

    # return HttpResponse("not has classrommidList")

    # subject = models.Subject.objects.get(id=selectedSubjectID)
    # scoreRule = models.ScoreRule.objects.get(id=scoreRuleID)



    return HttpResponseRedirect('/ses/subjectManage?whichPanel=' + whichPanel)


def getNotClaBySubGra(request):
    selectSubID = 0
    selectGradeID = 0
    outputClassroomList = []
    if "username" not in request.session:
        return render(request, 'ses/login.html', {})
    else:
        username = request.session["username"]

    if 'selectGradeID' in request.GET:
        selectGradeID = int(request.GET['selectGradeID'].encode('utf-8'))

    if 'selectSubID' in request.GET:
        selectSubID = int(request.GET['selectSubID'].encode('utf-8'))

    allclassroomList = models.Classroom.objects.values('id', 'name').filter(grade=selectGradeID)

    # classroomTeaHasList = models.Course.objects.values('classroom__id', 'classroom__name').filter(
    #     teacher__name=username, classroom__grade=selectGradeID, subject__id=selectSubID).distinct()

    classroomTeaHasList = models.Course.objects.values('classroom__id', 'classroom__name').filter(
        classroom__grade=selectGradeID, subject__id=selectSubID).distinct()

    print "---------------", classroomTeaHasList
    print "++++++++++++++++", allclassroomList

    classroomHasList = []
    for item in classroomTeaHasList:
        classroomHasList.append(item['classroom__id'])

    for classroom in allclassroomList:
        if classroom['id'] in classroomHasList:
            outputClassroomList.append(
                {'id': classroom['id'], 'name': classroom['name'], 'isHas': 1})
        else:
            outputClassroomList.append(
                {'id': classroom['id'], 'name': classroom['name'], 'isHas': 0})

    return HttpResponse(json.dumps(list(outputClassroomList)), content_type="application/json")

def toimportData(request):
    return render(request, 'ses/importdata.html',{})
def importData(request):
    return render(request, 'ses/importdata.html',{})
