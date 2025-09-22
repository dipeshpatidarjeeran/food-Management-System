import mysql.connector, os
from flask import render_template,redirect,request
from werkzeug.utils import secure_filename
con = mysql.connector.connect(host="localHost",user="root",password="asdf@123",database="foodManagementSystem")


def addFood():
    if request.method == "GET":
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("foods/addFood.html",cats=cats)
    else:
        food_name = request.form.get("food_name")
        cid = request.form.get("category")
        price = request.form.get("price")
        description = request.form.get("description")

        f = request.files['image_url']
        filename = secure_filename(f.filename)
        filepath = "static/Images/" + f.filename   # save path
        f.save(filepath)

        filename = "Images/"+secure_filename(f.filename)
        sql = "insert into food(food_name,cid,price,description,image,status) values (%s,%s,%s,%s,%s,%s)"
        val = (food_name,cid,price,description,filename,"Available")
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showAllFoods")
    

def showAllFoods():
    sql = """select food_id,food_name,price,description,image,cname,c.cid from food f 
                inner join category c on c.cid=f.cid"""
    cursor = con.cursor()
    cursor.execute(sql)
    foods = cursor.fetchall()
    return render_template("foods/showAllFoods.html",foods=foods)  


def deleteFood(fid):
    if request.method == "GET":
        return render_template("foods/deleteFood.html")
    else:
        action = request.form.get("action")
        if action == "Yes":
            sql = "delete from food where food_id=%s"
            val = (fid,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect("/showAllFoods")


def updateFood(fid):
    if request.method == "GET":
        cursor = con.cursor()
        sql = """select food_id,food_name,price,description,image,cname,c.cid from food f 
                inner join category c on c.cid=f.cid where food_id=%s"""
        val = (fid,)
        cursor.execute(sql,val)
        food = cursor.fetchone()

        sql1 = "select * from Category"
        cursor.execute(sql1)
        cats = cursor.fetchall()
        return render_template("foods/updateFood.html",food=food,cats=cats)



def dashBoard():
    sql = "select * from food"
    cursor = con.cursor()
    cursor.execute(sql)
    foods = cursor.fetchall()

    sql1 = "select * from category"
    cursor.execute(sql1)
    cats = cursor.fetchall()
    return render_template("dashboard.html",foods=foods,cats=cats)