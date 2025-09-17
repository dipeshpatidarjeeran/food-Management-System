from flask import render_template,redirect,request
import mysql.connector

con = mysql.connector.connect(host="localHost",user="root",password="asdf@123",database="foodManagementSystem")

def addCategory():
    if request.method == "GET":
        return render_template("addCategory.html")
    else:
        cname = request.form.get("cname")
        sql = "insert into Category (cname) values (%s)"
        val = (cname,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return "Record added..."


def showAllCategory():
    sql = "select * from Category"
    cursor = con.cursor()
    cursor.execute(sql)
    cate = cursor.fetchall()
    return render_template("showAllCategory.html",cate=cate)
 

def deleteCategory(cid):
    if request.method == "GET":
        return render_template("deleteConfirm.html")
    else:
        action = request.form.get("action")
        if action == "Yes":
            sql = "delete from Category where cid=%s"
            val = (cid,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect("/showAllCategory")


def updateCategory(cid):
    if request.method == 'GET':
        sql = "select * from Category where cid=%s"
        val = (cid,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        cate = cursor.fetchone()
        return render_template("updateCategory.html",cate=cate)
    else:
        cname = request.form.get("cname")
        sql = "update Category set cname=%s where cid=%s"
        val = (cname,cid)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showAllCategory")
