#coding: utf8
import os, time, psycopg2

delay = 30

db_host = '192.168.10.152'
db_name = 'gxddb'
db_port = 5432
db_user = 'postgres'
db_pass = 'postgres@#DBM'

conn = psycopg2.connect(host=db_host, port=db_port, user=db_user, password=db_pass, database=db_name)
conn.autocommit = True
cursor = conn.cursor()

while 1:
    cursor.execute("select public.maintain_vacuum()")
    t = cursor.fetchone()
    if t:
        tablename = t[0]
        cursor.execute("vacuum full analyze %s" % tablename)
        #print 'vacuum %s' % tablename
    else:
        cursor.execute("select public.maintain_analyze()")
        t = cursor.fetchone()
        if t:
            tablename = t[0]
            cursor.execute("analyze %s" % tablename)
            #print 'analyze %s' % tablename
    time.sleep(delay)
