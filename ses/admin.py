# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Teacher
from models import Student
from models import Classroom
from models import Subject
from models import Course
from models import Score
from models import ScoreRule
from models import ScoreTopTitle
from models import TestForm

from django.contrib import admin
from django import forms


# Register your models here.

# class ScoreForm(forms.ModelForm):
#     classrooms = Classroom.objects.all()
#     classNames = []
#     for classroom in classrooms:
#         classNames.append((classroom.name,classroom.name))
#     classroom = forms.ChoiceField(choices=[('sqlserver','SQLServer'),('oracle','Oracle')])
#     classroomName = forms.ChoiceField(choices=classNames)
#     # classroomName = forms.CharField(initial=0,widget=forms.TextInput(attrs={'readonly':'true'}))
#     class Meta:
#         forms.model=Score

# class CourseInline(admin.StackedInline):
class CourseInline(admin.TabularInline):
    model = Course

# class ScoreInline(admin.StackedInline):
class ScoreInline(admin.TabularInline):
    model = Score

class ScoreTopTitleInline(admin.TabularInline):
    model = ScoreTopTitle

class ScoreRuleInline(admin.TabularInline):
    model = ScoreRule

class TeacherAdmin(admin.ModelAdmin):
    inlines = [CourseInline, ]
    list_display = ['name','age','pwd','number' ]

class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name','number')
    inlines = [ScoreInline]
    list_display = ['name','number','pwd','classroom' ]
    list_filter =('classroom','classroom__grade')

class ClassroomAdmin(admin.ModelAdmin):
    inlines = [CourseInline, ]
    list_display = ['name','clazz','grade' ]
    list_filter = ('grade',)

class SubjectAdmin(admin.ModelAdmin):
    inlines = [CourseInline, ]
    list_display = ['name','introduction']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'homework', 'subject', 'teacher']

class ScoreAdmin(admin.ModelAdmin):
    search_fields = ('student__name','student__classroom__name')
    list_display = ['student', 'subject','score']
    # fields = ('student', 'subject','title','score')
    list_filter = ('subject',)
    # form = ScoreForm
    # fields = ('student', 'subject', 'title', 'score')



class TestFormAdmin(admin.ModelAdmin):
    # inlines = [ScoreInline, ]
    list_display = ['title','testScore']

admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Classroom,ClassroomAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Score,ScoreAdmin)
# admin.site.register(TestForm,TestFormAdmin)
