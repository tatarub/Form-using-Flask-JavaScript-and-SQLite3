from threading import Event
from flask import Flask,request,render_template,make_response
import sqlite3


conn = sqlite3.connect('studentdb.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS students (firstName TEXT, lastName TEXT, id TEXT, grade TEXT)')
print("Table created successfully")


app = Flask('__name__')


@app.route("/")
def index():
    return render_template("index.html");
    


@app.route('/process',methods= ['POST'])
def process():
    msg = "msg"
    if request.method == 'POST':
        try:
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            id = request.form['id']
            grade = request.form['grade']
            
            with sqlite3.connect('studentdb.db') as con:
                cur = con.cursor()
                cur.execute('INSERT INTO students (firstName,lastName,id,grade)VALUES (?,?,?,?)',(firstName,lastName,id,grade) )
                con.commit()
                msg = "successfully submited"    
        except:
            conn.rollback()
            msg = 'error in insert operation'
        finally:
            return render_template('index.html',msg = msg)
            con.close()   


@app.route('/proc',methods= ['GET'])
def proc():
    
    with sqlite3.connect("studentdb.db") as con:
        try:
            output = request.values["id"]
            cur = con.cursor()
            cur.execute("select id, firstName, lastName, grade from students where id = ?", (output,))
            result = cur.fetchone()
            print (result)
        except Exception as error:  
            print(error)
        finally:
            if result is None:
                return make_response({}, 404)
            else:
                return {"id": result[0], "firstName": result[1], "lastName": result[2], "grade": result[3]}


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5500, debug=True)
