# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
# class HomeworkManager(models.Manager):
#     def create_homework(self,title,content):
#         homework = self.create(title=title,content=content)
#         return homework


class Homework(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=1024)
    type = models.CharField(max_length=128)

    @classmethod
    def create(cls,title,content,type):
        homework =cls(title=title,content=content,type=type)
        return homework

    def __unicode__(self):
        return self.title


class Subject(models.Model):
    name = models.CharField(max_length=128)
    introduction = models.TextField(max_length=1024)

    # homework = models.ForeignKey(Homework, on_delete=models.CASCADE)

    # students = models.ManyToManyField(Student, through='Score')
    # classrooms = models.ManyToManyField(Classroom,through='Course',through_fields=('subject','classroom'))
    @classmethod
    def create(cls, name='1', introduction='1'):
        subject = cls(name=name,introduction=introduction)
        return subject

    # def __init__(self, name='1', introduction='1'):
    #     self.name = name
    #     self.introduction = introduction

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=128)
    age = models.CharField(max_length=128)
    pwd = models.CharField(max_length=128)
    number = models.CharField(max_length=128)

    @classmethod
    def create(cls,name,age,pwd,number):
        teacher = cls(name=name,age=age,pwd=pwd,number=number)
        return teacher


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

class Classroom(models.Model):
    name = models.CharField(max_length=128,verbose_name="班级名称")
    clazz = models.CharField(max_length=128,verbose_name="班级")
    grade = models.CharField(max_length=128,verbose_name="年级")
    subjects = models.ManyToManyField(Subject, through='Course')

    # subjects = models.ManyToManyField(Subject,through='Course',through_fields=('subject','classroom'),)

    @classmethod
    def create(cls,name,clazz,grade):
        classroom = cls(name = name ,clazz = clazz,grade=grade)
        #subjects定义的多对多关系，由于有索引表Course所以不需要再本类中create
        # classroom = cls(name = name ,clazz = clazz,grade=grade,subjects=subjects)
        return classroom

    # def __inti__(self, name, clazz, grade, subjects):
    #     self.name = name
    #     self.clazz = clazz
    #     self.grade = grade
    #     self.subjects = subjects

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'


class Student(models.Model):
    name = models.CharField(max_length=128)
    number = models.CharField(max_length=128)
    pwd = models.CharField(max_length=128)
    stuNO = models.IntegerField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, through='Score')
    groupid = models.IntegerField()
    isHeadman = models.IntegerField()


    @classmethod
    def create(cls,name,number,pwd,stuNO,classroom,groupid,isHeadman):
        student = cls(name= name ,number=number,pwd= pwd,stuNO=stuNO,classroom=classroom,groupid=groupid,isHeadman=isHeadman)
        return student


    # def __init__(self, name, number, pwd, classroom):
    #     self.name = name
    #     self.number = number
    #     self.pwd = pwd
    #     self.classroom = classroom

    def __unicode__(self):
        return self.name


class TestForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    testScore = models.DecimalField(max_digits=5, decimal_places=2)
    #iscount表示是否计入Score表
    iscount = models.CharField(max_length=128)

    @classmethod
    def create(cls,student,subject,title,testScore,iscount):
        testForm = cls(student=student,subject=subject,title=title,testScore=testScore,iscount=iscount)
        return testForm

    def __unicode__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    answer = models.CharField(max_length=128)
    testForm = models.ForeignKey(TestForm, on_delete=models.CASCADE)

    @classmethod
    def create(cls,title,type,score,answer,testForm):
        question = cls(title=title,type=type,score=score,answer=answer,testForm=testForm)
        return question

    def __unicode__(self):
        return self.title

class ScoreTopTitle(models.Model):
    name= models.CharField(max_length=128)
    # 0课堂评价积分类型(小组合作/自我探究/认真听讲/作品评价)1导入类型评价(测试)
    type = models.IntegerField()

    @classmethod
    def create(cls,name,type):
        scoreTopTitle = cls(name=name,type=type)
        return scoreTopTitle

    def __unicode__(self):
        return self.name


class ScoreRule(models.Model):
    title = models.CharField(max_length=128)
    topTitle = models.ForeignKey(ScoreTopTitle, on_delete=models.CASCADE)
    #是否统计如总分
    isCount = models.IntegerField()
    createTeacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    @classmethod
    def create(cls,title,topTitle,isCount,createTeacher):
        scoreRule = cls(title=title,topTitle=topTitle,isCount=isCount,createTeacher=createTeacher)
        return scoreRule

    def __unicode__(self):
        return self.title


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # testForm = models.ForeignKey(TestForm, on_delete=models.CASCADE,related_name="TESTFORM")
    # title = models.CharField(max_length=128)
    scoreRule = models.ForeignKey(ScoreRule, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    @classmethod
    def create(cls,student,subject,scoreRule,score):
        score = cls(student=student,subject=subject,scoreRule=scoreRule,score= score)
        return score

    def __unicode__(self):
        return '_'.join([self.student.name, self.subject.name])


class Seat(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name="STUDENT")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name="SUBJECT")
    seatNo = models.IntegerField()
    groupid = models.IntegerField()
    isHeadman = models.IntegerField()

    @classmethod
    def create(cls,student,subject,seatNo,groupid,isHeadman):
        seat = cls(student=student,subject=subject,seatNo=seatNo,groupid=groupid,isHeadman=isHeadman)
        return seat

    def __unicode__(self):
        return u'_'.join([self.student.name, self.subject.name])


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    @classmethod
    def create(cls,subject,classroom,homework,teacher):
        course = cls(subject=subject,classroom=classroom,homework=homework,teacher=teacher)
        return course

    def __unicode__(self):
        return '_'.join([self.subject.name, self.classroom.name])
