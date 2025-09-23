from flask import render_template,redirect,request,session
import mysql.connector

con = mysql.connector.connect(host="localHost",user="root",password="asdf@123",database="foodManagementSystem")


def homePage():
    return render_template("user/userDashboard.html")


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