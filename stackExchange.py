import stackexchange
from bs4 import BeautifulSoup

def insertUser(site,userid):
    #TODO
    #Query the database to check if the user is already present, if not present 
    #then insert the user into the database
    user = site.users(userid)[0]
    #TODO
    sql = 'insert into Users values(%d, %s, %s)' %(user.id, user.display_name,user.creation_date) 
    badgeCounts= user.json['badge_counts']
    for badge in badgeCounts:
        if(badgeCounts[badge]>0):
            #TODO
            sql = 'insert into UserBadges(%s,%d)' %(badge,user.id)

def insertTag(tagname):
    #TODO
    #Query the database to check if the tag is already present, if not present 
    #then insert the tag into the database
    sql = 'insert into Tags values(%s)' %(tagname)

def insertComments(site, json):
    for comment in q.json['comments']:
        text = BeautifulSoup(comment['body_markdown']).text
        cdate = comment['creation_date']
        userId = comment['owner']['user_id']
        insertUser(site,userId)
        postId = comment['post_id']
        #TODO
        sql = 'insert into Comments values(%s,%d,%d,%s)' %(cdate,userId,postId,text)
   
def main():    
    try:
        site = stackexchange.Site(stackexchange.StackOverflow,'NGR16KWDHIjGDT4E0ZBt4w((')
        site.be_inclusive()
        count=0;
        for q in site.questions(pagesize=10,filter='!BHTP)Vsd03.5*FXL(yaiuPYpjIkySi'):
            try:
                try:
                    insertUser(site, q.owner_id)
                except:
                    print "Could not add user"
                else:
                    body= BeautifulSoup(q.body).text
                    #TODO
                    sql = 'insert into Questions values( %d, %d, %s, %s,%s)' %(q.id,q.owner_id,q.creation_date,q.title,body)
                    # insertComments(site,q.json)
                    # Currently we are ignoring comments to questions
                    for tag in q.tags:
                        insertTag(tag);
                        #TODO
                        sql= 'insert into Tagged values(%d,%s)' %(q.owner_id,tag);
                    ans= q.answers
                    for a in ans:
                        insertUser(site,a.owner_id)
                        body= BeautifulSoup(a.body).text;
                        #TODO
                        sql = 'insert into Answers values( %d, %d,%d, %s,%s)' %(a.id,a.owner_id,q.id,a.creation_date,body)
                        insertComments(site,a.json)
                    count=count+1
                    print q
                    if(count>=10): 
                        break;
            except:
                print "Could not add question"
    except :
        print "Exception"

if __name__=="__main__":
    main()