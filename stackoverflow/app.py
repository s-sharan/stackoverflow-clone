from flask import Flask, render_template, request, redirect, url_for
from flask.ext.triangle import Triangle
import psycopg2
import json
from datetime import date
from StringIO import StringIO

app = Flask(__name__)
Triangle(app)
conn = psycopg2.connect("dbname='ry2294' user='ry2294' password='VFGTHP' host='w4111db.eastus.cloudapp.azure.com'")

@app.route("/")
def indexHTML():
    return render_template('index.html')
    
@app.route("/search",methods=['POST'])
def search():
    global conn;
    if(request.method== 'POST'):
        content = request.get_json()["query"]
        print(content.lower())
        sql = 'select * from questions where lower(title) like \'%s%s%s\';'%('%',content.lower(),'%')
        jsonArr=[]
        cur = conn.cursor()
        try:
            cur.execute(sql)
            rows=cur.fetchall()
            for row in rows:
                jsonOb={}
                jsonOb['questionid']=row[0]
                jsonOb['userid']=row[1]
                jsonOb['title']=row[3]
                jsonOb['body']=row[4]
                jsonArr.append(jsonOb)
        except Exception as e:
            print e
    return str(json.dumps(jsonArr))

@app.route("/question",methods=['POST'])
def questionSearch():
    global conn;
    print 'tfdsete'
    if(request.method == 'POST'):
        print 'tetete'
        content = request.get_json()["query"]
        print(content)
        sql = 'select * from answers a left outer join comments c on a.answerid=c.answerid where a.questionid=%s;'%(content)
        print(sql)
        cur = conn.cursor()
        try:
            cur.execute(sql)
            rows=cur.fetchall()
            jsonArr=[]
            ans={}
            for row in rows:
                answers={}
                comments={}
                if(row[5]!=None):
                    comments['answerid']=row[5]
                    comments['userid']=row[6]
                    comments['body']=row[8]
                if(row[0] not in ans):
                    answers['answerid']=row[0]
                    answers['questionid']=row[1]
                    answers['userid']=row[2]
                    answers['body']=row[4]
                    c=[]
                    c.append(comments)
                    answers['comments']=c
                    ans[row[0]]=answers
                else:
                    answers=ans[row[0]]
                    c=answers['comments']
                    c.append(comments)
                    answers['comments']=c
                    ans[row[0]]=answers
        except Exception as e:
            print e

    return str(json.dumps(ans))


@app.route("/userinfo",methods=['POST'])
def getUserInfo():
    global conn;
    if(request.method== 'POST'):
        content = request.get_json()["username"]
        sql='select * from users u, userbadges b where u.userid=b.userid lower(name) =\'%s\';'%(content.lower())
        print(sql)
        userArr=[]
        cur = conn.cursor()
        try:
            cur.execute(sql)
            rows=cur.fetchall()
            for row in rows:
                jsonOb={}
                jsonOb['userid']=row[0]
                jsonOb['name']=row[1]
                jsonOb['badgename']=row[3]
                userArr.append(jsonOb)
        except Exception as e:
            print e
    res={}
    print(userArr)
    res['result']=userArr;
    return str(res)
         
    
@app.route("/insertquestion",methods=['POST'])
def insertquestion():
    global conn;
    print(request.get_json())
    content = request.get_json()
    userid=content["userid"]
    title=content["title"]
    body=content["body"]
    tags=content["tags"]
    print userid,title,body,tags
    today = date.today().isoformat()
    sql='select max(questionid) from questions'
    cur = conn.cursor()
    try:
        cur.execute(sql)
        res=cur.fetchone()
        questionid=int(res[0])+1
        sql='insert into questions values(%d,%s,\'%s\',\'%s\',\'%s\');'%(questionid,userid,today,title,body)
        print(sql)
        cur.execute(sql)
        conn.commit()
        for  tag in tags:
            sql='insert into tagged values(%d,\'%s\');'%(questionid,tag)
            cur.execute(sql)
            conn.commit()
    except Exception as e:
        print(e)
    return "Successfully added to database"
    
    
@app.route("/login.html")
def loginHTML():
    return render_template('login.html')

@app.route("/search.html")
def searchHTML():
    return render_template('search.html')

@app.route("/question.html")
def questionHTML():
    return render_template('question.html')

@app.route("/createQuestion.html")
def createQuestionHTML():
    return render_template('createQuestion.html')

@app.route("/admin.html")
def adminHTML():
    return render_template('admin.html')

if __name__ == "__main__":
    conn = psycopg2.connect("dbname='ry2294' user='ry2294' password='VFGTHP' host='w4111db.eastus.cloudapp.azure.com'")
    app.run()
