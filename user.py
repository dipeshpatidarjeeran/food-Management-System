from flask import render_template,redirect,request,session, flash
import mysql.connector

con = mysql.connector.connect(host="localHost",user="root",password="asdf@123",database="foodManagementSystem")


def homePage():
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    return render_template("user/userDashboard.html",cats=cats)


def userRegister():
    if request.method == "GET":
        return render_template("user/userRegister.html")
    else:
        uname = request.form.get("uname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        pwd = request.form.get("pwd")
        address = request.form.get("address")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE uname = %s", (uname,))
        user = cursor.fetchone()

        if user:
            flash("Username already exists! Choose another.")
            return redirect("/register")
        else:
            sql = "insert into Users(uname,email,phone,password,address) value(%s,%s,%s,%s,%s)"
            val = (uname,email,phone,pwd,address)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
            return redirect("/login")

    

def userLogin():
    if request.method == "GET":
        return render_template("user/userLogin.html")
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        sql = "select count(*) from Users where uname=%s and password=%s"
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if count[0] == 0:
            return redirect("/login")
        else:
            session['uname'] = uname
            return redirect("/menu/all")
        

def userLogout():
    session.clear()
    return redirect("/")

def menu(cid):
    cursor = con.cursor()
    if cid == "all":
        sql = "select * from food"
        cursor.execute(sql)
    else:
        sql = "select * from food where cid=%s"
        val = (cid,)
        cursor.execute(sql,val)
    
    foods = cursor.fetchall()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    return render_template("user/menu.html",foods=foods,cats=cats)


def foodDetails(fid):
    sql = """select food_id,food_name,price,description,image,cname,c.cid from food f 
                inner join category c on c.cid=f.cid where f.food_id=%s"""
    val = (fid,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    food = cursor.fetchone()
    return render_template("user/foodDetails.html",food=food)


def searchFood():
    data = request.form.get("searchFood")
    data = data[:3]
    sql = f"select * from food where food_name like  '%{data}%'"
    cursor = con.cursor()
    cursor.execute(sql)
    foods = cursor.fetchall()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    return render_template("user/menu.html",foods=foods,cats=cats)