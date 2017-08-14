# -*- coding: utf-8 -*-
from . import utils
from . import models
import ses

def testDB():
    subject1 = models.Subject.create(name='信息技术', introduction='学习信息')
    subject1.save()
    # classroom1 = models.Classroom.create(name='五年级8班', clazz=8, grade=5)
    classroom1 = models.Classroom()
    classroom1.name = '五年级8班'
    classroom1.clazz = 8
    classroom1.grade = 5
    classroom1.save()
    # 不需要classromm添加subjects
    # classroom1.subjects.add(subject1)
    homework1 = models.Homework.create(title="作业1",content="作业1内容")
    homework1.save()

    teacher1 = models.Teacher.create(name="老师1",age=26,pwd="123@abcd")
    teacher1.save()

    course = models.Course.create(subject=subject1,classroom=classroom1,homework=homework1,teacher=teacher1)
    course.save()


    # student1 = models.Student.create(name='aaa', number='20125801', pwd='123@abcd', classroom=classroom1)
    # student1.save()

def saveDB():
    saveSubjectDB()
    saveClassroomDB()
    saveStudentDB()

def saveSubjectDB():
    print u"============导入subjectData==============="
    utils.saveSubjectDataFromExcel("subjectData.xlsx")

    subjects = models.Subject.objects.all()
    for index, subject in enumerate(subjects):
        # print 'subject1 name:' + subject.name
        print '_'.join(['subject', str(index + 1), 'name:     ', subject.name]),
        print '_'.join(['subject', str(index + 1), 'info:     ', subject.introduction])


def saveClassroomDB():
    print u"============导入classroom名单==============="
    utils.saveClassroomDataFromExcel("classroomData.xlsx")
def saveStudentDB():
    print u"=============导入students名单=============================="
    utils.saveStudentDataFromExcel("studentData.xlsx")

if __name__ == '__main__':
    saveDB()
