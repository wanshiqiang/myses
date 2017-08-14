# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from . import models
from . import views
from . import utils


# Create your tests here.

class DatabaseTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        print("======in setUp")

    # 需要测试的内容
    def test_add(self):

        subject1 = models.Subject.create(name='信息技术', introduction='学习信息')
        subject2 = models.Subject.create(name='语文', introduction='学习语文')
        subject3 = models.Subject.create(name='数学', introduction='学习数学')
        subject4 = models.Subject.create(name='机器人', introduction='学习机器人')
        subject1.save()
        subject2.save()
        subject3.save()
        subject4.save()
        classroom1 = models.Classroom.create(name='五年级1班', clazz=1, grade=5)
        classroom2 = models.Classroom.create(name='五年级2班', clazz=2, grade=5)
        classroom3 = models.Classroom.create(name='五年级3班', clazz=3, grade=5)

        # classroom1 = models.Classroom()
        # classroom1.name = '五年级8班'
        # classroom1.clazz = 8
        # classroom1.grade = 5
        classroom1.save()
        classroom2.save()
        classroom3.save()

        # 不需要classromm添加subjects
        # classroom1.subjects.add(subject1)
        homework1 = models.Homework.create(title="作业1", content="作业1内容",type='0')
        homework1.save()

        teacher1 = models.Teacher.create(name="信息老师1", age=26, pwd="123@abcd",number='20140901')
        teacher2 = models.Teacher.create(name="语文老师2", age=27, pwd="123@abcd",number='20130901')
        teacher3 = models.Teacher.create(name="数学老师2", age=33, pwd="123@abcd",number='20140901')
        teacher4 = models.Teacher.create(name="信息老师2", age=33, pwd="123@abcd",number='19980901')
        teacher1.save()
        teacher2.save()
        teacher3.save()
        teacher4.save()

        course1 = models.Course.create(subject=subject1, classroom=classroom1, homework=homework1, teacher=teacher1)
        course2 = models.Course.create(subject=subject2, classroom=classroom2, homework=homework1, teacher=teacher2)
        course3 = models.Course.create(subject=subject3, classroom=classroom1, homework=homework1, teacher=teacher3)
        course4 = models.Course.create(subject=subject1, classroom=classroom3, homework=homework1, teacher=teacher4)
        course5 = models.Course.create(subject=subject4, classroom=classroom1, homework=homework1, teacher=teacher1)
        course1.save()
        course2.save()
        course3.save()
        course4.save()
        course5.save()
        # self.assertEqual(student.name, 'aaa')

        stu1 = models.Student.create(name='学生1', number='20125101', pwd='123@abcd',seat=1, classroom=classroom1)
        stu2 = models.Student.create(name='学生2', number='20125201', pwd='123@abcd',seat=1, classroom=classroom2)
        stu3 = models.Student.create(name='学生3', number='20125102', pwd='123@abcd',seat=2, classroom=classroom1)
        stu4 = models.Student.create(name='学生4', number='20125301', pwd='123@abcd',seat=1, classroom=classroom3)
        stu1.save()
        stu2.save()
        stu3.save()
        stu4.save()

        testForm1 = models.TestForm.create(title='总分',testScore=0)
        testForm2 = models.TestForm.create(title='总分',testScore=0)
        testForm3 = models.TestForm.create(title='总分',testScore=0)
        testForm4 = models.TestForm.create(title='总分',testScore=0)
        testForm5 = models.TestForm.create(title='语文第一单元',testScore=100)
        testForm1.save()
        testForm2.save()
        testForm3.save()
        testForm4.save()
        testForm5.save()

        score1 = models.Score.create(student=stu1, subject=subject1, testForm=testForm1)
        score2 = models.Score.create(student=stu2, subject=subject1, testForm=testForm2)
        score3 = models.Score.create(student=stu3, subject=subject1, testForm=testForm3)
        score4 = models.Score.create(student=stu4, subject=subject1, testForm=testForm4)
        score5 = models.Score.create(student=stu1, subject=subject2, testForm=testForm5)
        # score1 = models.Score.create(student=stu1, subject=subject1, title='总分', testScore=10)
        # score2 = models.Score.create(student=stu2, subject=subject1, title='总分', testScore=10)
        # score3 = models.Score.create(student=stu3, subject=subject1, title='总分', testScore=100)
        # score4 = models.Score.create(student=stu4, subject=subject1, title='总分', testScore=10)
        # score5 = models.Score.create(student=stu1, subject=subject2, title='语文第一单元', testScore=100)
        score1.save()
        score2.save()
        score3.save()
        score4.save()
        score5.save()

        print("================查询all===============")
        subjects = models.Subject.objects.all()
        for index, subject in enumerate(subjects):
            # print 'subject1 name:' + subject.name
            print '_'.join(['subject', str(index + 1), 'name:     ', subject.name]),
            print '_'.join(['subject', str(index + 1), 'info:     ', subject.introduction])

        classrooms = models.Classroom.objects.all()
        for index, classroom in enumerate(classrooms):
            # print 'subject1 name:' + subject.name
            print '_'.join(['classroom', str(index + 1), 'name:     ', classroom.name]),
            print '_'.join(['clazz:     ', classroom.clazz]),
            print '_'.join(['grade:     ', classroom.grade])

        homeworks = models.Homework.objects.all()
        for index, homework in enumerate(homeworks):
            print '_'.join(['homework', str(index + 1), 'title:     ', homework.title])

        stus = models.Student.objects.all()
        for index, stu in enumerate(stus):
            print '_'.join(['stu', str(index + 1), 'name', stu.name]),

        print '\n'

        print("================条件查询======================")
        xxsubject = models.Subject.objects.filter(name='信息技术')
        xxCourses = models.Course.objects.filter(subject=xxsubject)
        print '信息学科的老师有：'
        # print Tpye(xxCourses)
        for index, course in enumerate(xxCourses):
            print course.teacher.name + " ",
        print '\n'


        print '信息老师1的所有学科'
        xxTeacher = models.Teacher.objects.filter(name='信息老师1')
        xxCourses2 = models.Course.objects.filter(teacher=xxTeacher)
        for index, course2 in enumerate(xxCourses2):
            print course2.subject.name + " ",

        print '\n'
        print '信息老师1的所有班级'
        xxCourses2 = models.Course.objects.filter(teacher=xxTeacher)
        for index, course2 in enumerate(xxCourses2):
            print course2.classroom.name + " ",

        print '\n'



        print '班级51的所有学科'

        xxCourses2 = models.Course.objects.filter(classroom=classroom1)
        for index, course2 in enumerate(xxCourses2):
            print course2.subject.name + " ",
        # for subject in classroom1.subjects:
        #     print subject.name
        # models.Course.subject.filter(name='信息技术')

        print "\n"
        print '五1班所有学生的信息总成绩'
        stus = models.Student.objects.filter(classroom=classroom1)

        for index, stu in enumerate(stus):
            sumScores = models.Score.objects.filter(student=stu, subject=subject1, testForm=testForm1)
            for score in sumScores:
                print stu.name +" "+score.testForm.title +" "+str(score.testForm.testScore)

        print '五1班所有学生的信息总成绩,第二种查询'
        stus2 = classroom1.student_set.all()
        print type(stus2)
        for index, stu in enumerate(stus2):
            # sumScores = models.Score.objects.filter(student=stu, subject=subject1, title="总分")
            # get查询的是单个对象
            # sumScores = stu.score_set.get(subject=subject1, title="总分")
            sumScores = stu.score_set.filter(subject=subject1, testForm=testForm1)
            for score in sumScores:
                print stu.name + " " + score.testForm.title + " " + str(score.testForm.testScore)

        utils.saveSubjectDataFromExcel("subjectData.xlsx")

        subjects = models.Subject.objects.all()
        for index, subject in enumerate(subjects):
            # print 'subject1 name:' + subject.name
            print '_'.join(['subject', str(index + 1), 'name:     ', subject.name]),
            print '_'.join(['subject', str(index + 1), 'info:     ', subject.introduction])


    # 需要测试的内容
    def test_query(self):
        pass
        # print("================查询===============")
        # subjects = Subject.objects.all()
        # print 'subject1 name:'+subjects[0].name
        # # self.assertEqual(0,  Student.objects.count())

        # 测试函数执行后执行

    def tearDown(self):
        print("======in tearDown")
