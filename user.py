from flask import render_template,redirect,request,session, flash
import mysql.connector
import datetime

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
    if request.method == 'GET':
        sql = """select food_id,food_name,price,description,image,cname,c.cid from food f 
                    inner join category c on c.cid=f.cid where f.food_id=%s"""
        val = (fid,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        food = cursor.fetchone()
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("user/foodDetails.html",food=food,cats=cats)
    else:
        session["food_id"] = request.form.get("food_id")
        session["qty"] = request.form.get("quantity")
        return redirect("/addToCart")


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


def addToCart():
    print(session)
    if "uname" in session:
        sql = "select count(*) from MyCart where food_id=%s and username=%s and order_id is null"
        val = (session["food_id"],session["uname"])
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if count[0] == 1:
            #This is a duplicate item
            return redirect("/showCart")
        else:
            #Perform add to cart        
            sql = "insert into mycart (food_id,username,qty,status) values (%s,%s,%s,%s)"
            val = (session["food_id"],session["uname"],session["qty"],0)
            cursor.execute(sql,val)
            con.commit()
            return redirect("/showCart")
    else:
        return redirect("/login")
    
def showCart():
    if "uname" in session:
        sql = "select * from cart_vw where username=%s and order_id is null"
        val = (session['uname'],)
        cursor = con.cursor()
        cursor.execute(sql,val)
        carts = cursor.fetchall()

        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        total = 0
        for cart in carts:
            total += float(cart[8])
        gst = total * 0.05
        grand_total = total + gst

        session['grand_total'] = grand_total
        return render_template("user/showCart.html",carts=carts,cats=cats,gst=gst,total=total)
    else:
        return redirect("/login")
    

def updateCart():
    cart_id = request.form.get("cart_id")
    action = request.form.get("action")
    cursor = con.cursor()
    
    cursor.execute("select qty from mycart where Id=%s", (cart_id,))
    row = cursor.fetchone()
    qty = row[0]

    if action == "increase":
        qty += 1
        cursor.execute("update mycart set qty=%s where Id=%s", (qty, cart_id))

    elif action == "decrease":
        qty -= 1
        if qty > 0:
            cursor.execute("update mycart set qty=%s where Id=%s", (qty, cart_id))
        else:
            cursor.execute("delete from mycart where Id=%s", (cart_id,))

    elif action == "remove":
        cursor.execute("delete from mycart where Id=%s", (cart_id,))

    con.commit()
    cursor.close()

    return redirect("/showCart")


def MakePayment():
    if request.method == "GET":
        sql = "select * from cart_vw where username=%s and order_id is null"
        val = (session['uname'],)
        cursor = con.cursor()
        cursor.execute(sql,val)
        carts = cursor.fetchall()
        return render_template("user/makePayment.html",carts=carts)
    else:
        cardno = request.form.get("cardno")
        cvv = request.form.get("cvv")
        expiry = request.form.get("expiry")
        sql = "select count(*) from Payment where cardno=%s and cvv=%s and expiry=%s"
        val = (cardno,cvv,expiry)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if count[0] == 1:
            # buyer update
            sql = "update payment set balance=balance-%s where cardno=%s and cvv=%s and expiry=%s"
            val = (session['grand_total'],cardno,cvv,expiry)
            cursor.execute(sql,val)
            #seller update
            sql = "update payment set balance=balance+%s where cardno=%s and cvv=%s and expiry=%s"
            val = (session['grand_total'],"222",'222','12/2030')
            cursor.execute(sql,val)
            con.commit()
            
            sql = "insert into order_master (date_of_order,amount) values (%s,%s)"
            val = (datetime.datetime.now().date(),session["grand_total"])
            cursor.execute(sql,val)
            con.commit()
            sql = "select order_id from order_master where date_of_order=%s and amount=%s"
            val = (datetime.datetime.now().date(),session["grand_total"])
            cursor.execute(sql,val)
            order_id = cursor.fetchone()[0]
            #print(order_id)
            sql = "update mycart set order_id=%s,status=1 where username=%s and order_id is null"
            val = (order_id,session["uname"])
            cursor.execute(sql,val)
            con.commit()
            session.pop("grand_total")
            
            return redirect("/menu/all")
        else:
            return redirect("/makePayment")