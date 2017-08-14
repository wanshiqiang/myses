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
        classroom.clazz = classroomLine[1]
        classroom.grade = classroomLine[2]
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

    subjectList = models.Subject.objects.all()

    studentsData = sht.range('A2').expand('table').value


    for studentLine in studentsData:
        student = models.Student()
        student.name = studentLine[0]
        # student.number = str(studentLine[1])
        student.number = int(studentLine[1])
        student.pwd = int(studentLine[2])
        student.stuNO = studentLine[3]
        print '===============',student.number
        if len(models.Student.objects.filter(number=student.number)) == 0:
            classroom = models.Classroom.objects.filter(name=studentLine[4])
            if len(classroom) == 1:
                student.classroom = classroom[0]
                student.save()

                for subject in subjectList:
                    seat = models.Seat()
                    seat.student = student
                    seat.subject = subject
                    seat.seatNo = student.stuNO
                    seat.save()

                    # 总积分是默认自动添加的
                    # testForm = models.TestForm()
                    # testForm.title = '总积分'
                    # testForm.testScore = 0
                    # testForm.save()

                    # score = models.Score()
                    # score.student = student
                    # score.subject = subject
                    # # score.testForm = testForm
                    # score.title = '课堂表现'
                    # score.score = 0
                    # score.save()

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