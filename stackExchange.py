import stackexchange
from bs4 import BeautifulSoup
import psycopg2
import datetime

def insertUser(site,userid, conn):
    user = site.users(userid)[0]
    #TODO
    insertuser = 'insert into users values(%d, \'%s\', \'%s\');' %(user.id, user.display_name, user.creation_date)
    selectuser = 'select * from users where userid = %d;' %(user.id)
    cur = conn.cursor()
    try:
        cur.execute(selectuser)
    except Exception as e:
        print e
    else:
        if cur.fetchone() == None:
            cur.execute(insertuser)
            conn.commit()
        badgeCounts= user.json['badge_counts']
        for badge in badgeCounts:
            if(badgeCounts[badge]>0):
                selectuserbadge = 'select * from userbadges where badgename = \'%s\' and userid = %d;' %(badge, user.id)
                insertuserbadge = 'insert into userbadges values( \'%s\' , %d );' %(badge,user.id)
                try:
                    cur.execute(selectuserbadge)
                except Exception as e:
                    print e
                else:
                    if cur.fetchone() == None:
                        cur.execute(insertuserbadge)
                        conn.commit()

def insertTag(tag, conn):
    cur = conn.cursor()
    selecttag = 'select * from tags where tagname = \'%s\';' %(tag)
    inserttag = 'insert into tags values(\'%s\');' %(tag)
    try:
        cur.execute(selecttag)
    except Exception as e:
        print e
    else:
        if cur.fetchone() == None:
            cur.execute(inserttag)
            conn.commit()

def insertTagged(tag, questionid, conn):
    cur = conn.cursor()
    selecttagged = 'select * from tagged where tagname = \'%s\' and questionid = %d;' %(tag, questionid)
    inserttagged = 'insert into tagged values(%d, \'%s\');' %(questionid, tag)
    try:
        cur.execute(selecttagged)
    except Exception as e:
        print e
    else:
        if cur.fetchone() == None:
            cur.execute(inserttagged)
            conn.commit()

def insertAnswer(ans, conn, qid, site):
    cur = conn.cursor()
    body= BeautifulSoup(ans.body).text;
    selectanswer = 'select * from answers where answerid = %d;' %(ans.id)
    selectuser = 'select * from users where userid = %d;' %(ans.owner_id)
    insertanswer = 'insert into answers values(%d, %d, %d, \'%s\', \'%s\');' %(ans.id, qid, ans.owner_id, ans.creation_date, body.replace("'", "''"))
    insertUser(site,ans.owner_id,conn)
    try:
        cur.execute(selectanswer)
        fanswer = cur.fetchone()
        cur.execute(selectuser)
        fuser = cur.fetchone()
    except Exception as e:
        print e
    else:
        if fanswer == None and fuser != None:
            cur.execute(insertanswer)
            conn.commit()
            if ans.json != None and ans.json.get('comments') != None:
                insertComments(site, ans.json, conn, ans.id)
                #print "json = ", ans.json

def insertComments(site, json, conn, ansid):
    cur = conn.cursor()
    for comment in json['comments']:
        body = BeautifulSoup(comment['body_markdown'], "lxml").text
        cdate = datetime.datetime.fromtimestamp(comment['creation_date']/1000.0)
        userId = comment['owner']['user_id']
        insertUser(site,userId,conn)
        #TODO
        selectcomment = 'select * from comments where userid = %d and answerid = %d;' %(userId, ansid)
        insertcomment = 'insert into comments values(%d,%d,\'%s\',\'%s\');' %(ansid,userId,cdate,body.replace("'", "''"))
        try:
            cur.execute(selectcomment)
        except Exception as e:
            print e
        else:
            if cur.fetchone() == None:
                cur.execute(insertcomment)
                conn.commit()
   
def main():    
    try:
        site = stackexchange.Site(stackexchange.StackOverflow,'NGR16KWDHIjGDT4E0ZBt4w((')
        print "testtest 1"
        site.be_inclusive()
        print "testtest 2"
        count=0;
        conn = psycopg2.connect("dbname='ry2294' user='ry2294' password='VFGTHP' host='w4111db.eastus.cloudapp.azure.com'")
        print "testtest 3"
        for q in site.questions(pagesize=100,filter='!BHTP)Vsd03.5*FXL(yaiuPYpjIkySi'):
            try:
                try:
                    insertUser(site, q.owner_id, conn)
                except Exception as e:
                    print "Could not add user", e
                else:
                    body= BeautifulSoup(q.body).text
                    #TODO
                    selectquestion = 'select * from questions where questionid = %d;' %(q.id)
                    insertquestion = 'insert into questions values( %d, %d, \'%s\', \'%s\',\'%s\')' %(q.id,q.owner_id,q.creation_date,q.title.replace("'", "''"),body.replace("'", "''"))
                    cur = conn.cursor()
                    try:
                        cur.execute(selectquestion)
                    except Exception as e:
                        print e
                    else:
                        if cur.fetchone() == None:
                            cur.execute(insertquestion)
                            conn.commit()
                    for tag in q.tags:
                        insertTag(tag, conn)
                        insertTagged(tag, q.id, conn)
                    for ans in q.answers:
                        insertAnswer(ans, conn, q.id, site)
                    count=count+1
                    if(count>=100): 
                        break;
            except Exception as e:
                print "Error ", e
    except Exception as e:
        print "test", e

if __name__=="__main__":
    main()