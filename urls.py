from main import app

import category_op as cat
import food_op as f
import admin as a
import user as u

app.add_url_rule('/addCategory',view_func=cat.addCategory,methods=["GET","POST"])
app.add_url_rule('/showAllCategory',view_func=cat.showAllCategory,methods=["GET"])
app.add_url_rule('/deleteCategory/<cid>',view_func=cat.deleteCategory,methods=["GET","POST"])
app.add_url_rule('/updateCategory/<cid>',view_func=cat.updateCategory,methods=["GET","POST"])

app.add_url_rule('/addFood',view_func=f.addFood,methods=["GET","POST"])
app.add_url_rule('/showAllFoods',view_func=f.showAllFoods,methods=["GET","POST"])
app.add_url_rule('/deleteFood/<fid>',view_func=f.deleteFood,methods=["GET","POST"])
app.add_url_rule('/updateFood/<fid>',view_func=f.updateFood,methods=["GET","POST"])


app.add_url_rule('/adminDashboard',view_func=a.adminDashboard)
app.add_url_rule('/adminLogin',view_func=a.adminLogin,methods=["GET","POST"])
app.add_url_rule('/adminLogout',view_func=a.adminLogout)
app.add_url_rule('/adminSearchFood',view_func=a.adminSearchFood,methods=['GET','POST'])
app.add_url_rule('/viewDetails/<fid>',view_func=a.viewDetails)


app.add_url_rule("/",view_func=u.homePage)
app.add_url_rule("/menu/<cid>",view_func=u.menu)
app.add_url_rule("/foodDetails/<fid>",view_func=u.foodDetails,methods=["GET","POST"])
app.add_url_rule("/login",view_func=u.userLogin,methods=["GET","POST"])
app.add_url_rule("/register",view_func=u.userRegister,methods=["GET","POST"])
app.add_url_rule("/logout",view_func=u.userLogout)
app.add_url_rule("/searchFood",view_func=u.searchFood,methods=["GET","POST"])
app.add_url_rule("/addToCart",view_func=u.addToCart,methods=["GET","POST"])
app.add_url_rule("/showCart",view_func=u.showCart,methods=["GET","POST"])
app.add_url_rule("/updateCart",view_func=u.updateCart,methods=["GET","POST"])
