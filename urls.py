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


app.add_url_rule("/",view_func=u.homePage)