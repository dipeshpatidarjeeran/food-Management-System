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

    sql1 = "select * from order_master"
    cursor.execute(sql1)
    orders = cursor.fetchall()

    sql1 = "select * from users"
    cursor.execute(sql1)
    users = cursor.fetchall()
    return render_template("admin/adminDashboard.html",foods=foods,cats=cats,orders=orders,users=users)



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
    session.pop("admin")
    return redirect("/adminLogin")


def viewDetails(fid):
    sql = """select food_id,food_name,price,description,image,cname,c.cid from food f 
                inner join category c on c.cid=f.cid where f.food_id=%s"""
    val = (fid,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    food = cursor.fetchone()
    return render_template("admin/foodDetails.html",food=food)


def adminSearchFood():
    data = request.form.get("searchFood")
    if data:
        data = data[:3]
        sql = f"select * from food where food_name like  '%{data}%'"
        cursor = con.cursor()
        cursor.execute(sql)
        foods = cursor.fetchall()
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("admin/adminDashboard.html",foods=foods,cats=cats)
    else:
        return redirect("/adminDashboard")


def showAllOrders():
    if "admin" in session:
        # sql = "select * from cart_vw m inner join order_master o on o.order_id = m.order_id where m.username=%s"
        sql = "select distinct(order_id),date_of_order,amount,username from order_vw"
        cursor = con.cursor()
        cursor.execute(sql)
        order_details = cursor.fetchall()

        sql = "select food_name,price,description,image,qty,sub_total,order_id from order_vw"
        cursor = con.cursor()
        cursor.execute(sql)
        product_details = cursor.fetchall()

        final_data = {}
        for order in order_details:
            final_data[order] = []
            for product in product_details:
                if order[0] == product[6]:
                    final_data[order].append(product)

        return render_template("admin/showAllOrders.html",final_data=final_data)
    else:
        return redirect("/adminLogout")


def showAllUsers():
    sql = "select * from users"
    cursor = con.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    return render_template("admin/showAllUsers.html",users=users)
