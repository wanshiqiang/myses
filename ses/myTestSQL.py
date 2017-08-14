# -*- coding: utf-8 -*-

from . import models
from django.db import connection

def testQuery():
    cursor = connection.cursor()
    cursor.execute('''
                        SELECT student_id,
                        max(CASE title WHEN '课堂表现' THEN score ELSE 0 end)课堂表现,
                        max(CASE title WHEN '数学' THEN score ELSE 0 end)数学,
                        max(CASE title WHEN '物理' THEN score ELSE 0 end)物理,
                        sum(score)总分,
                        cast(avg(score*1.0)AS DECIMAL(18,2))平均分
                        FROM ses_score
                        GROUP BY student_id
                    '''
                   )
    print '==========================================='
    print cursor.fetchone()
    print type(cursor.fetchone())
    # print type(query)
    cds = cursor.fetchall()
    print type(cds)
    print cds

    cursor.close()

if __name__ == '__main__':
    testQuery()