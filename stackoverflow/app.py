from flask import Flask, render_template, request
from flask.ext.triangle import Triangle
app = Flask(__name__)
Triangle(app)

@app.route("/index.html")
def indexHTML():
    return render_template('index.html')
    
@app.route("/search",methods=['GET','POST'])
def search():
    if(request.method== 'GET'):
        print(request,"Successfully rendered")

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

if __name__ == "__main__":
    app.run()
