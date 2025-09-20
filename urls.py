from main import app

import category_op as cat
import food_op as f

app.add_url_rule('/addCategory',view_func=cat.addCategory,methods=["GET","POST"])
app.add_url_rule('/showAllCategory',view_func=cat.showAllCategory,methods=["GET"])
app.add_url_rule('/deleteCategory/<cid>',view_func=cat.deleteCategory,methods=["GET","POST"])
app.add_url_rule('/updateCategory/<cid>',view_func=cat.updateCategory,methods=["GET","POST"])

app.add_url_rule('/addFood',view_func=f.addFood,methods=["GET","POST"])
app.add_url_rule('/showAllFoods',view_func=f.showAllFoods,methods=["GET","POST"])


app.add_url_rule('/Dashboard',view_func=f.dashBoard,methods=["GET"])
