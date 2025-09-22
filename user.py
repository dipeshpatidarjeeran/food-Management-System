from flask import render_template,redirect,request,session
import mysql.connector

con = mysql.connector.connect(host="localHost",user="root",password="asdf@123",database="foodManagementSystem")


def homePage():
    return render_template("homepage.html")