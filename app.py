from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MYSQL connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_PORT"] = 3307
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

#Loading Home Page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "Select * from users"
    con.execute(sql)
    res = con.fetchall()
    return render_template("home.html",datas = res)

# new user (insert)
@app.route("/add_User",methods=['GET','POST'])
def addUsers():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        con = mysql.connection.cursor()
        sql = "insert into users(NAME,AGE,CITY) value (%s,%s,%s)"
        con.execute(sql,[name,age,city])
        mysql.connection.commit()
        con.close()
        flash("User Details Added")
        return redirect(url_for("home"))
    return render_template("newUser.html")

#Edit user
@app.route("/edit_User/<string:id>",methods=['GET','POST'])
def editUser(id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        cur = mysql.connection.cursor()  # Create a cursor object
        sql = "UPDATE users SET NAME=%s, AGE=%s, CITY=%s WHERE ID=%s"
        cur.execute(sql, [name, age, city, id])  # Use the cursor to execute the query
        mysql.connection.commit()  # Commit the changes
        cur.close()  # Close the cursor
        flash("User Details Updated")
        return redirect(url_for("home"))
    sql = "select * from users where ID=%s"
    con.execute(sql,[id])
    res = con.fetchone()
    return render_template("editUser.html",datas = res)

#Delete Users
@app.route("/delete_User/<string:id>",methods=["GET","POST"])
def deleteUser(id):
    cur = mysql.connection.cursor()
    sql = "delete from users where ID=%s"
    cur.execute(sql,id)
    mysql.connection.commit()
    cur.close()
    flash("User Details Deleted")
    return redirect(url_for("home"))

if(__name__ == '__main__'):
    app.secret_key="abs1234"
    app.run(debug=True)