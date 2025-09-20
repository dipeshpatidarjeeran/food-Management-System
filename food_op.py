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
        cid = request.form.get("cid")
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
    return render_template("foods/showAllFoods.html")    
def dashBoard():
    return render_template("dashboard.html")