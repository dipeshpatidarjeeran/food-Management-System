from flask import render_template,redirect,request,session
import mysql.connector

con = mysql.connector.connect(host="localHost",user="root",password="asdf@123",database="foodManagementSystem")

def login_required(fun): 
    def wrapper(): 
        if "admin" in session: 
            return fun() 
        else: 
            return redirect("/adminLogin") 
    return wrapper

@login_required
def adminDashboard():
    sql = "select * from food"
    cursor = con.cursor()
    cursor.execute(sql)
    foods = cursor.fetchall()

    sql1 = "select * from category"
    cursor.execute(sql1)
    cats = cursor.fetchall()
    return render_template("admin/adminDashboard.html",foods=foods,cats=cats)



def adminLogin():
    if request.method == "GET":
        return render_template("admin/adminLogin.html")
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        sql = "select count(*) from adminlogin where username=%s and password=%s"
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if count[0] == 0:
            return redirect("/adminLogin")
        else:
            session['admin'] = uname
            return redirect("/adminDashboard")
        

def adminLogout():
    session.clear()
    return redirect("/adminLogin")
