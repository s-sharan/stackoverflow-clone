import psycopg2

try:
    conn = psycopg2.connect("dbname='ry2294' user='ry2294' password='VFGTHP' host='w4111db.eastus.cloudapp.azure.com'")
    cur = conn.cursor()
    result = cur.execute('insert into sampleusers(userid) values(1);')
    print result
except Exception as e:
    print e