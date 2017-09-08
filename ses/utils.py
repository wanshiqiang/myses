# -*- coding: utf-8 -*-
import xlwings as xw
import os
from . import models


def openExcelGetWorkBook(filename):
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    STATIC_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static\\upload\\')
    # print STATIC_ROOT
    filepath = os.path.join(STATIC_ROOT, filename)
    # print filepath

    wb = app.books.open(filepath)
    return wb


def saveSubjectDataFromExcel(filename):
    wb = openExcelGetWorkBook(filename)
    sht = wb.sheets[0]
    print type(sht)
    # print sht.range('A2').value
    subjectsData = sht.range('A2').expand('table').value
    for subjectLine in subjectsData:
        subject = models.Subject()
        subject.name = subjectLine[0]
        subject.introduction = subjectLine[1]

        if len(models.Subject.objects.filter(name=subject.name)) == 0:
            subject.save()
            print "name:" + subjectLine[0] + "info" + subjectLine[1]
        else:
            print subject.name + "ishaved"
    app = wb.app
    wb.close()
    app.quit()


def saveClassroomDataFromExcel(filename):
    wb = openExcelGetWorkBook(filename)
    sht = wb.sheets[0]
    print type(sht)
    # print sht.range('A2').value
    classroomsData = sht.range('A2').expand('table').value
    for classroomLine in classroomsData:
        classroom = models.Classroom()
        classroom.name = classroomLine[0]
        classroom.clazz = int(classroomLine[1])
        classroom.grade = int(classroomLine[2])
        if len(models.Classroom.objects.filter(name=classroom.name)) == 0:
            classroom.save()
            print "name:" + classroomLine[0] + "clazz" + str(classroomLine[1]) + "grade" + str(classroomLine[2])
        else:
            print classroom.name + "ishaved"

    app = wb.app
    wb.close()
    app.quit()


# def saveTestForm():
#     # 总积分是默认自动添加的
#     testForm = models.TestForm()
#     testForm.title = '总积分'
#     testForm.testScore = 0
#     testForm.save()


def saveStudentDataFromExcel(filename):
    wb = openExcelGetWorkBook(filename)
    sht = wb.sheets[0]
    print type(sht)
    # print sht.range('A2').value

    # subjectList = models.Subject.objects.all()

    studentsData = sht.range('A2').expand('table').value

    for studentLine in studentsData:
        student = models.Student()
        student.name = studentLine[0]
        # student.number = str(studentLine[1])
        student.number = int(studentLine[1])
        student.pwd = int(studentLine[2])
        student.stuNO = studentLine[3]
        #作为默认的分组号和是否组长设置
        student.groupid = int(studentLine[5])
        student.isHeadman = int(studentLine[6])
        print '===============', student.number
        if len(models.Student.objects.filter(number=student.number)) == 0:
            classroom = models.Classroom.objects.filter(name=studentLine[4])
            if len(classroom) == 1:
                student.classroom = classroom[0]
                student.save()
                # 查询添加的该学生所在班级的所有subject是否都有座位了，如果没有就添加seat表
                courseList = models.Course.objects.filter(classroom__id=student.classroom.id)
                print '========================saveStudent======================================', student.id, student.name
                print 'has subejcts', courseList
                seatNoList = models.Seat.objects.values_list('subject__id').filter(student__id=student.id)
                print 'has seatNoList', seatNoList
                for course in courseList:
                    if course.subject.id not in seatNoList:
                        seat = models.Seat()
                        seat.student = student
                        seat.subject = course.subject
                        seat.seatNo = student.stuNO
                        seat.groupid = int(studentLine[5])
                        seat.isHeadman = int(studentLine[6])
                        seat.save()
                    # 查询这个学生所在subject的所有评分标准,并添加积分=0
                    scoreRuleNoList = models.Score.objects.values_list('scoreRule__id').filter(
                        student__classroom__id=student.classroom.id, subject__id=course.subject.id).distinct()
                    for scoreRuleNo in scoreRuleNoList:
                        newScore = models.Score()
                        newScore.student= student
                        newScore.subject = course.subject
                        newScore.score = 0
                        newScore.scoreRule = models.ScoreRule.objects.get(id = scoreRuleNo[0])
                        print '===================================',newScore
                        newScore.save()


            else:
                print student.name + "的classroom is wrong，maybe is not exit"
            print "name:" + student.name + "is saved"
        else:
            print student.name + "ishaved"
    app = wb.app
    wb.close()
    app.quit()


def seatDataFromExcel(filename):
    pass


def saveTeacherDataFromExcel():
    pass


def saveScoreDataFromExcel():
    pass
